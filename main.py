
import csv
import time

from random import randint

from radix_sort import radix_sort, parallel_radix_sort

"""
    Parallel Radix Sort Time Trials
    :author William A. Morris
"""


def generate_list(size: int, min_num: int = 1, max_num: int = 100_000) -> list[int]:
    """ Generate a list with random numbers between (inclusive) `min_num` and `max_num`"""
    new_list = [randint(min_num, max_num) for _ in range(size)]

    return new_list


def is_sorted(arr: list[int]) -> bool:
    """ Check if `arr` is sorted """
    # store first element
    previous_element = arr[0]
    # for every element in the array
    for current_element in arr[1:]:
        # compare to last element
        if current_element < previous_element:
            return False
        # update previous
        previous_element = current_element
    return True


def main():
    # open log file
    with open('timetrials.csv', 'w') as timetrials:
        # init csv writer
        recorder = csv.writer(timetrials)
        # write header
        recorder.writerow(['Array Size', 'Max Num', 'Processes', 'TT Sort ms'])

        # test setup
        trials = 10
        sizes = [100_000, 1_000_000, 10_000_000, 100_000_000]
        processes = [1, 2, 4, 8]
        ranges = [9, 99, 999, 9_999, 999_999, 9_999_999]
        test_cases = [(size, proc, range_w)
                      for size in sizes
                      for proc in processes
                      for range_w in ranges]

        # run test cases
        for test in test_cases:
            size = test[0]
            proc = test[1]
            range_w = test[2]

            # log current test case
            print(f'===== Test Case S: {size} P: {proc} R: {range_w} =====')

            # run desired number of trials
            for _ in range(trials):
                # get a list
                random_list = generate_list(size, 1, range_w)

                # start stopwatch
                start = time.time()
                if proc == 1:  # if running on a single process, use reg sort
                    test_result = radix_sort(random_list)
                else:  # else parallel with desired # of processes
                    test_result = parallel_radix_sort(random_list, proc)
                # stop after completion
                end = time.time()

                # get time (seconds)
                stopwatch = end - start

                # record data
                recorder.writerow([size, range_w, proc, round(stopwatch * 1000)])

            # write test case results, continue
            timetrials.flush()


if __name__ == '__main__':
    main()
