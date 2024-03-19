import unittest
import hashlib
from pathlib import Path
import json

# CONSTANTS
INPUT_FILE = "qualcomm-test-words.txt"
LOOKUP_FILE = ".cache.json"


def file_hash_finder(fname: str) -> str:
    """Small helper function that gets a hash for a given file

    :param fname: file name
    :type fname: str
    :return: hash for that file based on the contents inside it
    :rtype: str
    """
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        # maybe file is too big
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


class DataLoader:
    def __init__(self, input_file: str, overwrite: bool = False) -> None:
        """An interface to interact with input file

        :param input_file: name of the input file
        :type input_file: str
        :param overwrite: overwrite the cache json that speeds up the lookup, defaults to False
        :type overwrite: bool, optional
        """
        data = {"prev_hash": None, "lookup": None}
        # preload previous lookup json
        if Path(LOOKUP_FILE).exists():
            with open(LOOKUP_FILE, "rb") as f:
                data = json.load(f)

        # compare hash of the current input file with previous, or re-write lookup json irrespective if overwrite flag is true
        input_file_hash = file_hash_finder(input_file)
        if overwrite or data["prev_hash"] != input_file_hash:
            data = self.__create_lookup(input_file)

        self.data = data

    def perform_lookup(self, word: str) -> list[str]:
        """For a passed word get all anagrams

        :param word: single word
        :type word: str
        :return: list of anagrams
        :rtype: list[str]
        """
        normalized_word = "".join(sorted(word.lower().strip()))
        return self.data["lookup"].get(normalized_word, [])

    def __create_lookup(self, input_file: str) -> dict:
        """This function reads an input file with words sperated by linebreaks and creates a lookup cache json for it

        :param input_file: file name
        :type input_file: str
        :return: dictionary representation of the cache lookup json
        :rtype: dict
        """
        data = {"prev_hash": file_hash_finder(input_file), "lookup": {}}
        with open(input_file, "r") as f:
            lines = f.readlines()
            for line in lines:
                # create dictionary with all letters of the word lowercase and sorted
                curr_key = "".join(sorted(line.lower().strip()))
                curr_val = data.get("lookup", {}).get(curr_key)
                if isinstance(curr_val, list):
                    curr_val.append(line.strip())
                else:
                    data["lookup"][curr_key] = [line.strip()]

        # dump new dictionary to a new lookup json
        with open(LOOKUP_FILE, "w") as f:
            json.dump(data, f)

        return data


class Anagrams:
    def __init__(self):
        self.data_loader = DataLoader(INPUT_FILE)

    def get_anagrams(self, word: str) -> list[str]:
        return self.data_loader.perform_lookup(word)


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
