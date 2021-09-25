import json
from unittest import TestCase, TestSuite, TextTestRunner, defaultTestLoader


class TestRunner:

    def __init__(self):
        self.runner = TextTestRunner(verbosity=2)

    def run(self):
        test_suite = TestSuite(
            tests=[
                defaultTestLoader.loadTestsFromTestCase(TestSplit),
            ]
        )
        return self.runner.run(test_suite)


class TestSplit(TestCase):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)
        with open("split_info.json", "r") as split_info_f:
            self.split_info = json.load(split_info_f)

    def test_data_equality(self):
        for parent_file_path, chunk_paths in self.split_info.items():
            with open(parent_file_path, "r") as parent_file:
                parent_data = parent_file.read()

            chunks_data = ""
            for chunk_path in chunk_paths:
                with open(chunk_path, "r") as chunk_file:
                    chunks_data += chunk_file.read()

            err_msg = f"\n\n{parent_file_path}: missing data in chunks!"
            self.assertEqual(parent_data, chunks_data, msg=err_msg)

    def test_chunks_size_std_deviation(self):
        pass
