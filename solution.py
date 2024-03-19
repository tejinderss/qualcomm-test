import unittest


class Anagrams:
    def __init__(self):
        self.words = open("words.txt").readlines()

    def get_anagrams(self, word):
        pass


class TestAnagrams(unittest.TestCase):
    def test_anagrams(self):
        anagrams = Anagrams()
        self.assertEquals(
            anagrams.get_anagrams("plates"),
            ["palest", "pastel", "petals", "plates", "staple"],
        )
        self.assertEquals(anagrams.get_anagrams("eat"), ["ate", "eat", "tea"])


if __name__ == "__main__":
    unittest.main()
