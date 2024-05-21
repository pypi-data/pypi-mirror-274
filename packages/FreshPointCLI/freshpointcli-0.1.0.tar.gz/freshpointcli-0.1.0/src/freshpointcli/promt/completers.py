import shlex
import typing

from prompt_toolkit.completion import Completer, Completion, CompleteEvent
from prompt_toolkit.document import Document
from unidecode import unidecode

from freshpointsync import Product

from .parsers import QueryParser


class QueryCompleter(Completer):

    def __init__(self, products: typing.Iterable[Product]) -> None:
        self.product_names = self._get_product_names(products)
        self.product_categories = self._get_product_categories(products)
        self.parser_argnames = self._get_parser_argnames()
        self.positional_name_encountered: bool = False

    def _get_product_names(
        self, products: typing.Iterable[Product]
    ) -> dict[str, str]:
        names = {}
        for product in products:
            if product.name:
                name_lowercase_ascii = product.name_lowercase_ascii
                if name_lowercase_ascii not in names:
                    names[name_lowercase_ascii] = product.name
        return names

    def _get_product_categories(
        self, products: typing.Iterable[Product]
    ) -> dict[str, str]:
        categories = {}
        for product in products:
            if product.category:
                category_lowercase_ascii = product.category_lowercase_ascii
                if category_lowercase_ascii not in categories:
                    categories[category_lowercase_ascii] = product.category
        return categories

    def _get_parser_argnames(self) -> dict[str, str]:
        return {short: full for short, full in QueryParser().optional_args}

    def yield_argname(self, text: str):
        for short, full in self.parser_argnames.items():
            if text in short or text in full:
                start_position = -len(text)
                if text == full:
                    start_position = start_position - 1
                yield Completion(
                    full,
                    start_position=start_position,
                    display=full,
                    )

    def yield_name(self, text: str):
        for name_lowercase_ascii in self.product_names:
            if text.strip('\'"') in name_lowercase_ascii:
                name = self.product_names[name_lowercase_ascii]
                yield Completion(
                    f'"{name}"',
                    start_position=-len(text),
                    display=name,
                    )

    def yield_category(self, text: str):
        for category_lowercase_ascii in self.product_categories:
            if text.strip('\'"') in category_lowercase_ascii:
                category = self.product_categories[category_lowercase_ascii]
                yield Completion(
                    f'"{category}"',
                    start_position=-len(text),
                    display=category
                    )

    def yield_completions(self, text: str, text_prev: typing.Optional[str]):
        if text_prev:  # suggest completions based on previous argument
            if text_prev.startswith('-'):
                if text_prev in ['-n', '--name']:
                    yield from self.yield_name(text)
                elif text_prev in ['-c', '--category']:
                    yield from self.yield_category(text)
                elif text_prev in [  # a number is expected after these
                    '-pmin', '--price-min', '-pmax', '--price-max',
                    '-qmin', '--quantity-min', '-qmax', '--quantity-max'
                ]:
                    return
        if text.startswith('-'):  # suggest -a and --arg completions
            yield from self.yield_argname(text)
        else:  # suggest name completions if was not suggested before
            if self.positional_name_encountered:
                return
            yield from self.yield_name(text)

    def format_text(self, text: str) -> str:
        return unidecode(text).casefold()

    def split_text(self, text: str) -> list[str]:
        try:
            args = shlex.split(text, posix=False)
            if len(args) > 1:
                last_two_args_concat = args[-2] + args[-1]
                if text.endswith(last_two_args_concat):
                    args[-2] = last_two_args_concat
                    del args[-1]
        except ValueError:
            try:
                args = shlex.split(f'{text}"', posix=False)
                if args and args[-1] and args[-1][-1] == '"':
                    args[-1] = args[-1][:-1]
            except ValueError:
                try:
                    args = shlex.split(f'{text}\'', posix=False)
                    if args and args[-1] and args[-1][-1] == '\'':
                        args[-1] = args[-1][:-1]
                except ValueError:  # should not happen
                    return []
        if text.endswith(' '):
            args.append('')
        return args

    def get_last_two_args(self, text: str) -> tuple[str, str]:
        text_formatted = unidecode(text).casefold()
        args = self.split_text(text_formatted)
        try:
            arg_last, arg_prev = args[-1], args[-2]
            self.positional_name_encountered = True
        except IndexError:
            self.positional_name_encountered = False
            try:
                arg_last, arg_prev = args[-1], ''
            except IndexError:  # should not happen
                arg_last, arg_prev = '', ''
        return arg_last, arg_prev

    def get_completions(self, document: Document, event: CompleteEvent):
        text = document.text_before_cursor
        arg_last, arg_prev = self.get_last_two_args(text)
        yield from self.yield_completions(arg_last, arg_prev)
