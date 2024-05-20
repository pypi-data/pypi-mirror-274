from bisect import bisect_right
from collections import defaultdict
from functools import cache
from importlib import resources as impresources
import re
from typing import Iterable, Literal, TypeAlias, get_args
import unicodedata

import lxml.etree as ETree

from . import corpora


ChapterAndVerse: TypeAlias = tuple[int, int]
CorpusName: TypeAlias = Literal[
    "ahmedali", "ahmedraza", "arberry", "daryabadi", "hilali", "itani",
    "maududi", "mubarakpuri", "pickthall", "qarai", "qaribullah",
    "sahih", "sarwar", "shakir", "transliteration", "wahiduddin",
    "yusufali",
]
VALID_CORPORA: tuple[CorpusName, ...] = get_args(CorpusName)


class Concordance:
    def __init__(self, corpus: CorpusName):
        """
        Create a concordance of words from a Quran corpus.

        Parameters
        ----------
        corpus : str
            Name of the Quran corpus (e.g. `pickthall`, `sahih`,
            `yusufali`).
        """
        # Check that corpus is valid
        if corpus not in VALID_CORPORA:
            raise ValueError(
                f"Invalid corpus; must be one of: {', '.join(VALID_CORPORA)}",
            )

        self.content = []
        self.words = []
        self.starts = []
        indices: defaultdict[str, list[int]] = defaultdict(list)

        # HACK Tanzil.net's XML files for Quran translations have
        # comments with double dashes ("--") in them, which is not well-
        # formed XML. Adding recover=True will force the parser to parse
        # this anyway.
        parser = ETree.XMLParser(recover=True)
        corpus_file = (impresources.files(corpora) / f"en.{corpus}.xml")
        with corpus_file.open("rb") as file:
            tree = ETree.parse(file, parser)
        root = tree.getroot()

        # Word index = index of this word in the Quran
        word_index = 0
        # For each chapter
        for sura in root.iter("sura"):
            sura_content = []
            # Verse starts = starting word indices of each verse in this
            # chapter
            verse_starts = []
            # For each verse in this chapter
            for aya in sura.iter("aya"):
                text = aya.attrib["text"]
                sura_content.append(text)
                words = self.text_to_words(text)

                # Normalized words will be in lowercase, and only have
                # letters and digits
                normalized_words = [
                    self.normalize_word(word)
                    for word in words
                ]

                # This verse starts at this word index
                verse_starts.append(word_index)

                # Add these words to the concordance
                self.words.extend(words)
                for word in normalized_words:
                    indices[word].append(word_index)
                    word_index += 1

            self.content.append(sura_content)
            # Add these verse starts to the concordance
            self.starts.append(verse_starts)

        # I don't like keeping the indices as a defaultdict
        self.indices = dict(indices)

    @staticmethod
    def valid_corpora() -> list[CorpusName]:
        """
        Get a list of all valid corpus names.

        Returns
        -------
        list of str
            List of all valid corpus names.
        """
        return list(VALID_CORPORA)

    @staticmethod
    def normalize_word(word: str, preserve_case: bool = False) -> str:
        """
        Normalize a word by removing everything but letters and digits.

        Parameters
        ----------
        word : str
            Word to normalize.
        preserve_case : bool, default False
            If true, preserve the case of the word. If false, convert
            the word to lowercase

        Returns
        -------
        str
            Normalized word.
        """
        # Strip everything but letters and digits
        stripped_word = re.sub(
            r"[^0-9a-z]",
            "",
            # NOTE Normalizing with NFD splits accented characters into
            # characters and their accents.
            unicodedata.normalize("NFD", word),
            flags=re.IGNORECASE,
        )
        if preserve_case:
            return stripped_word
        # Convert to lowercase if case shouldn't be preserved
        return stripped_word.lower()

    @staticmethod
    def text_to_words(text: str, alnum_only=True) -> list[str]:
        """
        Split a string into words.

        "Words" consist of letters, digits, apostrophes, and dashes; any
        other characters are removed.

        Parameters
        ----------
        text : str
            String to split into words.
        alnum_only : bool, default True
            If true, remove "words" that don't contain any alphanumeric
            characters when converted.

        Returns
        -------
        list of str
            List of words.
        """
        words = [
            # NOTE Normalizing with NFD splits accented characters into
            # characters and their accents.
            unicodedata.normalize("NFD", word)
            for word in text.split()
        ]

        return [
            re.sub(r"[^0-9a-z'\-]", "", word, flags=re.IGNORECASE)
            for word in words
            if (
                re.search(r"[0-9a-z]", word, flags=re.IGNORECASE)
                if alnum_only
                else True
            )
        ]

    @cache
    def word_index_to_verse(self, word_index: int) -> ChapterAndVerse:
        """
        Convert a word index in this concordance to a chapter and verse
        index.

        Parameters
        ----------
        word_index : int
            Index of a word in this concordance.

        Returns
        -------
        tuple of (int, int)
            Chapter and verse index (0-based).
        """
        # Find chapter index in chapter starts
        chapter_index = bisect_right(
            self.starts,
            word_index,
            key=lambda a: a[0],
        )
        if not chapter_index:
            raise ValueError("could not find chapter")
        chapter_index -= 1

        # Find chapter index in verse starts for this chapter
        verse_index = bisect_right(
            self.starts[chapter_index],
            word_index,
            key=lambda a: a,
        )
        if not verse_index:
            raise ValueError("could not find verse")
        verse_index -= 1

        # NOTE Chapter and verse index are 0-based
        return (chapter_index, verse_index)

    def word_indices_to_verses(
            self,
            word_indices: Iterable[int],
    ) -> set[ChapterAndVerse]:
        """
        Convert a word indices in this concordance to chapter and verse
        indices.

        Parameters
        ----------
        word_indices : iterable of int
            Indices of words in this concordance.

        Returns
        -------
        set of tuple of (int, int)
            Chapter and verse indices (1-based).
        """
        return self._word_indices_to_verses(tuple(word_indices))

    # HACK To add caching to word_indices_to_verses for general
    # iterables (even unhashable ones), this helper function is used
    # that only accepts a tuple of ints, and caching is applied to this
    # function instead.
    @cache
    def _word_indices_to_verses(
            self,
            word_indices: tuple[int],
    ) -> set[ChapterAndVerse]:
        return set(
            self.word_index_to_verse(word_index)
            for word_index in word_indices
        )

    @cache
    def search(self, query: str) -> list[int]:
        """
        Search the concordance for instances of a search query.

        Syntax for queries:
        - `phrase`: search for `phrase`.
        - `^phrase`: search for `phrase` case-sensitively.
        - `#phrase`: don't search for `phrase`; return no results.

        Parameters
        ----------
        query : str
            Search query.

        Returns
        -------
        list of int
            List of word indices matching the search query.
        """
        if ";" in query:
            return sorted(
                index
                for subquery in query.split(";")
                for index in self.search(subquery)
            )

        # If query starts with "#", ignore the query
        if query.startswith("#"):
            return []

        case_sensitive = False
        # If query starts with "^", make the search case-sensitive 
        if query.startswith("^"):
            case_sensitive = True
            query = query.removeprefix("^")

        words = [word for word in query.split()]
        # If word list is empty, return no results
        if not words:
            return []

        first_word, *other_words = words
        # Search for first word case-insensitive
        first_word_indices = self.indices.get(
            self.normalize_word(first_word), [],
        )
        if not first_word_indices:
            return []

        # Normalize all search words
        first_word = self.normalize_word(
            first_word,
            preserve_case=case_sensitive,
        )
        other_words = [
            self.normalize_word(
                other_word,
                preserve_case=case_sensitive,
            )
            for other_word in other_words
        ]

        indices = []
        # Continue searching from each occurrence of the first word
        for word_index in first_word_indices:
            # Do case-sensitive check of this word
            if case_sensitive:
                # If word doesn't match, continue
                if first_word != self.normalize_word(
                    self.words[word_index],
                    preserve_case=case_sensitive,
                ):
                    continue

            found_result = True
            # Check that all other words match
            for offset, other_word in enumerate(other_words, 1):
                next_word = self.normalize_word(
                    self.words[word_index + offset],
                    preserve_case=case_sensitive,
                )

                if other_word != next_word:
                    found_result = False
                    break

            # If all words match, this is a new result
            if found_result:
                indices.append(word_index)

        return indices
