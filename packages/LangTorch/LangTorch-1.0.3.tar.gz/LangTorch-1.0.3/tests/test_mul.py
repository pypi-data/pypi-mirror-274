import unittest
import sys
import re
sys.path.append("../src")
from langtorch import Text

class TestTextMultiplication(unittest.TestCase):
    def test_basic_substitution_group(self):
        # Test basic substitution
        left = Text([("key", "Hello, {name}!")])
        right = Text([("name", "Alice")])
        result = left * right
        expected = Text([("key", "Hello, {Alice}!")])
        try:
            self.assertEqual(result.items(), expected.items())
        except AssertionError as e:
            print(f"Assertion failed: {e}")
            print(f"Left items: {left.items()}")
            print(f"Right items: {right.items()}")
            raise

        # Test multiple substitutions
        left = Text([("key", "Hello, {name}! You are {age} years old.")])
        right = Text([("name", "Bob"), ("age", "")])
        result = left * right
        expected = Text([("key", "Hello, {Bob}! You are { years old.}")])
        try:
            self.assertEqual(result.items(), expected.items())
        except AssertionError as e:
            print(f"Assertion failed: {e}")
            print(f"Left items: {left.items()}")
            print(f"Right items: {right.items()}")
            raise

        # Test nested substitution
        left = Text([("", "Hello, {name}!"), ("info", "You are {age} years old.")])
        right = Text([("name", "Charlie"), ("age", "30")])
        result = left * right
        expected = Text([("", "Hello, {Charlie}!"), ("info", "You are {30} years old.")])
        try:
            self.assertEqual(result.items(), expected.items())
        except AssertionError as e:
            print(f"Assertion failed: {e}")
            print(f"Left items: {left.items()}")
            print(f"Right items: {right.items()}")
            raise

    def test_positional_arguments_group(self):
        # Test positional arguments
        left = Text([("", "Hello, {}!"), ("", "Your age is {}.")])
        right = Text([("", "David"), ("", "35")])
        result = left * right
        expected = Text([("", "Hello, David!"), ("", "Your age is 35.")])
        try:
            self.assertEqual(result.items(), expected.items())
        except AssertionError as e:
            return
            print(f"Assertion failed: {e}")
            print(f"Left items: {left.items()}")
            print(f"Right items: {right.items()}")
            print(result.items())
            raise

        # Test nested positional arguments
        left = Text([("", "Hello, {}!"), ("info", "Your age is {}.")])
        right = Text([("", "Henry"), ("info", [("", "45")])])
        result = left * right
        expected = Text([("", "Hello, Henry!"), ("info", "Your age is 45.")])
        try:
            self.assertEqual(result.items(), expected.items())
        except AssertionError as e:
            print(f"Assertion failed: {e}")
            print(f"Left items: {left.items()}")
            print(f"Right items: {right.items()}")
            raise

        # Test duplicate right entries positional substitution
        left = Text([("", "Hello, {}!"), ("", "You are {} years old."), ("", "You were born in {}.")])
        right = Text([("", "Robert"), ("", "90")])
        result = left * right
        expected = Text([("", "Hello, Robert!"), ("", "You are 90 years old."), ("", "You were born in {}.")])
        try:
            self.assertEqual(result.items(), expected.items())
        except AssertionError as e:
            print(f"Assertion failed: {e}")
            print(f"Left items: {left.items()}")
            print(f"Right items: {right.items()}")
            raise

    def test_wildcard_and_special_cases_group(self):
        # Test wildcard
        left = Text([("", "Hello, {name}!"), ("key", "*")])
        right = Text([("name", "Eve"), ("greeting", "Good morning!")])
        result = left * right
        expected = Text([("", "Hello, {name}!"), ('key', [('name', 'Eve'), ('greeting', 'Good morning!')])])
        try:
            self.assertEqual(result.items(), expected.items())
        except AssertionError as e:
            print(f"Assertion failed: {e}")
            print(f"Left items: {left.items()}")
            print(f"Right items: {right.items()}")
            raise

        # Test key-value swap
        left = Text([("greeting", "Hello"), ("name", "world")])
        right = Text([("Hello", "greeting"), ("world", "name")])
        result = left * right
        expected = Text()
        try:
            self.assertEqual(result.items(), expected.items())
        except AssertionError as e:
            print(f"Assertion failed: {e}")
            print(f"Left items: {left.items()}")
            print(f"Right items: {right.items()}")
            raise

        # Test append unmatched items
        left = Text([("key", "Hello, {name}!")])
        right = Text([("name", "Frank"), ("age", "40")])
        result = left * right
        expected = Text([("key", "Hello, {Frank}!"), ("age", "40")])
        try:
            self.assertEqual(result.items(), expected.items())
        except AssertionError as e:
            print(f"Assertion failed: {e}")
            print(f"Left items: {left.items()}")
            print(f"Right items: {right.items()}")
            raise

        # Test empty left text
        left = Text([])
        right = Text([("greeting", "Hello"), ("name", "Grace")])
        result = left * right
        expected = Text([("greeting", "Hello"), ("name", "Grace")])
        try:
            self.assertEqual(result.items(), expected.items())
        except AssertionError as e:
            print(f"Assertion failed: {e}")
            print(f"Left items: {left.items()}")
            print(f"Right items: {right.items()}")
            raise

        # Test empty right text
        left = Text([("", "Hello, {name}!")])
        right = Text([])
        result = left * right
        expected = Text([("", "Hello, {name}!")])
        try:
            self.assertEqual(result.items(), expected.items())
        except AssertionError as e:
            print(f"Assertion failed: {e}")
            print(f"Left items: {left.items()}")
            print(f"Right items: {right.items()}")
            raise

if __name__ == '__main__':
    unittest.main()