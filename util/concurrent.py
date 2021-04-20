"""
Hosts utility classes or functions that support thread-safe operations.
"""

import threading


class AtomicInteger:
    """
    An integer whose value can be read/changed by multiple threads concurrently with consistency.
    """
    _value = 0
    _lock = None

    def __init__(self, ini=0):
        self._value = ini
        self._lock = threading.Lock()

    def get(self):
        return self._value

    def increment_and_get(self):
        """
        Increments the value safely, and then returns it.
        :return:
        """
        with self._lock:
            self._value += 1
            return self._value

    def get_and_increment(self):
        """
        Returns the value, then increments it safely.
        :return:
        """
        val = self._value
        with self._lock:
            self._value += 1
        return val


class ConcurrentSet:
    """
    A set that can be modified concurrently safely.
    """
    _set = None
    _lock = None

    def __init__(self):
        self._set = set()
        self._lock = threading.Lock()

    def size(self):
        """
        Returns the number of elements in the set.
        :return:
        """
        return len(self._set)

    def add(self, value):
        """
        Adds a value to the set.
        :return:
        """
        with self._lock:
            self._set.add(value)

    def remove(self, value):
        """
        Removes a value from the set.
        :param value:
        :return:
        """
        with self._lock:
            self._set.remove(value)

    def contains(self, value):
        """
        Checks if the set contains the specified value.
        :param value:
        :return:
        """
        return value in self._set

    def clear(self):
        """
        Removes all elements in the set.
        :return:
        """
        with self._lock:
            self._set.clear()

    def copy_to_set(self):
        """
        Creates and returns a shallow copy of the set. A regular Python set is returned.
        :return:
        """
        return set(self._set)
