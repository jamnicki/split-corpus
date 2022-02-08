import os


def utf8size(string: str) -> int:
    return len(string.encode("utf8"))


def clear_folder(relative_path: str):
    clear_command = f"rm {relative_path}/*"
    decision = input(f"Executing:\n\t> {clear_command}\n\nProceed (y/n)?")
    if decision.lower() == "y":
        os.system(clear_command)
        print(f"Clearing {relative_path}...\n")
