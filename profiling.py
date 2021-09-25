import io
import os
import time
import pstats
import cProfile
from pathlib import Path
from datetime import datetime


def log_profile(func, log_folder="profile_logs"):
    def inner(*args, **kwargs) -> object:
        curr_time_hr: object = datetime.now()
        curr_time_unixs: object = time.time()

        pr: object = cProfile.Profile()

        pr.enable()
        retval: object = func(*args, **kwargs)
        pr.disable()

        stream = io.StringIO()
        ps: object = pstats.Stats(pr, stream=stream).sort_stats('cumulative')
        ps.print_stats()

        report_content: str = stream.getvalue()

        Path(log_folder).mkdir(parents=True, exist_ok=True)

        script_path: str = func.__globals__['__file__']
        log_title: str = f'{script_path}: {func.__name__} at {curr_time_hr}'
        log_heading: str = f"{'='*10} {log_title} {'='*10}\n\n"
        log_filename: str = f"log_{str(curr_time_unixs).replace('.', '_')}.txt"
        log_path: str = os.path.join(log_folder, log_filename)

        with open(log_path, 'w') as log_f:
            log_f.writelines([log_heading, report_content])

        return retval

    return inner
