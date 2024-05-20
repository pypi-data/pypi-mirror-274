from argparse import ArgumentParser, RawDescriptionHelpFormatter
from collections import defaultdict
import sys

from purequransearch import Concordance, VALID_CORPORA


def cli():
    # Create parser for command line arguments
    parser = ArgumentParser(
        prog="purequransearch",
        description=(
            "Search the Quran (in English) for words and phrases."
        ),
    )
    subparsers = parser.add_subparsers(
        title="commands",
        dest="command",
    )

    parser_search = subparsers.add_parser(
        "search", help="search Quran for a query",
        epilog=(
            "example queries:\n"
            "  the great\n"
            "    Search for \"the great\", case-insensitive.\n"
            "  ^Loving\n"
            "    Search for \"Loving\", case-sensitive.\n"
            "  #hidden\n"
            "    Do not search for this query (reports 0 occurrences "
            "in 0 verses).\n"
            "  Allah;god\n"
            "    Search for \"Allah\" and \"god\" (searches both "
            "queries separately).\n"
            "  ^He;him\n"
            "    Search for \"He\", case-sensitive, and \"him\", case-"
            "insensitive."
        ),
        formatter_class=RawDescriptionHelpFormatter,
    )
    parser_search.add_argument(
        "query", help="search query",
        metavar="QUERY",
        type=str,
    )
    parser_search.add_argument(
        "-c", "--corpus",
        help='Quran corpus (e.g. "pickthall", "sahih", "yusufali")',
        metavar="CORPUS",
        choices=VALID_CORPORA, required=True,
    )
    parser_search.add_argument(
        "-o", "--output", help=(
            "path to output file (if left out, result is printed to "
            "command line)"
        ),
        metavar="FILE",
    )

    parser_corpora = subparsers.add_parser(
        "corpora", help="list all valid Quran corpora",
    )
    parser_corpora.add_argument(
        "-o", "--output", help=(
            "path to output file (if left out, result is printed to "
            "command line)"
        ),
        metavar="FILE",
    )

    # If where aren't any arguments to parse
    if len(sys.argv) < 2:
        # Print help message and exit with error
        parser.print_help()
        sys.exit(1)

    # Overwrite the error handler to also print a help message
    # HACK: This is what's known in the biz as a "monkey-patch". Don't
    # worry if it doesn't make sense to you; it makes sense to argparse,
    # and that's all that matters.
    def custom_error_handler(_self: ArgumentParser):
        def wrapper(message: str):
            sys.stderr.write(f"{_self.prog}: error: {message}\n")
            _self.print_help()
            sys.exit(2)
        return wrapper
    parser.error = custom_error_handler(parser)

    # Actually parse and handle the arguments
    args = parser.parse_args()
    if args.command == "search":
        search(args)
    elif args.command == "corpora":
        corpora(args)
    else:
        # This should never happen
        sys.stderr.write(
            f"{parser.prog}: error: unexpected command {args.command!r}"
        )
        parser.print_help()
        sys.exit(1)


def search(args):
    query = args.query
    corpus = args.corpus
    output = args.output

    # If output file isn't specified
    if output is None:
        # Printing will go to command line
        _search(query, corpus)
    # If output file is specificed
    else:
        oldout = sys.stdout
        # Printing will go to output file
        with open(output, "w") as output_file:
            sys.stdout = output_file
            _search(query, corpus)
        sys.stdout = oldout

        print(f"Results printed to: {output}")


def _search(query: str, corpus: str):
    concordance = Concordance(corpus)

    verse_map = defaultdict(list)
    # For each semicolon-separated search term
    for term in query.split(";"):
        # Conduct a search with this term
        term_results = concordance.search(term)

        word_length = len(concordance.text_to_words(term))
        # For each search result
        for index in term_results:
            verse_index = concordance.word_index_to_verse(index)
            # Create mapping between verse index and search result
            verse_map[verse_index].append((index, word_length))

        verse_map[verse_index].sort()

    occurrence_total = 0
    verse_total = 0
    # For each verse which is part of the results
    for (chapter, verse), verse_results in sorted(verse_map.items()):
        verse_total += 1

        # Get info for this verse
        verse_start = concordance.starts[chapter][verse]
        text = concordance.content[chapter][verse]

        # HACK What I want to do is surround each occurrence of a search
        # term with braces (like "In the name {{ of Allah }}"). The most
        # robust way I can think of to do this is to split the text into
        # words, make the replacement, then join the text together.
        text = text.split()
        # NOTE Making the text replacements in reverse ensures that they
        # don't affect the positions of the other terms in the text.
        for index, length in reversed(verse_results):
            occurrence_total += 1

            # Find the starting index of the term
            term_start = 0
            i = index - verse_start
            while i > 0:
                if Concordance.normalize_word(text[term_start]):
                    i -= 1
                term_start += 1

            # Find the ending index of the term
            term_end = term_start + 1
            i = length - 1
            overflow = False
            while i > 0:
                # If the end of the term is past the end of this verse
                if term_end >= len(text):
                    # The term overflows into the next verse
                    overflow = True
                    break
                if Concordance.normalize_word(text[term_end]):
                    i -= 1
                term_end += 1

            if overflow:
                # If there is overflow, surround in braces and display
                # ellipsis at end
                text[term_start:] = [
                    "{{" + " ".join(text[term_start:]) + " ...}}"
                ]
                # TODO Display part of next verse if there is overflow
            else:
                # If there is no overflow, surround in braces
                text[term_start:term_end] = [
                    "{{" + " ".join(text[term_start:term_end]) + "}}"
                ]

        # Rejoin and display the text
        text = " ".join(text)
        print(f"{chapter + 1}:{verse + 1}\t{text}")
        print(f"Occurrences: {occurrence_total}; Verses: {verse_total}")
        print()

    # Report total occurrence and verse count
    print(
        f"Found {occurrence_total} occurrence(s) in {verse_total} "
        f"verse(s)."
    )


def corpora(args):
    for corpus in VALID_CORPORA:
        print(corpus)
