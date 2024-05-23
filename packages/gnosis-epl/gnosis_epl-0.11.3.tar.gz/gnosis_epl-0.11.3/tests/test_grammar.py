import unittest
from gnosis_epl.main import QueryParser
from gnosis_epl.grammar.epl_listener import GnosisEPLParserException


class TestGnosisEPLGrammar(unittest.TestCase):

    def setUp(self):
        self.parser = QueryParser()

    def tearDown(self):
        pass

    def test_query_name_is_correctly_parsed(self):
        query_text = """REGISTER QUERY my_first_query
            OUTPUT K_GRAPH_JSON
            CONTENT ObjectDetection, ColorDetection, SpeachToText, TextLanguageModel
            MATCH (c1:Car {color:'blue'}) , (c2:Car {color:'white'})
            FROM test
            WITHIN TUMBLING_COUNT_WINDOW(2)
            RETURN *"""
        query_dict = self.parser.parse(query_text)
        self.assertIn('name', query_dict)
        self.assertEqual(query_dict['name'], 'my_first_query')

    def test_query_name_with_num_is_correctly_parsed(self):
        query_text = """REGISTER QUERY my_first_query000
            OUTPUT K_GRAPH_JSON
            CONTENT ObjectDetection, ColorDetection
            MATCH (c1:Car {color:'blue'}) , (c2:Car {color:'white'})
            FROM test
            WITHIN TUMBLING_COUNT_WINDOW(2)
            RETURN *"""
        query_dict = self.parser.parse(query_text)
        self.assertIn('name', query_dict)
        self.assertEqual(query_dict['name'], 'my_first_query000')

    def test_query_name_exception_when_invalid(self):
        query_text = """REGISTER QUERY Invalid Query Name
            OUTPUT K_GRAPH_JSON
            CONTENT ObjectDetection, ColorDetection
            MATCH (c1:Car {color:'blue'}) , (c2:Car {color:'white'})
            FROM test
            WITHIN TUMBLING_COUNT_WINDOW(2)
            RETURN *"""

        with self.assertRaises(GnosisEPLParserException):
            query_dict = self.parser.parse(query_text)

    def test_output_with_single_output(self):
        query_text = """REGISTER QUERY my_first_query000
            OUTPUT K_GRAPH_JSON
            CONTENT ObjectDetection, ColorDetection
            MATCH (c1:Car {color:'blue'}) , (c2:Car {color:'white'})
            FROM test
            WITHIN TUMBLING_COUNT_WINDOW(2)
            RETURN *"""
        query_dict = self.parser.parse(query_text)
        self.assertIn('output', query_dict)
        self.assertListEqual(query_dict['output'], ['K_GRAPH_JSON'])

    def test_output_with_multiple_output(self):
        query_text = """REGISTER QUERY my_first_query000
            OUTPUT K_GRAPH_JSON, VIDEO_STREAM
            CONTENT ObjectDetection, ColorDetection
            MATCH (c1:Car {color:'blue'}) , (c2:Car {color:'white'})
            FROM test
            WITHIN TUMBLING_COUNT_WINDOW(2)
            RETURN *"""
        query_dict = self.parser.parse(query_text)
        self.assertIn('output', query_dict)
        self.assertListEqual(query_dict['output'], ['K_GRAPH_JSON', 'VIDEO_STREAM'])

    def test_from_is_correctly_parsed_when_single_value(self):
        query_text = """REGISTER QUERY my_first_query
            OUTPUT K_GRAPH_JSON
            CONTENT ObjectDetection, ColorDetection
            MATCH (c1:Car {color:'blue'}) , (c2:Car {color:'white'})
            FROM test
            WITHIN TUMBLING_COUNT_WINDOW(2)
            RETURN *"""
        query_dict = self.parser.parse(query_text)
        self.assertIn('from', query_dict)
        self.assertEqual(query_dict['from'], ['test'])

    def test_from_is_correctly_parsed_when_multi_value(self):
        query_text = """REGISTER QUERY my_first_query
            OUTPUT K_GRAPH_JSON
            CONTENT ObjectDetection, ColorDetection
            MATCH (c1:Car {color:'blue'}) , (c2:Car {color:'white'})
            FROM test, test2
            WITHIN TUMBLING_COUNT_WINDOW(2)
            RETURN *"""
        query_dict = self.parser.parse(query_text)
        self.assertIn('from', query_dict)
        self.assertEqual(query_dict['from'], ['test', 'test2'])

    def test_from_is_correctly_parsed_when_asterisk_value(self):
        query_text = """REGISTER QUERY my_first_query
            OUTPUT K_GRAPH_JSON
            CONTENT ObjectDetection, ColorDetection
            MATCH (c1:Car {color:'blue'}) , (c2:Car {color:'white'})
            FROM *
            WITHIN TUMBLING_COUNT_WINDOW(2)
            RETURN *"""
        query_dict = self.parser.parse(query_text)
        self.assertIn('from', query_dict)
        self.assertEqual(query_dict['from'], ['*'])

    def test_content_is_correctly_parsed_when_single_value(self):
        query_text = """REGISTER QUERY my_first_query
            OUTPUT K_GRAPH_JSON
            CONTENT ObjectDetection
            MATCH (c1:Car {color:'blue'}) , (c2:Car {color:'white'})
            FROM *
            WITHIN TUMBLING_COUNT_WINDOW(2)
            RETURN *"""
        query_dict = self.parser.parse(query_text)
        self.assertIn('content', query_dict)
        self.assertEqual(query_dict['content'], ['ObjectDetection'])

    def test_content_is_correctly_parsed_when_multiple_values(self):
        query_text = """REGISTER QUERY my_first_query
            OUTPUT K_GRAPH_JSON
            CONTENT ObjectDetection, ColorDetection
            MATCH (c1:Car {color:'blue'}) , (c2:Car {color:'white'})
            FROM *
            WITHIN TUMBLING_COUNT_WINDOW(2)
            RETURN *"""
        query_dict = self.parser.parse(query_text)
        self.assertIn('content', query_dict)
        self.assertEqual(query_dict['content'], ['ObjectDetection', 'ColorDetection'])

    def test_content_is_correctly_parsed_when_not_present(self):
        query_text = """REGISTER QUERY my_first_query
            OUTPUT K_GRAPH_JSON
            MATCH (c1:Car {color:'blue'}) , (c2:Car {color:'white'})
            FROM *
            WITHIN TUMBLING_COUNT_WINDOW(2)
            RETURN *"""
        query_dict = self.parser.parse(query_text)
        self.assertNotIn('content', query_dict)

    def test_window_is_correctly_parsed_with_single_arg(self):
        query_text = """REGISTER QUERY my_first_query
            OUTPUT K_GRAPH_JSON
            CONTENT ObjectDetection, ColorDetection
            MATCH (c1:Car {color:'blue'}) , (c2:Car {color:'white'})
            FROM *
            WITHIN TUMBLING_COUNT_WINDOW(2)
            RETURN *"""
        query_dict = self.parser.parse(query_text)
        excepted_dict = {
            'window_type': 'TUMBLING_COUNT_WINDOW',
            'args': [2]
        }
        self.assertIn('window', query_dict)
        self.assertEqual(query_dict['window'], excepted_dict)

    def test_window_is_correctly_parsed_with_multiple_arg(self):
        query_text = """REGISTER QUERY my_first_query
            OUTPUT K_GRAPH_JSON
            CONTENT ObjectDetection, ColorDetection
            MATCH (c1:Car {color:'blue'}) , (c2:Car {color:'white'})
            FROM *
            WITHIN TUMBLING_COUNT_WINDOW(2, 1)
            RETURN *"""
        query_dict = self.parser.parse(query_text)
        excepted_dict = {
            'window_type': 'TUMBLING_COUNT_WINDOW',
            'args': [2, 1]
        }
        self.assertIn('window', query_dict)
        self.assertEqual(query_dict['window'], excepted_dict)

    def test_window_is_correctly_parsed_with_mixed_type_arg(self):
        query_text = """REGISTER QUERY my_first_query
            OUTPUT K_GRAPH_JSON
            CONTENT ObjectDetection, ColorDetection
            MATCH (c1:Car {color:'blue'}) , (c2:Car {color:'white'})
            FROM *
            WITHIN TUMBLING_COUNT_WINDOW(a1b2c, 1)
            RETURN *"""
        query_dict = self.parser.parse(query_text)
        excepted_dict = {
            'window_type': 'TUMBLING_COUNT_WINDOW',
            'args': ['a1b2c', 1]
        }
        self.assertIn('window', query_dict)
        self.assertEqual(query_dict['window'], excepted_dict)

    def test_entire_match_with_is_correctly_parsed_when_obj_not_defined(self):
        query_text = """REGISTER QUERY my_first_query
            OUTPUT K_GRAPH_JSON
            CONTENT ObjectDetection, ColorDetection
            MATCH (:Car)
            FROM *
            WITHIN TUMBLING_COUNT_WINDOW(a1b2c, 1)
            RETURN *"""
        query_dict = self.parser.parse(query_text)
        excepted_str = 'MATCH (:Car)'
        self.assertIn('match', query_dict)
        self.assertEqual(query_dict['match'], excepted_str)

    def test_entire_match_with_is_correctly_parsed_when_obj_is_defined(self):
        query_text = """REGISTER QUERY my_first_query
            OUTPUT K_GRAPH_JSON
            CONTENT ObjectDetection, ColorDetection
            MATCH (c:Car)
            FROM *
            WITHIN TUMBLING_COUNT_WINDOW(a1b2c, 1)
            RETURN *"""
        query_dict = self.parser.parse(query_text)
        excepted_str = 'MATCH (c:Car)'
        self.assertIn('match', query_dict)
        self.assertEqual(query_dict['match'], excepted_str)

    def test_entire_match_with_is_correctly_parsed_when_non_related_matches(self):
        query_text = """REGISTER QUERY my_first_query
            OUTPUT K_GRAPH_JSON
            CONTENT ObjectDetection, ColorDetection
            MATCH (:Car), (:Person)
            FROM *
            WITHIN TUMBLING_COUNT_WINDOW(a1b2c, 1)
            RETURN *"""
        query_dict = self.parser.parse(query_text)
        excepted_str = 'MATCH (:Car), (:Person)'
        self.assertIn('match', query_dict)
        self.assertEqual(query_dict['match'], excepted_str)

    def test_entire_match_with_is_correctly_parsed_when_single_left_relation(self):
        query_text = """REGISTER QUERY my_first_query
            OUTPUT K_GRAPH_JSON
            CONTENT ObjectDetection, ColorDetection
            MATCH (:Car)-->(:Person)
            FROM *
            WITHIN TUMBLING_COUNT_WINDOW(a1b2c, 1)
            RETURN *"""
        query_dict = self.parser.parse(query_text)
        excepted_str = 'MATCH (:Car)-->(:Person)'
        self.assertIn('match', query_dict)
        self.assertEqual(query_dict['match'], excepted_str)

    def test_entire_match_with_is_correctly_parsed_when_single_right_relation(self):
        query_text = """REGISTER QUERY my_first_query
            OUTPUT K_GRAPH_JSON
            CONTENT ObjectDetection, ColorDetection
            MATCH (:Car)<--(:Person)
            FROM *
            WITHIN TUMBLING_COUNT_WINDOW(a1b2c, 1)
            RETURN *"""
        query_dict = self.parser.parse(query_text)
        excepted_str = 'MATCH (:Car)<--(:Person)'
        self.assertIn('match', query_dict)
        self.assertEqual(query_dict['match'], excepted_str)

    def test_entire_match_with_is_correctly_parsed_when_single_gen_relation(self):
        query_text = """REGISTER QUERY my_first_query
            OUTPUT K_GRAPH_JSON
            CONTENT ObjectDetection, ColorDetection
            MATCH (:Car)--(:Person)
            FROM *
            WITHIN TUMBLING_COUNT_WINDOW(a1b2c, 1)
            RETURN *"""
        query_dict = self.parser.parse(query_text)
        excepted_str = 'MATCH (:Car)--(:Person)'
        self.assertIn('match', query_dict)
        self.assertEqual(query_dict['match'], excepted_str)

    def test_entire_match_with_is_correctly_parsed_when_single_relation_detailed(self):
        query_text = """REGISTER QUERY my_first_query
            OUTPUT K_GRAPH_JSON
            CONTENT ObjectDetection, ColorDetection
            MATCH (:Car)-[:something]-(:Person)
            FROM *
            WITHIN TUMBLING_COUNT_WINDOW(a1b2c, 1)
            RETURN *"""
        query_dict = self.parser.parse(query_text)
        excepted_str = 'MATCH (:Car)-[:something]-(:Person)'
        self.assertIn('match', query_dict)
        self.assertEqual(query_dict['match'], excepted_str)

    def test_entire_match_with_is_correctly_parsed_when_single_relation_detailed_label(self):
        query_text = """REGISTER QUERY my_first_query
            OUTPUT K_GRAPH_JSON
            CONTENT ObjectDetection, ColorDetection
            MATCH (:Car)-[r:something]-(:Person)
            FROM *
            WITHIN TUMBLING_COUNT_WINDOW(a1b2c, 1)
            RETURN *"""
        query_dict = self.parser.parse(query_text)
        excepted_str = 'MATCH (:Car)-[r:something]-(:Person)'
        self.assertIn('match', query_dict)
        self.assertEqual(query_dict['match'], excepted_str)

    def test_entire_match_with_is_correctly_parsed_when_single_relation_detailed_attrs(self):
        query_text = """REGISTER QUERY my_first_query
            OUTPUT K_GRAPH_JSON
            CONTENT ObjectDetection, ColorDetection
            MATCH (:Car)-[:something {something:123, abc:"test"}]-(:Person)
            FROM *
            WITHIN TUMBLING_COUNT_WINDOW(a1b2c, 1)
            RETURN *"""
        query_dict = self.parser.parse(query_text)
        excepted_str = 'MATCH (:Car)-[:something {something:123, abc:"test"}]-(:Person)'
        self.assertIn('match', query_dict)
        self.assertEqual(query_dict['match'], excepted_str)

    def test_entire_match_with_is_correctly_parsed_when_single_relation_detailed_attrs_label_node(self):
        query_text = """REGISTER QUERY my_first_query
            OUTPUT K_GRAPH_JSON
            CONTENT ObjectDetection, ColorDetection
            MATCH (c:Car)-[:something {something:123, abc:"test"}]-(p:Person)
            FROM *
            WITHIN TUMBLING_COUNT_WINDOW(a1b2c, 1)
            RETURN *"""
        query_dict = self.parser.parse(query_text)
        excepted_str = 'MATCH (c:Car)-[:something {something:123, abc:"test"}]-(p:Person)'
        self.assertIn('match', query_dict)
        self.assertEqual(query_dict['match'], excepted_str)

    def test_entire_match_with_is_correctly_parsed_when_single_relation_detailed_attrs_label_node_directed_right(self):
        query_text = """REGISTER QUERY my_first_query
            OUTPUT K_GRAPH_JSON
            CONTENT ObjectDetection, ColorDetection
            MATCH (c:Car)-[:something {something:123, abc:"test"}]->(p:Person)
            FROM *
            WITHIN TUMBLING_COUNT_WINDOW(a1b2c, 1)
            RETURN *"""
        query_dict = self.parser.parse(query_text)
        excepted_str = 'MATCH (c:Car)-[:something {something:123, abc:"test"}]->(p:Person)'
        self.assertIn('match', query_dict)
        self.assertEqual(query_dict['match'], excepted_str)

    def test_entire_match_with_is_correctly_parsed_when_single_relation_detailed_attrs_label_node_directed_left(self):
        query_text = """REGISTER QUERY my_first_query
            OUTPUT K_GRAPH_JSON
            CONTENT ObjectDetection, ColorDetection
            MATCH (c:Car)<-[:something {something:123, abc:"test"}]-(p:Person)
            FROM *
            WITHIN TUMBLING_COUNT_WINDOW(a1b2c, 1)
            RETURN *"""
        query_dict = self.parser.parse(query_text)
        excepted_str = 'MATCH (c:Car)<-[:something {something:123, abc:"test"}]-(p:Person)'
        self.assertIn('match', query_dict)
        self.assertEqual(query_dict['match'], excepted_str)

    def test_entire_match_with_is_correctly_parsed_when_multiple_relation_gen(self):
        query_text = """REGISTER QUERY my_first_query
            OUTPUT K_GRAPH_JSON
            CONTENT ObjectDetection, ColorDetection
            MATCH (c:Car)--(p:Person)--(ct:Cat)
            FROM *
            WITHIN TUMBLING_COUNT_WINDOW(a1b2c, 1)
            RETURN *"""
        query_dict = self.parser.parse(query_text)
        excepted_str = 'MATCH (c:Car)--(p:Person)--(ct:Cat)'
        self.assertIn('match', query_dict)
        self.assertEqual(query_dict['match'], excepted_str)

    def test_entire_match_with_is_correctly_parsed_when_multiple_relation_attrs_label_directed(self):
        query_text = """REGISTER QUERY my_first_query
            OUTPUT K_GRAPH_JSON
            CONTENT ObjectDetection, ColorDetection
            MATCH (c:Car)-->(p:Person)<-[r:Owns]-(ct:Cat)
            FROM *
            WITHIN TUMBLING_COUNT_WINDOW(a1b2c, 1)
            RETURN *"""
        query_dict = self.parser.parse(query_text)
        excepted_str = 'MATCH (c:Car)-->(p:Person)<-[r:Owns]-(ct:Cat)'
        self.assertIn('match', query_dict)
        self.assertEqual(query_dict['match'], excepted_str)

    def test_entire_optional_match_with_is_correctly_parsed_when_multiple_relation_attrs_label_directed(self):
        query_text = """REGISTER QUERY my_first_query
            OUTPUT K_GRAPH_JSON
            CONTENT ObjectDetection, ColorDetection
            MATCH (c:Car)-->(p:Person)<-[r:Owns]-(ct:Cat)<--(p)
            OPTIONAL MATCH (c)-->(x)
            FROM *
            WITHIN TUMBLING_COUNT_WINDOW(a1b2c, 1)
            RETURN *"""
        query_dict = self.parser.parse(query_text)
        excepted_str = 'MATCH (c:Car)-->(p:Person)<-[r:Owns]-(ct:Cat)<--(p)'
        excepted_optional_str = 'OPTIONAL MATCH (c)-->(x)'
        self.assertIn('match', query_dict)
        self.assertEqual(query_dict['match'], excepted_str)
        self.assertIn('optional_match', query_dict)
        self.assertEqual(query_dict['optional_match'], excepted_optional_str)

    def test_entire_where_single(self):
        query_text = """REGISTER QUERY my_first_query
            OUTPUT K_GRAPH_JSON
            CONTENT ObjectDetection, ColorDetection
            MATCH (c:Car)-->(p:Person)<-[r:Owns]-(ct:Cat)<--(p)
            OPTIONAL MATCH (c)-->(x)
            WHERE c.color = "blue"
            FROM *
            WITHIN TUMBLING_COUNT_WINDOW(a1b2c, 1)
            RETURN *"""
        query_dict = self.parser.parse(query_text)
        excepted_str = 'WHERE c.color = "blue"'
        self.assertIn('where', query_dict)
        self.assertEqual(query_dict['where'], excepted_str)

    def test_entire_where_multiple_with_and(self):
        query_text = """REGISTER QUERY my_first_query
            OUTPUT K_GRAPH_JSON
            CONTENT ObjectDetection, ColorDetection
            MATCH (c:Car)-->(p:Person)<-[r:Owns]-(ct:Cat)<--(p)
            OPTIONAL MATCH (c)-->(x)
            WHERE c.color = "blue" AND p.age = 23
            FROM *
            WITHIN TUMBLING_COUNT_WINDOW(a1b2c, 1)
            RETURN *"""
        query_dict = self.parser.parse(query_text)
        excepted_str = 'WHERE c.color = "blue" AND p.age = 23'
        self.assertIn('where', query_dict)
        self.assertEqual(query_dict['where'], excepted_str)

    def test_entire_where_multiple_with_or(self):
        query_text = """REGISTER QUERY my_first_query
            OUTPUT K_GRAPH_JSON
            CONTENT ObjectDetection, ColorDetection
            MATCH (c:Car)-->(p:Person)<-[r:Owns]-(ct:Cat)<--(p)
            OPTIONAL MATCH (c)-->(x)
            WHERE c.color = "blue" OR p.age = 23
            FROM *
            WITHIN TUMBLING_COUNT_WINDOW(a1b2c, 1)
            RETURN *"""
        query_dict = self.parser.parse(query_text)
        excepted_str = 'WHERE c.color = "blue" OR p.age = 23'
        self.assertIn('where', query_dict)
        self.assertEqual(query_dict['where'], excepted_str)

    def test_entire_where_single_lesser_than(self):
        query_text = """REGISTER QUERY my_first_query
            OUTPUT K_GRAPH_JSON
            CONTENT ObjectDetection, ColorDetection
            MATCH (c:Car)-->(p:Person)<-[r:Owns]-(ct:Cat)<--(p)
            OPTIONAL MATCH (c)-->(x)
            WHERE p.age < 23
            FROM *
            WITHIN TUMBLING_COUNT_WINDOW(a1b2c, 1)
            RETURN *"""
        query_dict = self.parser.parse(query_text)
        excepted_str = 'WHERE p.age < 23'
        self.assertIn('where', query_dict)
        self.assertEqual(query_dict['where'], excepted_str)

    def test_entire_where_single_lesser_than_eq(self):
        query_text = """REGISTER QUERY my_first_query
            OUTPUT K_GRAPH_JSON
            CONTENT ObjectDetection, ColorDetection
            MATCH (c:Car)-->(p:Person)<-[r:Owns]-(ct:Cat)<--(p)
            OPTIONAL MATCH (c)-->(x)
            WHERE p.age <= 23
            FROM *
            WITHIN TUMBLING_COUNT_WINDOW(a1b2c, 1)
            RETURN *"""
        query_dict = self.parser.parse(query_text)
        excepted_str = 'WHERE p.age <= 23'
        self.assertIn('where', query_dict)
        self.assertEqual(query_dict['where'], excepted_str)

    def test_entire_where_single_greater_than(self):
        query_text = """REGISTER QUERY my_first_query
            OUTPUT K_GRAPH_JSON
            CONTENT ObjectDetection, ColorDetection
            MATCH (c:Car)-->(p:Person)<-[r:Owns]-(ct:Cat)<--(p)
            OPTIONAL MATCH (c)-->(x)
            WHERE p.age > 23
            FROM *
            WITHIN TUMBLING_COUNT_WINDOW(a1b2c, 1)
            RETURN *"""
        query_dict = self.parser.parse(query_text)
        excepted_str = 'WHERE p.age > 23'
        self.assertIn('where', query_dict)
        self.assertEqual(query_dict['where'], excepted_str)

    def test_entire_where_single_greater_than_eq(self):
        query_text = """REGISTER QUERY my_first_query
            OUTPUT K_GRAPH_JSON
            CONTENT ObjectDetection, ColorDetection
            MATCH (c:Car)-->(p:Person)<-[r:Owns]-(ct:Cat)<--(p)
            OPTIONAL MATCH (c)-->(x)
            WHERE p.age >= 23
            FROM *
            WITHIN TUMBLING_COUNT_WINDOW(a1b2c, 1)
            RETURN *"""
        query_dict = self.parser.parse(query_text)
        excepted_str = 'WHERE p.age >= 23'
        self.assertIn('where', query_dict)
        self.assertEqual(query_dict['where'], excepted_str)

    def test_entire_where_single_diff(self):
        query_text = """REGISTER QUERY my_first_query
            OUTPUT K_GRAPH_JSON
            CONTENT ObjectDetection, ColorDetection
            MATCH (c:Car)-->(p:Person)<-[r:Owns]-(ct:Cat)<--(p)
            OPTIONAL MATCH (c)-->(x)
            WHERE p.age <> 23
            FROM *
            WITHIN TUMBLING_COUNT_WINDOW(a1b2c, 1)
            RETURN *"""
        query_dict = self.parser.parse(query_text)
        excepted_str = 'WHERE p.age <> 23'
        self.assertIn('where', query_dict)
        self.assertEqual(query_dict['where'], excepted_str)

    def test_entire_where_compare_nodes(self):
        query_text = """REGISTER QUERY my_first_query
            OUTPUT K_GRAPH_JSON
            CONTENT ObjectDetection, ColorDetection
            MATCH (c:Car)-->(p1:Person)<-[r:Owns]-(ct:Cat)<--(p)
            OPTIONAL MATCH (c)-->(x)
            WHERE p1.age <> ct.age
            FROM *
            WITHIN TUMBLING_COUNT_WINDOW(a1b2c, 1)
            RETURN *"""
        query_dict = self.parser.parse(query_text)
        excepted_str = 'WHERE p1.age <> ct.age'
        self.assertIn('where', query_dict)
        self.assertEqual(query_dict['where'], excepted_str)

    def test_simple_query(self):
        query_text = (
            "REGISTER QUERY my_first_query "
            "OUTPUT K_GRAPH_JSON "
            "CONTENT ObjectDetection "
            "MATCH (c:Car)--(p:Person) "
            "FROM publisher1 "
            "WITHIN TUMBLING_COUNT_WINDOW(1) "
            "RETURN *"
        )
        query_dict = self.parser.parse(query_text)
        excepted_str = 'MATCH (c:Car)--(p:Person)'
        self.assertIn('match', query_dict)
        self.assertEqual(query_dict['match'], excepted_str)

    def test_entire_ret_simple(self):
        query_text = (
            "REGISTER QUERY my_first_query "
            "OUTPUT K_GRAPH_JSON "
            "CONTENT ObjectDetection "
            "MATCH (c:Car)--(p:Person) "
            "FROM publisher1 "
            "WITHIN TUMBLING_COUNT_WINDOW(1) "
            "RETURN c"
        )
        query_dict = self.parser.parse(query_text)
        excepted_str = 'RETURN c'
        self.assertIn('ret', query_dict)
        self.assertEqual(query_dict['ret'], excepted_str)

    def test_entire_ret_simple_attr(self):
        query_text = (
            "REGISTER QUERY my_first_query "
            "OUTPUT K_GRAPH_JSON "
            "CONTENT ObjectDetection "
            "MATCH (c:Car)--(p:Person) "
            "FROM publisher1 "
            "WITHIN TUMBLING_COUNT_WINDOW(1) "
            "RETURN c.color"
        )
        query_dict = self.parser.parse(query_text)
        excepted_str = 'RETURN c.color'
        self.assertIn('ret', query_dict)
        self.assertEqual(query_dict['ret'], excepted_str)

    def test_entire_ret_mult_attr(self):
        query_text = (
            "REGISTER QUERY my_first_query "
            "OUTPUT K_GRAPH_JSON "
            "CONTENT ObjectDetection "
            "MATCH (c:Car)--(p:Person) "
            "FROM publisher1 "
            "WITHIN TUMBLING_COUNT_WINDOW(1) "
            "RETURN c.color, p"
        )
        query_dict = self.parser.parse(query_text)
        excepted_str = 'RETURN c.color, p'
        self.assertIn('ret', query_dict)
        self.assertEqual(query_dict['ret'], excepted_str)

    def test_entire_ret_mult_attr2(self):
        query_text = (
            "REGISTER QUERY my_first_query "
            "OUTPUT K_GRAPH_JSON "
            "CONTENT ObjectDetection "
            "MATCH (c:Car)--(p:Person) "
            "FROM publisher1 "
            "WITHIN TUMBLING_COUNT_WINDOW(1) "
            "RETURN c.color, p.name"
        )
        query_dict = self.parser.parse(query_text)
        excepted_str = 'RETURN c.color, p.name'
        self.assertIn('ret', query_dict)
        self.assertEqual(query_dict['ret'], excepted_str)

    def test_entire_ret_asterisk(self):
        query_text = (
            "REGISTER QUERY my_first_query "
            "OUTPUT K_GRAPH_JSON "
            "CONTENT ObjectDetection "
            "MATCH (c:Car)--(p:Person) "
            "FROM publisher1 "
            "WITHIN TUMBLING_COUNT_WINDOW(1) "
            "RETURN *"
        )
        query_dict = self.parser.parse(query_text)
        excepted_str = 'RETURN *'
        self.assertIn('ret', query_dict)
        self.assertEqual(query_dict['ret'], excepted_str)

    def test_entire_ret_complex_aggr(self):
        query_text = (
            "REGISTER QUERY my_first_query "
            "OUTPUT K_GRAPH_JSON "
            "CONTENT ObjectDetection "
            "MATCH (c:Car)--(p:Person) "
            "FROM publisher1 "
            "WITHIN TUMBLING_COUNT_WINDOW(1) "
            "RETURN count(distinct p) as PersonCount, p as People"
        )
        query_dict = self.parser.parse(query_text)
        excepted_str = 'RETURN count(distinct p) as PersonCount, p as People'
        self.assertIn('ret', query_dict)
        self.assertEqual(query_dict['ret'], excepted_str)

    def test_entire_where_with_list_attributes(self):
        query_text = (
            "REGISTER QUERY my_first_query "
            "OUTPUT K_GRAPH_JSON "
            "CONTENT ObjectDetection "
            "MATCH (p:person), (p2:person) "
            "WHERE p.bounding_box[2] < p2.bounding_box[0] "
            "FROM publisher1 "
            "WITHIN TUMBLING_COUNT_WINDOW(1) "
            "RETURN *"
        )
        query_dict = self.parser.parse(query_text)
        excepted_str = 'WHERE p.bounding_box[2] < p2.bounding_box[0]'
        self.assertIn('where', query_dict)
        self.assertEqual(query_dict['where'], excepted_str)

    def test_parsed_with_qos_statements_single_metric_num(self):
        query_text = (
            "REGISTER QUERY my_first_query "
            "OUTPUT K_GRAPH_JSON "
            "CONTENT ObjectDetection "
            "MATCH (p:person), (p2:person) "
            "WHERE p.bounding_box[2] < p2.bounding_box[0] "
            "FROM publisher1 "
            "WITHIN TUMBLING_COUNT_WINDOW(1) "
            "WITH_QOS accuracy = 123 "
            "RETURN *"
        )
        query_dict = self.parser.parse(query_text)
        expected_dict = {
            'accuracy': 123,
        }
        self.assertIn('qos_policies', query_dict)
        self.assertDictEqual(query_dict['qos_policies'], expected_dict)

    def test_parsed_with_qos_statements_single_metric_str(self):
        query_text = (
            "REGISTER QUERY my_first_query "
            "OUTPUT K_GRAPH_JSON "
            "CONTENT ObjectDetection "
            "MATCH (p:person), (p2:person) "
            "WHERE p.bounding_box[2] < p2.bounding_box[0] "
            "FROM publisher1 "
            "WITHIN TUMBLING_COUNT_WINDOW(1) "
            "WITH_QOS accuracy = \"min mean max\" "
            "RETURN *"
        )
        query_dict = self.parser.parse(query_text)
        expected_dict = {
            'accuracy': 'min mean max',
        }
        self.assertIn('qos_policies', query_dict)
        self.assertDictEqual(query_dict['qos_policies'], expected_dict)

    def test_parsed_with_qos_statements_multiple_metrics(self):
        query_text = (
            "REGISTER QUERY my_first_query "
            "OUTPUT K_GRAPH_JSON "
            "CONTENT ObjectDetection "
            "MATCH (p:person), (p2:person) "
            "WHERE p.bounding_box[2] < p2.bounding_box[0] "
            "FROM publisher1 "
            "WITHIN TUMBLING_COUNT_WINDOW(1) "
            "WITH_QOS accuracy = \"min mean max\", energy = 123, latency = 'average' "
            "RETURN *"
        )
        query_dict = self.parser.parse(query_text)
        expected_dict = {
            'accuracy': 'min mean max',
            'energy': 123.0,
            'latency': 'average'
        }
        self.assertIn('qos_policies', query_dict)
        self.assertDictEqual(query_dict['qos_policies'], expected_dict)
