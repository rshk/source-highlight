Source highlight
################

Simple tool to show code with syntax highlight.

Based on `pygments <http://pygments.org/>`_.
Also uses `click <http://click.pocoo.org/6/>`_, so make sure you have
those two installed.

It's a single-file project, so copy it anywhere. I have it symlinked
as ``~/bin/hl``.


Usage
=====


::

    ./source_highlight.py -n ./source_highlight.py

Will display its own source code, with syntax highlight, using a pager.

The ``-n`` option enables showing line numbers.

File format is guessed by extension, but you can tweak things::

    % hl --help
    Usage: hl [OPTIONS] INPUT_FILE

    Options:
      -l, --lexer TEXT
      -s, --style TEXT
      -f, --formatter TEXT
      -n, --line-numbers
      --list-lexers
      --list-styles
      --list-formatters
      --help                Show this message and exit.
