import argparse

from split import split_corpus


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--src-path",
        help="Path to directory, zip or text file."
    )
    parser.add_argument(
        "-o",
        "--dst-path",
        help="Destination directory path."
    )
    parser.add_argument(
        "-s",
        "--chunk-size",
        type=int,
        help="Size of each partial file in bytes."
    )
    return parser.parse_args()


def main():
    args = get_args()

    split_corpus(
        source_path=args.src_path,
        destination_path=args.dst_path,
        chunk_size=args.chunk_size
    )


if __name__ == "__main__":
    main()
