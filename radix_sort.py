
from multiprocessing import Process, SimpleQueue
from time import sleep
from typing import Optional

"""
    Radix Sort
    William A. Morris
"""


def count_sort(
        arr: list[int],
        digit_to_sort: int,
        max_digits: int = 12
):
    """
    sort an array of elements based on one digit

     :param arr: the array to sort
     :param digit_to_sort: the digit to sort
     :param max_digits: the maximum number of digits of any number in array (default int max value)
     :return: the sorted array
     """
    # create bucket for all 10 digits 0-9
    build_output_arr: list[list[int]] = [[] for _ in range(10)]

    # for every number in the array
    for num in arr:
        # get zero filled str repr
        num_str = str(num).zfill(max_digits)
        # git digit at desired place
        digit = int(num_str[digit_to_sort])
        # put number in appropriate bucket
        build_output_arr[digit].append(num)

    # return sorted array by adding every number in every bucket in order
    return [num for each in build_output_arr for num in each]


def radix_sort(unsorted: list[int]) -> list[int]:
    """ regular ole radix sort """
    # make a copy of the unsorted array
    output = unsorted.copy()
    # get max value in array
    max_val = max(output)
    # get # of digits in max value
    max_places = len(f'{max_val}')

    # begin at most significant digit
    placeCounter = max_places - 1
    # and count down
    while placeCounter >= 0:
        # count sort for every place (thousands, hundreds, tens, ones)
        output = count_sort(output, placeCounter, max_places)
        placeCounter -= 1

    # return sorted array
    return output


def radix_sort_process(unsorted: list[int], result: SimpleQueue) -> None:
    """ radix sort wrapped up for execution as process """
    sorted_arr = radix_sort(unsorted)
    # store result from sort in async queue
    result.put(sorted_arr)


def merge(sorted_i: list[int], sorted_j: list[int]) -> list[int]:
    """ merge two sorted arrays, maintain sort """
    # get size of both arrays
    size_i = len(sorted_i)
    size_j = len(sorted_j)
    # store current index while iterating through both arrays
    current_i_idx, current_j_idx = 0, 0
    # created output array
    output = []
    # while both arrays have a value at the front
    while current_i_idx < size_i and current_j_idx < size_j:
        # add smaller of two to output, iterate
        if sorted_i[current_i_idx] < sorted_j[current_j_idx]:
            output.append(sorted_i[current_i_idx])
            current_i_idx += 1
        else:
            output.append(sorted_j[current_j_idx])
            current_j_idx += 1

    # when one array is empty
    # return the generated output and remaining values in non-empty list
    return output + sorted_i[current_i_idx:] + sorted_j[current_j_idx:]


def parallel_radix_sort(unsorted: list[int], process_count: int = 4) -> list[int]:
    """ parallel implementation of radix sort """
    # get size of array
    list_size = len(unsorted)
    # get size of each subarray to sort in parallel
    block_size: int = list_size // process_count

    # create array to store running processes
    processes = []
    # create process results queue
    process_results_queue = SimpleQueue()

    # create all desired processes
    subarray_start = 0
    subarray_end = block_size
    for i in range(process_count):
        if i == process_count:
            sublist = unsorted[subarray_start:list_size]
        else:
            sublist = unsorted[subarray_start:subarray_end]

        # create new process, pass in subarray
        np = Process(target=radix_sort_process, args=(sublist, process_results_queue))
        processes.append(np)

        # next subarray
        subarray_start = subarray_start + block_size
        subarray_end = subarray_end + block_size

    # start all jobs
    for proc in processes:
        proc.start()

    # count completed process
    completed_processes = 0
    # create final result array
    results: Optional[list[int]] = None
    # poll process_results_queue every second for new results
    while True:
        sleep(1)

        process_output = process_results_queue.get()

        # if process_results_queue returned a value, record
        if process_output is not None:
            completed_processes += 1

        # store first output to result array
        if completed_processes == 1:
            results = process_output
        # else merge remaining process outputs into existing results array
        elif results is not None:
            results = merge(results, process_output)

        # if all processes have completed exit
        if completed_processes == process_count:
            break

    # terminate lingering processes
    for proc in processes:
        proc.terminate()

    # close queue
    process_results_queue.close()

    return results
