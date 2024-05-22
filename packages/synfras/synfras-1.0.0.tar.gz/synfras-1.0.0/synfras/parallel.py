import os
from concurrent.futures import (
    Executor, ProcessPoolExecutor, ThreadPoolExecutor, as_completed
)
from typing import Literal

from tqdm import tqdm


def parallel(
    func,
    params_list,
    executor_type: Executor,
    add_results: Literal['append', 'extend'] = 'append',
    disable_pbar: bool = False
):

    num_iter = len(params_list)

    if executor_type == ThreadPoolExecutor:
        max_workers = int(os.getenv('SF_NUM_THREADS', 100))

    elif executor_type == ProcessPoolExecutor:
        max_workers = int(os.getenv('SF_NUM_PROCESSORS', 8))

    if max_workers > num_iter:
        max_workers = num_iter

    with executor_type(max_workers=max_workers) as executor:
        futures = [executor.submit(func, **p) for p in params_list]
        results = []
        with tqdm(total=num_iter, disable=disable_pbar) as pbar:
            for future in as_completed(futures):
                if add_results == 'append':
                    results.append(future.result())
                elif add_results == 'extend':
                    results.extend(future.result())
                pbar.update()

        return results
