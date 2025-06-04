import unittest

from src.ternary_search_tree import TernarySearchTree


class TestTernarySearchTree(unittest.TestCase):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        with open('data/search_trees/insert_words.txt') as file:
            words = [line.strip() for line in file]

        self.insertion_words = words

        with open('data/search_trees/not_insert_words.txt') as file:
            words = [line.strip() for line in file]

        self.non_insertion_words = words

    def test_tree_insert_single_word(self) -> None:
        tst = TernarySearchTree()
        assert len(tst) == 0

        tst.insert("word")
        assert len(tst) == 1
        assert tst.all_strings() == ["word"]

    def test_tree_insert_duplicate_word(self) -> None:
        tst = TernarySearchTree()
        assert len(tst) == 0

        tst.insert("word")
        tst.insert("word")
        assert len(tst) == 1
        assert tst.all_strings() == ["word"]

    def test_tree_insert_empty_string(self) -> None:
        tst = TernarySearchTree()
        tst.insert("")
        assert len(tst) == 1
        assert tst.all_strings() == [""]

    def test_tree_search_word_inserted_entry(self) -> None:
        tst = TernarySearchTree()
        tst.insert("word")
        assert tst.search("word", exact=True) is True

    def test_tree_search_word_nonexistent_entry(self) -> None:
        tst = TernarySearchTree()
        tst.insert("word")
        assert tst.search("nonexistent", exact=True) is False

    def test_tree_search_prefix_inserted_entry(self) -> None:
        tst = TernarySearchTree()
        tst.insert("word")
        assert tst.search("wo", exact=False) is True

    def test_tree_search_prefix_nonexistent_entry(self) -> None:
        tst = TernarySearchTree()
        tst.insert("word")
        assert tst.search("woo", exact=False) is False

    def test_tree_search_word_empty_string(self) -> None:
        tst = TernarySearchTree()
        tst.insert("")
        assert tst.search("", exact=True) is True

    def test_tree_search_word_empty_string_no_direct_insertion(self) -> None:
        tst = TernarySearchTree()
        tst.insert("word")
        assert tst.search("", exact=True) is False

    def test_tree_search_prefix_empty_string(self) -> None:
        tst = TernarySearchTree()
        tst.insert("")
        assert tst.search("", exact=False) is True

    def test_tree_search_prefix_empty_string_no_direct_insertion(self) -> None:
        tst = TernarySearchTree()
        tst.insert("word")
        assert tst.search("", exact=False) is True

    def test_tree_length(self) -> None:
        tst = TernarySearchTree()
        assert len(tst) == 0

        for word in self.insertion_words:
            tst.insert(word)

        unique_words = set(self.insertion_words)
        assert len(tst) == len(unique_words)

    def test_tree_all_strings(self) -> None:
        tst = TernarySearchTree()
        assert tst.all_strings() == []

        words = ["this", "list", "is", "not", "sorted"]

        for word in words:
            tst.insert(word)

        assert tst.all_strings() == sorted(words)

    def test_tree_search_word_extensive(self) -> None:
        tst = TernarySearchTree()
        unique_words = set(self.insertion_words)

        for word in unique_words:
            tst.insert(word)

        for word in unique_words:
            assert tst.search(word, exact=True) is True

    def test_tree_search_word_extensive_fail(self) -> None:
        tst = TernarySearchTree()
        unique_words = set(self.insertion_words)

        for word in unique_words:
            tst.insert(word)

        for word in unique_words:
            for i in range(len(word), 0, -1):
                prefix = word[:i]
                if prefix not in unique_words:
                    assert tst.search(prefix, exact=True) is False

    def test_tree_search_prefix_extensive(self) -> None:
        tst = TernarySearchTree()
        unique_words = set(self.insertion_words)

        for word in unique_words:
            tst.insert(word)

        for word in unique_words:
            for i in range(len(word) - 1, 0, -1):
                prefix = word[:i]
                assert tst.search(prefix, exact=False) is True

    def test_tree_search_prefix_extensive_non_inserted(self) -> None:
        tst = TernarySearchTree()
        unique_words = set(self.insertion_words)

        for word in unique_words:
            tst.insert(word)

        for word in self.non_insertion_words:
            assert tst.search(word, exact=False) is False

    def test_tree_all_strings_extensive_sorted(self) -> None:
        tst = TernarySearchTree()
        unique_words = set(self.insertion_words)

        for word in self.insertion_words:
            tst.insert(word)

        assert tst.all_strings() == sorted(unique_words)
