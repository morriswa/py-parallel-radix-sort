
import csv
import time

from random import randint

from radix_sort import radix_sort, parallel_radix_sort

"""
    Parallel Radix Sort Time Trials
    :author William A. Morris
"""

# test params
TRIALS = 5
TEST_ARRAY_SIZES = [100_000_000]
TEST_PROCESSES = [4, 2, 1]
TEST_RANGES = [999_999]
TEST_CASES = [(size, proc, range_w)
              for size in TEST_ARRAY_SIZES
              for proc in TEST_PROCESSES
              for range_w in TEST_RANGES]


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

        # run test cases
        for test in TEST_CASES:
            size = test[0]
            proc = test[1]
            range_w = test[2]

            # log current test case
            print(f'===== Size: {size} Processes: {proc} Range: {range_w} =====')

            # run desired number of trials
            for trial in range(TRIALS):
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

                print(f'Trial {trial + 1}: {stopwatch}')
                # record data
                recorder.writerow([size, range_w, proc, round(stopwatch * 1000)])

            # write test case results, continue
            timetrials.flush()


if __name__ == '__main__':
    main()
