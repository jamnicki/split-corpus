import os
from main import split_corpus


def clear_folder(relative_path: str):
    clear_command = f'rm {relative_path}/*'
    decision = input(f"Executing:\n\t> {clear_command}\n\nProceed (y/n)?")
    if decision.lower() == 'y':
        os.system(clear_command)
        print(f'Clearing {relative_path}...\n')


def split_task():
    INPUT_FOLDER = '/media/jamnicki/HDD/__Test_input/tematy'
    OUTPUT_FOLDER = '/media/jamnicki/HDD/__Test_output/tematy'

    if os.path.exists(OUTPUT_FOLDER) and os.listdir(OUTPUT_FOLDER):
        clear_folder(OUTPUT_FOLDER)

    chunks_dict = {}
    for test_file in os.listdir(INPUT_FOLDER):
        file_path = os.path.join(INPUT_FOLDER, test_file)

        output_files = split_corpus(
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
