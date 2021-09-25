import json
from split_task import split_task
from tests import TestRunner


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
