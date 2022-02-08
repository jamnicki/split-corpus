import os
import json

from tests import TestRunner
from split import split_file
from utils import clear_folder


def split_task():
    INPUT_FOLDER = "./tematy"
    OUTPUT_FOLDER = "./out"

    if os.path.exists(OUTPUT_FOLDER) and os.listdir(OUTPUT_FOLDER):
        clear_folder(OUTPUT_FOLDER)

    chunks_dict = {}
    for test_file in os.listdir(INPUT_FOLDER):
        file_path = os.path.join(INPUT_FOLDER, test_file)

        output_files = split_file(
            source_path=file_path,
            destination_path=OUTPUT_FOLDER,
            file_name=test_file,
            chunk_size=os.path.getsize(file_path) / 5
        )
        output_file_paths = [
            os.path.join(OUTPUT_FOLDER, f) for f in output_files
        ]
        chunks_dict[file_path] = output_file_paths

    return chunks_dict


def run_tasks():
    split_info = split_task()
    with open("split_info.json", "w") as split_info_f:
        json.dump(split_info, split_info_f, indent=2)


def run_unittests():
    test_runner = TestRunner()
    results = test_runner.run()
    if results.failures or results.errors:
        exit()


if __name__ == "__main__":
    run_tasks()
    run_unittests()
