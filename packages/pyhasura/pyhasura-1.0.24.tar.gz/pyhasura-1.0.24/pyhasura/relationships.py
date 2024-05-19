import hashlib
import re
import copy
import camelcaser as cc
from neo4j import GraphDatabase
from pluralizer import Pluralizer
from graphql import is_object_type, is_non_null_type, is_list_type, is_leaf_type, is_enum_type, is_wrapping_type, \
    get_named_type
from sklearn_extra.cluster import KMedoids

from pyhasura.helpers import get_ordinal_of_smallest_number, compute_deltas
from pyhasura.keys import combine_words
from pyhasura.synonyms import split_cased_phrase, get_last_noun_sequence, get_synonyms
from pyhasura.vectorize import vectorize_string, find_related_words
import diskcache

# Specify the path where you want to store the cache
cache_path = ".cache/pyhasura/relationships"

# Create or load the cache
cache = diskcache.Cache(cache_path)

pluralizer = Pluralizer()

fk_candidates = {}
ak_candidates = {}
correlation_test = {}


class Relationships:
    def __init__(self, metadata, schema,
                 disallowed_key_types=None,
                 entity_synonyms=None,
                 alternate_keys=None,
                 key_suffixes=None,
                 logging_=None,
                 client=None,
                 key_uniqueness_test_size=10000,
                 key_uniqueness_test_rate=.2,
                 key_correlation_test_size=300000,
                 key_correlation_test_rate=.05
                 ):
        self.logging = logging_
        self.metadata = copy.deepcopy(metadata)
        self.schema = schema
        self.disallowed_key_types = disallowed_key_types or ['timestamptz', 'Boolean', 'timestamp']
        self.entity_synonyms = entity_synonyms or {}
        self.alternate_keys = alternate_keys or ['state', 'city', 'country', 'zip code', 'postal code']
        self.alternate_keys = self._get_cached_data(self.alternate_keys)
        self.alternate_keys_regex = [re.compile(ak, re.IGNORECASE) for ak in self.alternate_keys]
        self.key_suffixes = key_suffixes or ['id', 'key', 'serial number', 'code']
        self.relationships = []
        self.valid_keys = set()
        self.client = client
        self.key_uniqueness_test_size = key_uniqueness_test_size
        self.key_uniqueness_test_rate = key_uniqueness_test_rate
        self.key_correlation_test_size = key_correlation_test_size
        self.key_correlation_test_rate = key_correlation_test_rate
        self.type_names = [source.get('customization', {}).get('type_names') for source in
                           self.metadata.get('sources', [])
                           if source.get('customization', {}).get('type_names') is not None]

        def get_prefix_object_names(source):
            root_fields = source.get('customization', {}).get('root_fields', {})
            # prefix = root_fields.get('prefix', '')
            # suffix = root_fields.get('suffix', '')
            namespace = root_fields.get('namespace', '')
            return [
                f'{namespace}_mutation_frontend',
                f'{namespace}_query',
                f'{namespace}_subscription'
            ]

        self.root_fields = []
        for source in self.metadata.get('sources', []):
            if source.get('customization', {}).get('root_fields') is not None:
                self.root_fields += get_prefix_object_names(source)
        self.valid_keys_uniqueness = {}

    def _get_data_from_source(self, alternate_keys):

        self.logging.info('Generating the alternate key cache. This may take several minutes on first run.')
        candidates = [candidate.split() for candidate in alternate_keys]
        word_lists = []

        for candidate in candidates:
            word_list = []
            for word in candidate:
                synonyms = [synonyms.replace('_', ' ').lower() for synonyms in get_synonyms(word.lower())]
                synonyms.append(word.lower())
                synonyms = list(set(synonyms))
                word_list.append(synonyms)
            combined = combine_words(word_list)
            word_lists.append(combined)
        word_lists = sum(word_lists, [])
        result = ['|'.join(list({cc.make_snake_case(ak), cc.make_lower_camel_case(ak), ak})) for ak in word_lists]
        return result

    def _get_cached_data(self, alternate_keys):
        input_key = hashlib.sha256(bytes("\n".join(alternate_keys), "utf-8")).hexdigest()
        data = cache.get(input_key)
        # Check if data is already cached
        if data is None:
            # Derive data and cache it
            data = self._get_data_from_source(alternate_keys)
            result = cache.set(input_key, data)
            test = cache.get(input_key)
        return data

    def _create_pk_candidates(self, entity):
        schema = self.schema
        key_hints = self.key_suffixes
        phrase = split_cased_phrase(self.remove_type_names(entity))
        assumed_name = get_last_noun_sequence(phrase)
        similar_words = [{word.lower()} for word in assumed_name]
        for index, word_list in enumerate(similar_words):
            original = next(iter(word_list))
            similar_words[index] = word_list.union(
                set([word.replace('_', ' ') for word in get_synonyms(original)])).union(
                set([word.replace('_', ' ') for word in find_related_words(original)]))
        similar_words.append(key_hints)
        add_key_hints = list(set(
            [pluralizer.singular(hint) for hint in key_hints] +
            [pluralizer.plural(hint) for hint in key_hints]
        ))
        candidates = [candidate.split() for candidate in combine_words(similar_words)]
        if self.entity_synonyms.get(entity):
            candidates = candidates + \
                         [candidate.split() for candidate in
                          combine_words([self.entity_synonyms.get(entity), key_hints])]
        candidates_regexes = (
                ['^.*(' + ').*('.join(phrase) + ').*$' for phrase in candidates] +
                ['^(' + hint + ')$' for hint in add_key_hints])
        _regex = '|'.join(candidates_regexes)
        regex = re.compile(_regex, re.IGNORECASE)
        fields = schema.type_map[entity].fields.keys()
        possible_keys = set()
        for field in fields:
            if regex.match(field):
                possible_keys.add(field)
        return list(possible_keys)

    def _create_fk_candidates(self, primary_entity, foreign_entity, schema):
        key_hints = self.key_suffixes
        if fk_candidates.get(primary_entity) is None:
            phrase = split_cased_phrase(self.remove_type_names(primary_entity))
            assumed_name = get_last_noun_sequence(phrase)
            similar_words = [{word.lower()} for word in assumed_name]
            for index, word_list in enumerate(similar_words):
                original = next(iter(word_list))
                similar_words[index] = word_list.union(
                    set([word.replace('_', ' ') for word in get_synonyms(original)])).union(
                    set([word.replace('_', ' ') for word in find_related_words(original)]))
            similar_words.append(key_hints)
            candidates = [candidate.split() for candidate in combine_words(similar_words)]
            candidates += [[phrase] for phrase in key_hints]
            candidates_regexes = ['^.*(' + ').*('.join(phrase) + ').*$' for phrase in candidates]
            _regex = '|'.join(candidates_regexes)
            regex = re.compile(_regex, re.IGNORECASE)
            fk_candidates[primary_entity] = regex
        else:
            regex = fk_candidates[primary_entity]

        fields = [field[0] for field in schema.type_map[foreign_entity].fields.items() if is_leaf_type(field[1].type)]
        possible_keys = set()
        for field in fields:
            if regex.match(field):
                possible_keys.add(field)
        return list(possible_keys)

    def _create_ak_candidates(self, primary_entity, foreign_entity):
        possible_keys = set()
        if self.alternate_keys:
            schema = self.schema
            primary_fields = [field[0] for field in schema.type_map[primary_entity].fields.items() if
                              is_leaf_type(field[1].type)]
            foreign_fields = [field[0] for field in schema.type_map[foreign_entity].fields.items() if
                              is_leaf_type(field[1].type)]
            for regex in self.alternate_keys_regex:
                for foreign_field in foreign_fields:
                    for primary_field in primary_fields:
                        if regex.match(foreign_field) and regex.match(primary_field):
                            possible_keys.add((primary_entity, primary_field, foreign_entity, foreign_field))
        return list(possible_keys)

    def _get_leaf_type(self, t):
        if not is_leaf_type(t):
            return self._get_leaf_type(t.of_type)
        return t

    def _get_concrete_type(self, t):
        if is_wrapping_type(t):
            return self._get_concrete_type(t.of_type)
        return t

    def _is_list_type(self, t):
        if is_wrapping_type(t):
            if is_list_type(t):
                return True
            return self._is_list_type(t.of_type)
        return False

    def _is_relationship(self, t):
        if is_non_null_type(t):
            return self._is_relationship(t.of_type)
        return is_list_type(t) or is_object_type(t)

    @staticmethod
    def remove_prefix_and_suffix(text, prefix, suffix):
        # Construct a regular expression pattern to match the prefix and suffix
        pattern = f"^{re.escape(prefix)}(.*?){re.escape(suffix)}$"

        # Use re.sub() to replace the matched pattern with an empty string
        result = re.sub(pattern, r"\1", text)

        return result

    def remove_type_names(self, t):
        x = str(t)
        for type_names in self.type_names:
            x = self.remove_prefix_and_suffix(x, type_names.get('prefix', ''), type_names.get('suffix', ''))
        return x

    def _field_documents(self, objects):
        fields = []
        for key, value in objects:
            for field_key, field_value in value.fields.items():
                document = self.remove_type_names(key) + ' ' + str(value.description or '') + ' ' + field_key + ' ' + \
                           str(field_value.description or '')
                document = document.replace('_', ' ')
                vector = vectorize_string(document)
                if not self._is_relationship(field_value.type):
                    fields.append(
                        tuple([
                            key,
                            field_key,
                            document,
                            vector
                        ]))
        return fields

    def _check_object_type(self, item):
        root = self.remove_type_names(item[0])
        return is_object_type(item[1]) and not root.startswith('_') and not root.endswith('_aggregate') and not \
            root.endswith('_root') and not root.endswith('_fields') and not root.endswith('_response') and \
            root not in self.root_fields

    @staticmethod
    def _get_entity_name(source, table):
        return table.get('configuration', {}).get('custom_name') or \
            (source.get('customization', {}).get('type_names', {}).get('prefix', '') + table.get('table', {}).get(
                'name') + source.get('customization', {}).get('type_names', {}).get('suffix', ''))

    def _get_table(self, name=None, table_id=None):
        if name is not None:
            for source in self.metadata.get('sources', []):
                for table in source.get('tables', []):
                    test_name = self._get_entity_name(source, table)
                    if name == test_name:
                        return source, table
        elif table_id is not None:
            for source in self.metadata.get('sources', []):
                for table in source.get('tables', []):
                    if table.get('table', {}) == table_id:
                        return source, table
        return None, None

    def _metadata_tables(self):
        table_list = []
        for source in self.metadata.get('sources', []):
            for table in source.get('tables', []):
                name = self._get_entity_name(source, table)
                table_list.append(tuple([table.get('table'), name]))
        return table_list

    # Relationship: ((primary_table, primary_column, remote_table, remote_column),
    # name, existing|candidate, object|array)
    def create_existing_relationship(self, relationship_type, source, table):
        relationships = []
        for type_of_relationship in table.get(f'{relationship_type}_relationships', []):
            manual_configuration = type_of_relationship.get('using', {}).get('manual_configuration', {})
            remote_table_id = manual_configuration.get('remote_table')
            if remote_table_id is not None:
                column_mapping = list(manual_configuration.get('column_mapping', {}).items())
                remote_source, remote_table = self._get_table(table_id=remote_table_id)
                relationship = tuple([
                    tuple([self._get_entity_name(source, table),
                           column_mapping[0][0],
                           self._get_entity_name(source, remote_table),
                           column_mapping[0][1]]),
                    type_of_relationship.get('name', ''),
                    'existing',
                    relationship_type
                ])
                relationships.append(relationship)
            elif type_of_relationship.get('using', {}).get('foreign_key_constraint_on') is not None:
                self.logging.info('found foreign key constraint')
        if len(relationships) > 0:
            return relationships
        return None

    @staticmethod
    def _list_relationships(table):
        relationships = []
        for relationship_type in ['object', 'array', 'remote']:
            for type_of_relationship in table.get(f'{relationship_type}_relationships', []):
                relationships.append(type_of_relationship.get('name'))
        if len(relationships) > 0:
            return relationships
        return None

    def _get_key_guess_relationships(self):
        relationships = []
        rel_pks = {}
        for object_type in self._get_object_types():
            object_name = object_type[0]
            for remote_object_type in self._get_object_types():
                remote_object_name = remote_object_type[0]
                if remote_object_name != object_name and (object_name, remote_object_name) not in relationships:
                    relationships.append((object_name, remote_object_name))
        self.logging.info(f'Looking for PK/FK in {len(relationships)} combinations')
        for index, relationship in enumerate(relationships):
            pks = rel_pks.get(relationship[0]) if rel_pks.get(relationship[0]) is not None else (
                self._create_pk_candidates(relationship[0]))
            rel_pks[relationship[0]] = pks
            fks = self._create_fk_candidates(relationship[0], relationship[1], self.schema)
            if len(fks) == 0:
                self.logging.info(
                    f'{index + 1}-Entities {relationship[0]} and {relationship[1]} have no potential foreign keys')
            for pk in pks:
                for fk in fks:
                    new_rel = (relationship[0], pk, relationship[1], fk)
                    existing_relationships = [x[0] for x in self.relationships]
                    if new_rel not in existing_relationships:
                        rel = (new_rel, None, 'candidate', None)
                        self.logging.info(f'{index + 1}-Added relationship: {rel}')
                        self.relationships.append(rel)
            aks = self._create_ak_candidates(relationship[0], relationship[1])
            for rel in aks:
                self.logging.info(f'{index + 1}-Added alternate key relationship: {rel}')
                self.relationships.append((rel, None, 'ak', None))

    def _get_existing_relationships(self, tables):
        rels = []
        for table_id in tables:
            source, table = self._get_table(table_id[1])
            r = ((self.create_existing_relationship('object', source, table) or []) +
                 (self.create_existing_relationship('array', source, table) or []))
            rels = rels + list(filter(lambda x: x is not None, r))
        return rels

    def _get_object_types(self):
        return list(filter(self._check_object_type, self.schema.type_map.items()))

    def _get_semantic_relationships(self):
        relationships = []
        object_types = self._get_object_types()
        field_documents = self._field_documents(object_types)
        field_vectors = list(map(lambda x: x[3], field_documents))
        costs = []
        for k in range(2, min(50, len(field_vectors))):
            kmedoids = KMedoids(n_clusters=k, random_state=42)
            kmedoids.fit(field_vectors)
            costs.append(kmedoids.inertia_)
        optimum_clusters = get_ordinal_of_smallest_number(compute_deltas(costs)) + 2

        kmedoids = KMedoids(n_clusters=optimum_clusters, random_state=42)
        kmedoids.fit(field_vectors)
        cluster_labels = kmedoids.labels_
        medoids_indices = kmedoids.medoid_indices_
        for i, cluster_label in enumerate(cluster_labels):
            pk = field_documents[medoids_indices[cluster_label]]
            fk = field_documents[i]
            pk_type = self._get_leaf_type(self.schema.type_map[pk[0]].fields[pk[1]].type)
            fk_type = self._get_leaf_type(self.schema.type_map[fk[0]].fields[fk[1]].type)
            if pk[0] != fk[0] and pk_type.name == fk_type.name and pk_type.name not in self.disallowed_key_types \
                    and not is_enum_type(pk_type):
                forward_id = tuple([pk[0], pk[1], fk[0], fk[1]])
                backward_id = tuple([fk[0], fk[1], pk[0], pk[1]])
                already_exists_forward = len(list(filter(lambda x: x[0] == forward_id, relationships))) > 0
                already_exists_backward = len(list(filter(lambda x: x[0] == backward_id, relationships))) > 0
                if not already_exists_forward and not already_exists_backward:
                    relationship = (forward_id, None, 'candidate', None)
                    self.logging.info(f'Added relationship: {relationship}')
                    relationships.append(relationship)
        if len(relationships) > 0:
            self.relationships = self.relationships + relationships

    # Split by underscores (snake_case) and camel case boundaries
    @staticmethod
    def _extract_words(phrase):
        words = re.findall(r'[A-Z][a-z]*|[a-z]+', phrase)
        return words

    def _find_query_for_entity(self, entity):
        for query_name, query in self.schema.query_type.fields.items():
            if get_named_type(query.type).name == entity:
                return query_name
        return None

    def _get_timestamp_field(self, entity):
        return [name[0] for name in self.schema.type_map.get(entity).fields.items() if
                is_leaf_type(name[1].type) and name[1].type.name in ['timestamp', 'timestampz']]

    def _validate_keys(self):
        keys = set()
        self.valid_keys = set()
        for relationship in self.relationships:
            if relationship[2] == 'ak':
                self.valid_keys.add((relationship[0][0], relationship[0][1]))
                self.valid_keys.add((relationship[0][2], relationship[0][3]))
            elif relationship[3] is None:
                keys.add((relationship[0][0], relationship[0][1]))
                keys.add((relationship[0][2], relationship[0][3]))
        for key in keys:
            entity = key[0]
            column = key[1]
            query = self._find_query_for_entity(entity)
            if query is not None:
                result = self.client.execute(f"""
                    query test_{entity}_uniqueness {{
                        {query}(limit:{self.key_uniqueness_test_size}) {{
                            {column}
                        }}
                    }}""")
                result = list(map(lambda x: x.get(column), result[self.remove_type_names(entity)]))
                unique_result = set(result)
                if self.valid_keys_uniqueness.get(entity) is None:
                    self.valid_keys_uniqueness[entity] = {}
                unique_ratio = len(unique_result) / len(result) if len(result) > 0 else -1
                self.valid_keys_uniqueness[entity][column] = unique_ratio
                if unique_ratio > self.key_uniqueness_test_rate:
                    self.logging.info(f'Added valid key: {key}')
                    self.valid_keys.add(key)
                else:
                    timestamps = self._get_timestamp_field(entity)
                    if timestamps:
                        result = self.client.execute(f"""
                                            query test_{entity}_uniqueness {{
                                                {query}(limit:{self.key_uniqueness_test_size}) {{
                                                    {timestamps[0]}
                                                }}
                                            }}""")
                        result = list(map(lambda x: x.get(timestamps[0]), result[self.remove_type_names(entity)]))
                        unique_result = set(result)
                        unique_ratio = len(unique_result) / len(result) if len(result) > 0 else -1
                        if unique_ratio <= self.key_uniqueness_test_rate:
                            self.logging.info(f'Added valid key: {key}')
                            self.valid_keys.add(key)
                        else:
                            self.logging.info(f'Blacklisted key: {key}')
                    else:
                        self.logging.info(f'Blacklisted key: {key}')
        return

    def _validate_relationships(self):
        new_relationships = []
        for relationship in self.relationships:
            key, name, existing, relationship_type = relationship
            entity1, field1, entity2, field2 = key
            query1 = self._find_query_for_entity(entity1)
            query2 = self._find_query_for_entity(entity2)
            if query1 is not None and query2 is not None:
                if correlation_test.get(entity1 + field1) is None:
                    key1 = self.client.execute(f"""
                        query test_{entity1}_correlation {{
                            {query1}(limit:{self.key_correlation_test_size}) {{
                                {field1}
                            }}
                        }}""")
                    key1 = set(map(lambda x: x.get(field1), key1[self.remove_type_names(entity1)]))
                    correlation_test[entity1 + field1] = key1
                else:
                    key1 = correlation_test[entity1 + field1]

                if correlation_test.get(entity2 + field2) is None:
                    key2 = self.client.execute(f"""
                        query test_{entity2}_correlation {{
                            {query2}(limit:{self.key_correlation_test_size}) {{
                                {field2}
                            }}
                        }}""")
                    key2 = set(map(lambda x: x.get(field2), key2[self.remove_type_names(entity2)]))
                    correlation_test[entity2 + field2] = key2
                else:
                    key2 = correlation_test[entity2 + field2]

                overlap = len(key1 & key2)
                self.logging.info(f'Validated relationship: {relationship}')
                new_relationships.append((
                    key, name, existing, relationship_type,
                    (overlap / len(key1), overlap / len(key2),
                     min(overlap / len(key1), overlap / len(key2)
                         ))))
        self.relationships = new_relationships

    def _get_field_names(self, entity):
        return self.schema.type_map.get(entity).fields.keys()

    def _fix_relationship_name_collisions(self, relationship):
        key, name, existing, relationship_type, correlation, relationship_names = relationship
        forward_rel, forward_rel_type, backward_rel, backward_rel_type = relationship_names
        entity1, field1, entity2, field2 = key
        source, table = self._get_table(name=entity1)
        existing_relationships = [name.lower() for name in self._list_relationships(table) or []]
        single = pluralizer.singular(forward_rel).lower()
        plural = pluralizer.plural(forward_rel).lower()
        if existing == 'existing' or single in existing_relationships or plural in existing_relationships:
            forward_rel = None
        else:
            field_names = [name.lower() for name in self._get_field_names(entity1)]
            if existing == 'ak' or single in field_names or pluralizer.plural(
                    forward_rel).lower() in field_names:
                rel = f'{forward_rel}By{field1}'
                if rel.lower() in field_names:
                    forward_rel = None
                else:
                    forward_rel = rel
        source, table = self._get_table(name=entity2)
        existing_relationships = [name.lower() for name in self._list_relationships(table) or []]
        single = pluralizer.singular(backward_rel).lower()
        plural = pluralizer.plural(backward_rel).lower()
        if single in existing_relationships or plural in existing_relationships:
            backward_rel = None
        else:
            field_names = [name.lower() for name in self._get_field_names(entity2)]
            if existing == 'ak' or single in field_names or pluralizer.plural(
                    backward_rel).lower() in field_names:
                rel = f'{backward_rel}By{field2}'
                if rel.lower() in field_names:
                    backward_rel = None
                else:
                    backward_rel = rel
        return forward_rel, forward_rel_type, backward_rel, backward_rel_type

    def _create_relationship_names(self):
        new_relationships = []
        for relationship in self.relationships:
            key, name, existing, relationship_type, correlation = relationship
            entity1, field1, entity2, field2 = key
            forward, reverse, maximum = correlation
            key1_unique = self.valid_keys_uniqueness.get(entity1).get(field1)
            key2_unique = self.valid_keys_uniqueness.get(entity2).get(field2)
            if maximum > self.key_correlation_test_rate:
                if key1_unique == 1 and key2_unique == 1:
                    relationship_names = (
                        pluralizer.singular(self.remove_type_names(entity2)), 'object',
                        pluralizer.singular(self.remove_type_names(entity1)), 'object')
                elif key2_unique == 1 and key1_unique != 1:
                    relationship_names = (pluralizer.singular(self.remove_type_names(entity2)), 'object',
                                          pluralizer.plural(self.remove_type_names(entity1)), 'array')
                elif key1_unique == 1 and key2_unique != 1:
                    relationship_names = (pluralizer.plural(self.remove_type_names(entity2)), 'array',
                                          pluralizer.singular(self.remove_type_names(entity1)), 'object')
                else:
                    relationship_names = (pluralizer.plural(self.remove_type_names(entity2)), 'array',
                                          pluralizer.plural(self.remove_type_names(entity1)), 'array')
                relationship_names = (
                    cc.make_lower_camel_case(relationship_names[0]), relationship_names[1],
                    cc.make_lower_camel_case(relationship_names[2]), relationship_names[3])
                relationship_names = self._fix_relationship_name_collisions(
                    (key, name, existing, relationship_type, correlation, relationship_names))
                new_relationships.append((key, name, existing, relationship_type, correlation, relationship_names))
        self.relationships = new_relationships

    def _get_column_name(self, entity, name):
        source, table = self._get_table(entity)
        fields = table.get('configuration', {}).get('column_config', {}).items()
        if len(fields) == 0:
            return name
        result = list(map(lambda x: x[0], filter(lambda x: x[1].get('custom_name') == name, fields)))
        if len(result) == 0:
            return name
        return result[0]

    def _update_metadata(self):
        for relationship in self.relationships:
            key, _, _, _, _, relationship_names = relationship
            entity1, field1, entity2, field2 = key
            forward_name, forward_type, reverse_name, reverse_type = relationship_names
            column1 = self._get_column_name(entity1, field1)
            column2 = self._get_column_name(entity2, field2)

            def add_relationship(_entity1, _entity2, _column1, _column2, relation_type, relation_name):
                source, table = self._get_table(_entity1)
                remote_source, remote_table = self._get_table(_entity2)
                if source == remote_source:
                    rels = table.get(f'{relation_type}_relationships') or []
                    if len([found for found in rels if found.get('name') == relation_name]) == 0:
                        if len(rels) == 0:
                            rels = []
                            table[f'{relation_type}_relationships'] = rels
                        rel = {
                            "name": relation_name,
                            "using": {
                                "manual_configuration": {
                                    "column_mapping": {
                                        _column1: _column2
                                    },
                                    "insertion_order": None,
                                    "remote_table": remote_table.get('table')
                                }
                            }
                        }
                        rels.append(rel)
                else:
                    rels = table.get('remote_relationships')
                    if rels is None:
                        rels = []
                        table['remote_relationships'] = rels
                    rel = {
                        "definition": {
                            "to_source": {
                                "field_mapping": {
                                    _column1: _column2
                                },
                                "relationship_type": relation_type,
                                "source": remote_source,
                                "table": remote_table.get('table')
                            }
                        },
                        "name": relation_name
                    }
                    rels.append(rel)

            if forward_name is not None:
                add_relationship(entity1, entity2, column1, column2, forward_type, forward_name)
            if reverse_name is not None:
                add_relationship(entity2, entity1, column2, column1, reverse_type, reverse_name)

    def get_schema_relationships(self):
        """
        Get the relationships between object types in the schema.

        Returns:
            nodes (set): A set of tuples containing the object types and their labels.
            relationships (list): A list of tuples containing the relationship information between object types.
        """
        relationships = []
        nodes = set()
        object_types = self._get_object_types()
        for object_type in object_types:
            object_type_source, object_type_table = self._get_table(name=object_type[0])
            object_type_labels = (object_type[0], object_type_source.get('name'), object_type_table.get('table').get('name'))
            nodes.add((object_type, object_type_labels))
            fields = object_type[1].fields.items()
            for field in fields:
                concrete_type = self._get_concrete_type(field[1].type)
                if is_object_type(concrete_type) and self._check_object_type((concrete_type.name, concrete_type)):
                    concrete_type_source, concrete_type_table = self._get_table(name=concrete_type.name)
                    concrete_type_labels = (
                        concrete_type.name, concrete_type_source.get('name'), concrete_type_table.get('table').get('name'))
                    nodes.add(((concrete_type.name, concrete_type), concrete_type_labels))
                    rel_type = 'array' if self._is_list_type(field[1].type) else 'object'
                    field_parts = field[0].split('By')
                    rel_modifier = field_parts[1] if len(field_parts) > 1 else None
                    rel_name = f'HAS_{pluralizer.plural(cc.make_snake_case(concrete_type.name)).upper()}' \
                        if rel_type == 'array' \
                        else f'HAVE_{pluralizer.singular(cc.make_snake_case(concrete_type.name)).upper()}'
                    if rel_modifier is not None:
                        rel_name += '_BY_' + rel_modifier.upper()
                    relationships.append((
                        object_type,
                        object_type_source,
                        object_type_table,
                        object_type_labels,
                        field,
                        rel_type,
                        rel_name,
                        (concrete_type.name, concrete_type),
                        concrete_type_source,
                        concrete_type_table,
                        concrete_type_labels
                    ))
        return nodes, relationships

    def analyze_relationships(self):
        self.logging.info('Analyzing relationships...')
        tables = self._metadata_tables()
        self.logging.info(f'Found {len(tables)} tables.')
        self.relationships = self._get_existing_relationships(tables) or []
        self.logging.info(f'Found {len(self.relationships)} relationships, existing.')
        self._get_semantic_relationships()
        self.logging.info(f'Found {len(self.relationships)} relationships, existing + semantic.')
        self._get_key_guess_relationships()
        self.logging.info(f'Found {len(self.relationships)} relationships, existing + semantic + key-guess.')
        # validate key uniqueness
        self._validate_keys()
        self.relationships = [relationship for relationship in self.relationships if
                              (relationship[0][0], relationship[0][1]) in self.valid_keys and
                              (relationship[0][2], relationship[0][3]) in self.valid_keys
                              ]
        self.logging.info(f'Found {len(self.relationships)} relationships, existing + semantic + key-guess - bad-keys.')
        # validate relationship correlation
        self._validate_relationships()
        self.logging.info(f'Validated {len(self.relationships)} relationships.')
        # generate relation names
        self._create_relationship_names()
        self.logging.info(f'Finalized {len(self.relationships)} relationships.')
        # add to hasura metadata
        self._update_metadata()
        # write out result
        return self.metadata

    def metadata_to_neo4j(self, uri, username, password, nodes=None, relationships=None):
        """
        Args:
            uri: The URI of the Neo4j database.
            username: The username used for authentication.
            password: The password used for authentication.
            nodes: A list of nodes to be created in the Neo4j database. Each node should be a tuple containing three elements: (fields, node_info, table_info). `fields` is a dictionary containing
        * the field names and their corresponding types. `node_info` is a tuple containing the name, source, and table information of the node. `table_info` is a dictionary containing additional
        * information about the table.
            relationships: A list of relationships to be created in the Neo4j database. Each relationship should be a tuple containing eleven elements: (_, _, _, source_labels, field, _, rel
        *_name, _, _, _, destination_labels). `_` represents unused elements. `source_labels` and `destination_labels` are tuples containing the name, source, and additional information of the
        * source and destination nodes, respectively. `field` is a tuple containing the name and additional information of the field. `rel_name` is the name of the relationship.

        Example usage:

        nodes = [
            ({"field1": "type1", "field2": "type2"}, ("Node1", "Source1", "Table1"), {}),
            ({"field3": "type3", "field4": "type4"}, ("Node2", "Source2", "Table2"), {}),
        ]

        relationships = [
            (_, _, _, ("Source1", "Node1", {}), ("Field1", {}), _, "RELATIONSHIP1", _, _, _, ("Source2", "Node2", {})),
            (_, _, _, ("Source2", "Node2", {}), ("Field2", {}), _, "RELATIONSHIP2", _, _, _, ("Source1", "Node1", {})),
        ]

        metadata_to_neo4j(uri="neo4j://localhost:7687", username="admin", password="password", nodes=nodes, relationships=relationships)
        """
        driver = GraphDatabase.driver(uri, auth=(username, password))

        def create_node(tx, node):
            name, source, table = node[1]
            fields = {"_name": name, "_source": source, "_table": table}

            for field in node[0][1].fields.items():
                concrete_type = self._get_concrete_type(field[1].type)
                field_name = field[0] if field[0] != 'name' else 'name_'
                if not is_object_type(concrete_type):
                    fields[field_name] = concrete_type.name
            tx.run(f"CREATE (a:{name}:{source}:DataProduct) SET a = $fields RETURN a",
                   fields=fields)

        def create_relationship(tx, relationship):
            _, _, _, source_labels, field, _, rel_name, _, _, _, destination_labels = relationship
            field_name, _ = field
            source_name, source_source, _ = source_labels
            dest_name, dest_source, _ = destination_labels
            tx.run(f"""
                MATCH (a:{source_name}:{source_source}:DataProduct), (b:{dest_name}:{dest_source}:DataProduct)
                CREATE (a)-[:{rel_name} {{relationshipName: $field_name}}]->(b)
            """, field_name=field_name)

        def remove_nodes(tx):
            tx.run(f"MATCH (n:DataProduct) DETACH DELETE n")

        with driver.session() as session:
            session.write_transaction(remove_nodes)
            for node in nodes:
                session.write_transaction(create_node, node)
            for relationship in relationships:
                session.write_transaction(create_relationship, relationship)

        driver.close()
