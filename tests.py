import unittest

from radix_sort import generate_list, count_sort, is_sorted, radix_sort, parallel_radix_sort


class TestRadixSortFunctions(unittest.TestCase):

    def test_count_sort_1_digit(self):
        vals = generate_list(1_000, 1, 9)
        done = count_sort(vals, 0, 1)
        self.assertTrue(is_sorted(done), 'list should be sorted')

    def test_radix_sort_2_digit(self):
        vals = generate_list(1_000, 0, 99)
        done = radix_sort(vals)
        self.assertTrue(is_sorted(done), 'list should be sorted')

    def test_radix_sort_7_digit(self):
        vals = generate_list(1_000, 0, 9_999_999)
        done = radix_sort(vals)
        self.assertTrue(is_sorted(done), 'list should be sorted')

    def test_radix_sort_7_digit_p(self):
        vals = generate_list(1_000_000, 0, 9_999_999)
        done = parallel_radix_sort(vals)
        self.assertTrue(is_sorted(done), 'list should be sorted')
