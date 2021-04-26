#!/usr/bin/env python3
import json
from functools import lru_cache
from collections import defaultdict, Counter
from pathlib import Path
import re
import sys
from typing import Tuple, Optional
from pygls.capabilities import COMPLETION
from pygls.server import LanguageServer
from pygls.workspace import Document, position_from_utf16
from pygls.lsp.types.basic_structures import Position
from pygls.lsp import (
    CompletionItem,
    CompletionList,
    CompletionOptions,
    CompletionParams,
)

__version__ = "0.0.1"

server = LanguageServer()


def debug(*s):
    print(*s, file=sys.stderr)


def preceding_words(
    document: Document, position: Position
) -> Optional[Tuple[str, str]]:
    """
    Get the word under the cursor returning the start and end positions.
    """
    lines = document.lines
    if position.line >= len(lines):
        return None

    row, col = position_from_utf16(lines, position)
    line = lines[row]
    try:
        a, b = line[:col].strip().split()[-2:]
        return a, b
    except (ValueError):
        return None


@server.feature(COMPLETION, CompletionOptions(trigger_characters=[" "]))
def completions(params: CompletionParams):
    """Returns completion items."""
    document = server.workspace.get_document(params.text_document.uri)
    words = preceding_words(document, params.position)
    debug("Completion", params.text_document.uri, words)
    if not words:
        return None
    ngrams = get_ngrams(server.workspace.root_path)
    candidates = ngrams.get((words[0], words[1]))
    if not candidates:
        debug("No candidates")
        return None
    labels = [candidate[0] for candidate in candidates.most_common(5)]
    debug(labels)
    return CompletionList(
        is_incomplete=False,
        items=[CompletionItem(label=label) for label in labels],
    )


def main():
    server.start_io()


def get_msgstrs(pofile):
    msgstr = None
    with open(pofile) as podata:
        for line in podata:
            if line.startswith("msgstr"):
                msgstr = line[8:-2].replace(r"\"", '"')
                continue
            if msgstr is not None and line[0] == '"':
                msgstr += line[1:-2].replace(r"\"", '"')
                continue
            if msgstr is not None:
                yield msgstr
                msgstr = None


@lru_cache()
def get_ngrams(root_path):
    ngrams = defaultdict(Counter)
    files = Path(root_path.replace("file://", "")).glob("**/*.po")
    for file in files:
        if any(part.startswith(".") for part in file.parts):
            continue
        for entry in get_msgstrs(file):
            words = entry.split()
            for a, b, c in zip(words, words[1:], words[2:]):
                ngrams[(a, b)][c] += 1
    return ngrams


if __name__ == "__main__":
    main()
