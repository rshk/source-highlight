#!/usr/bin/env python

import textwrap

import click
from pygments import highlight
from pygments.formatters import (
    FORMATTERS, Terminal256Formatter, get_formatter_by_name)
from pygments.lexers import (
    get_all_lexers, get_lexer_by_name, get_lexer_for_filename)
from pygments.styles import get_all_styles


def _add_line_numbers(text):
    line_fmt = '\033[48;5;235m\033[38;5;250m{:5d} \033[0m {}\n'
    return ''.join(
        line_fmt.format(idx + 1, line)
        for (idx, line) in enumerate(text.splitlines()))


def cmd_list_lexers(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    for label, names, ext, mime in get_all_lexers():
        click.echo(
            '\x1b[1m{}\x1b[0m \x1b[36m{}\x1b[0m'
            ' \x1b[38;5;245m({})\x1b[0m \x1b[32m[{}]\x1b[0m'
            .format(label, ' '.join(names), ', '.join(ext),
                    ', '.join(mime)))
    ctx.exit()


def cmd_list_formatters(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    for key, (cl, label, names, ext, desc) in FORMATTERS.items():
        click.echo(
            '\x1b[1m{}\x1b[0m \x1b[36m{}\x1b[0m \x1b[38;5;245m({})\x1b[0m\n'
            '{}\n'
            .format(label, ' '.join(names), ', '.join(ext),
                    textwrap.indent(textwrap.fill(desc, width=66), '    ')))
    ctx.exit()


def cmd_list_styles(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    for name in get_all_styles():
        click.echo(name)
    ctx.exit()


@click.command()
@click.argument('input_file', type=click.File(mode='r'))
@click.option('-l', '--lexer', 'lexer_name')
@click.option('-s', '--style', 'style_name', default='monokai')
@click.option('-f', '--formatter', 'formatter_name', default='terminal256')
@click.option('-n', '--line-numbers', 'line_numbers', default=False,
              is_flag=True)
@click.option('--list-lexers', default=False, is_flag=True,
              is_eager=True, callback=cmd_list_lexers, expose_value=False)
@click.option('--list-styles', default=False, is_flag=True,
              is_eager=True, callback=cmd_list_styles, expose_value=False)
@click.option('--list-formatters', default=False, is_flag=True,
              is_eager=True, callback=cmd_list_formatters, expose_value=False)
def main(input_file, lexer_name, style_name, formatter_name, line_numbers):

    lexer = (get_lexer_by_name(lexer_name) if lexer_name else
             get_lexer_for_filename(input_file.name))
    # formatter = Terminal256Formatter(style=style_name)
    formatter = get_formatter_by_name(formatter_name, style=style_name)

    text = input_file.read()
    text = highlight(text, lexer, formatter)

    if line_numbers:
        text = _add_line_numbers(text)

    num_lines = text.count('\n')
    if num_lines > click.get_terminal_size()[1]:
        click.echo_via_pager(text)
    else:
        click.echo(text)


if __name__ == '__main__':
    main()
