import unittest
from coben.coben import parse_hierarchy, format_puml_content, extract_uml_content

class TestCoben(unittest.TestCase):

    def test_parse_hierarchy(self):
        uml_content = """
        class A {
        }
        class B {
        }
        """
        hierarchy = parse_hierarchy(uml_content)
        expected = {'A': {}, 'B': {}}
        self.assertEqual(hierarchy, expected)

    def test_format_puml_content(self):
        puml_content = """
        class A {
        }
        """
        formatted_content = format_puml_content(puml_content)
        expected = "class A {\n}"
        self.assertEqual(formatted_content.strip(), expected.strip())

    def test_extract_uml_content(self):
        diff_content = """
        ```puml
        class A {
        }
        ```
        """
        uml_content = extract_uml_content(diff_content)
        expected = "class A {\n}"
        self.assertEqual(uml_content.strip(), expected.strip())

if __name__ == '__main__':
    unittest.main()
