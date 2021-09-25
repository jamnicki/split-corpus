import os
import logging
from typing import List
from pathlib import Path
from profiling import log_profile


def utf8size(string: str) -> int:
    return len(string.encode('utf8'))


def _save_chunk(chunk_data: str, chunk_file_name: str, destination_path: str,
                open_mode="w"):
    chunk_file_path: str = os.path.join(destination_path, chunk_file_name)
    with open(chunk_file_path, open_mode) as chunk_file:
        chunk_file.write(chunk_data)
        logging.debug(f'Saving {chunk_file_name}...')


def _update_last_chunk(tail_data: str, chunk_file_name: str,
                       destination_path: str):
    _save_chunk(tail_data, chunk_file_name, destination_path, open_mode="a")
    logging.debug(f'Updating last chunk({chunk_file_name})...')


@log_profile
def split_corpus(source_path: str, destination_path: str, file_name: str,
                 chunk_size: int, last_chunk_ratio=0.5, sep_diff_ratio=0.05,
                 separators=[". ", "!", "?", "...", ".", ",", " "]):
    file_size: str = os.path.getsize(source_path)
    if file_size == 0:
        logging.error('File is empty!')
        return None

    if chunk_size >= file_size:
        logging.error('Chunk size is greater than/equal to file size!')
        return None

    logging.debug(f'Creating the tree... ({destination_path})')
    Path(destination_path).mkdir(parents=True, exist_ok=True)

    output_files: List[str] = []
    read_buffer_size = int(chunk_size / 4)
    with open(source_path, "r") as file_stream:
        logging.debug(f'Processing {source_path}... ({file_size*10**-6} MB)\n')

        chunk_num = 0
        chunk_data = ""
        while True:
            # collect data until its exhausted
            buffer = file_stream.read(read_buffer_size)
            buffer_size = utf8size(buffer)
            if buffer_size == 0:
                if chunk_data:
                    # if any data left - update last chunk if data is too small
                    # otherwise save it as the next chunk
                    if utf8size(chunk_data) <= last_chunk_ratio * chunk_size:
                        chunk_num -= 1
                        chunk_file_name: str = f'{file_name}_{chunk_num}'
                        _update_last_chunk(
                            chunk_data, chunk_file_name, destination_path
                        )
                    else:
                        chunk_file_name: str = f'{file_name}_{chunk_num}'
                        _save_chunk(
                            chunk_data, chunk_file_name, destination_path
                        )
                        output_files.append(chunk_file_name)
                break  # no more data

            chunk_data += buffer
            curr_chunk_size = utf8size(chunk_data)
            if curr_chunk_size > chunk_size:
                # max chunk_size is reached so save chunk_data to file
                divided_by_separator = False
                for separator in separators:
                    # try split chunk_data by the most suitable separator
                    if separator in chunk_data[::-1]:
                        div_index = chunk_data.rindex(separator) + 1
                        save_part_size = utf8size(chunk_data[:div_index])
                        if (1 - sep_diff_ratio) * chunk_size <= \
                                save_part_size \
                                <= (1 + sep_diff_ratio) * chunk_size:
                            # divide by separator if there is no significant
                            # size difference according to sep_diff_ratio value
                            divided_by_separator = True
                            save_part = chunk_data[:div_index]
                            tail = chunk_data[div_index:]
                            break

                chunk_file_name: str = f'{file_name}_{chunk_num}'
                if divided_by_separator:
                    # save data including the separator
                    # and store rest of it for the next chunk
                    _save_chunk(save_part, chunk_file_name, destination_path)
                    chunk_data = tail
                else:
                    # save whole collected data to a file
                    _save_chunk(chunk_data, chunk_file_name, destination_path)
                    chunk_data = ""

                output_files.append(chunk_file_name)
                chunk_num += 1

    return output_files
