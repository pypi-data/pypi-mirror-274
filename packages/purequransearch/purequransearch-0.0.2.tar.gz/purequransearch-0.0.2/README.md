# pure-quran-search

Search the Quran (in English) for words and phrases.

## Installation

purequransearch is installable from PyPI:

```bash
$ pip install --upgrade pure-quran-search
```

## Usage

purequransearch can be imported as a Python module:

```python
from purequransearch import Concordance

concordance = Concordance("pickthall")
query = input("Enter query: ")

results = concordance.search(query)
verses = concordance.word_indices_to_verses(results)
print(f"Found {len(results)} occurrence(s) in {len(verses)} verse(s).")
```

purequransearch can also be used as a command line tool:

```bash
$ purequransearch search "the test" -c pickthall
6:165   He it is Who hath placed you as viceroys of the earth and hath exalted some of you in rank above others, that He may try you by {{(the test}} of) that which He hath given you. Lo! Thy Lord is swift in prosecution, and Lo! He verily is Forgiving, Merciful.
Occurrences: 1; Verses: 1

23:30   Lo! herein verily are portents, for lo! We are ever putting (mankind) to {{the test.}}
Occurrences: 2; Verses: 2

Found 2 occurrence(s) in 2 verse(s).

```

## Changelog

### v0.0.2 (2024-05-19)

- Fixed CLI error that can happen with overlapping matches.

### v0.0.1 (2024-05-19)

Initial release.
