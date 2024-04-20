import time

from radix_sort import is_sorted, generate_list, parallel_radix_sort, radix_sort


def main():

    random_list = generate_list(10_000_000, 1, 9_999_999)

    test = random_list.copy()
    start = time.time()
    test = radix_sort(test)
    end = time.time()

    stopwatch = end - start

    assert is_sorted(test)
    assert len(random_list) == len(test)
    print(f'took radix {stopwatch:.2f} seconds')

    testp = random_list.copy()

    start = time.time()
    testp = parallel_radix_sort(testp, 2)
    end = time.time()

    stopwatch = end - start

    assert is_sorted(testp)
    assert len(random_list) == len(testp)
    print(f'took p-radix {stopwatch:.2f} seconds')


if __name__ == '__main__':
    main()
