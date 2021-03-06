import unittest
import random

def bubbleSort(arr):
    arrLen = len(arr)
    for i in range(1, arrLen):
        for j in range(0, arrLen - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def selectionSort(arr):
    arrLen = len(arr)
    for i in range(arrLen - 1):
        minIndex = i
        for j in range(i + 1, arrLen):
            if arr[j] < arr[minIndex]:
                minIndex = j

        if i != minIndex:
            arr[i], arr[minIndex] = arr[minIndex], arr[i]
    return arr


def insertionSort(arr):
    for i in range(1, len(arr)):
        preIndex = i - 1
        current = arr[i]
        while preIndex >= 0 and arr[preIndex] > current:
            arr[preIndex + 1] = arr[preIndex]
            preIndex -= 1
        arr[preIndex + 1] = current
    return arr


def shellSort(arr):
    arrLen = len(arr)
    gap = arrLen // 2
    while gap > 0:
        for i in range(gap, arrLen):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap = gap // 2
    return arr


def mergeSort(arr):
    if (len(arr) < 2):
        return arr
    middle = len(arr) // 2
    left, right = arr[:middle], arr[middle:]
    return merge(mergeSort(left), mergeSort(right))


def merge(left, right):
    result = []
    while left and right:
        if left[0] <= right[0]:
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))
    while left:
        result.append(left.pop(0))
    while right:
        result.append(right.pop(0))
    return result


def quickSort(arr, left, right):
    if left >= right:
        return arr
    key = arr[left]
    low = left
    high = right
    while left < right:
        while left < right and arr[right] >= key:
            right -= 1
        arr[left] = arr[right]
        while left < right and arr[left] <= key:
            left += 1
        arr[right] = arr[left]
    arr[right] = key
    quickSort(arr, low, left - 1)
    quickSort(arr, left + 1, high)
    return arr

class TestBubbleSortMethod(unittest.TestCase):
    def test_nulllist(self):
        predict = []
        self.assertEqual(predict, bubbleSort([]))

    def test_order(self):
        predict = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.assertEqual(predict, bubbleSort([1, 2, 3, 4, 5, 6, 7, 8, 9]))

    def test_unorder(self):
        predict = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.assertEqual(predict, bubbleSort([3, 4, 6, 7, 1, 9, 2, 5, 8]))

    def test_order_dup(self):
        predict = [1, 2, 4, 4, 4, 5, 6, 6, 7, 9]
        self.assertEqual(predict, bubbleSort([1, 2, 4, 4, 4, 5, 6, 6, 7, 9]))

    def test_unorder_dup(self):
        predict = [1, 2, 4, 4, 4, 5, 6, 6, 7, 9]
        self.assertEqual(predict, bubbleSort([2, 4, 1, 4, 6, 7, 6, 5, 4, 9]))


class TestSelectionSort(unittest.TestCase):
    def test_nulllist(self):
        predict = []
        self.assertEqual(predict, selectionSort([]))

    def test_order(self):
        predict = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.assertEqual(predict, selectionSort([1, 2, 3, 4, 5, 6, 7, 8, 9]))

    def test_unorder(self):
        predict = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.assertEqual(predict, selectionSort([3, 4, 6, 7, 1, 9, 2, 5, 8]))

    def test_order_dup(self):
        predict = [1, 2, 4, 4, 4, 5, 6, 6, 7, 9]
        self.assertEqual(predict, selectionSort([1, 2, 4, 4, 4, 5, 6, 6, 7, 9]))

    def test_unorder_dup(self):
        predict = [1, 2, 4, 4, 4, 5, 6, 6, 7, 9]
        self.assertEqual(predict, selectionSort([2, 4, 1, 4, 6, 7, 6, 5, 4, 9]))


if __name__ == '__main__':
    unittest.main()
