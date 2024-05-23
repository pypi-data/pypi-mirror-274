import unittest


class TestPlyReader(unittest.TestCase):
    def test_import(self):
        module = __import__("apeboiy.ply")
        self.assertIsNotNone(module)

    def test_import_reader(self):
        try:
            from apeboiy.ply import Reader
        except ImportError:
            self.fail("Failed to import Reader from ply module")

    def test_reader_class(self):
        from apeboiy.ply import Reader
        reader = Reader("file.ply")
        self.assertIsNotNone(reader)


if __name__ == '__main__':
    unittest.main()
