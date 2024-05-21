import argparse
import shlex
import typing

from functools import lru_cache
from unidecode import unidecode

from freshpointsync import Product


@lru_cache(maxsize=4096)
def format_str(s: typing.Any) -> str:
    return unidecode(str(s)).strip().casefold()


T = typing.TypeVar('T', int, float)


class ArgTypes:
    @staticmethod
    def nonnegative_number(value: typing.Any, type_cls: typing.Type[T]) -> T:
        try:
            value_converted = type_cls(value)
        except Exception as e:
            raise ValueError(f'Value "{value}" is not a valid number') from e
        if value_converted < 0:
            raise ValueError(f'Value "{value}" cannot be negative')
        return value_converted

    @classmethod
    def nonnegative_float(cls, value: typing.Any) -> float:
        return cls.nonnegative_number(value, float)

    @classmethod
    def nonnegative_int(cls, value: typing.Any) -> int:
        if not str(value).isdigit():
            raise ValueError(f'Value "{value}" is not an integer')
        return cls.nonnegative_number(value, int)


def parse_args_init() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'location_id',
        nargs='?',
        type=ArgTypes.nonnegative_int,
        help="Product location (page ID)"
        )
    return parser.parse_args()


class QueryParserHelpFormatter(argparse.HelpFormatter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, max_help_position=52)


class QueryParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        if 'formatter_class' not in kwargs:
            kwargs['formatter_class'] = QueryParserHelpFormatter
        super().__init__(*args, **kwargs)
        self._add_arguments_init()

    def _add_arguments_init(self) -> None:
        group_name = self.add_mutually_exclusive_group()
        group_name.add_argument(
            'positional_name',
            nargs='?',
            help="Product name. Use this for a quick search by name, or omit it and use --name when specifying additional parameters."  # noqa
            )
        group_name.add_argument(
            '-n',
            '--name',
            help="Product name, use when specifying additional parameters. Mutually exclusive with the direct product name positional argument."  # noqa
            )
        self.add_argument(
            '-c',
            '--category',
            help="Product category"
            )
        self.add_argument(
            '-qmin',
            '--quantity-min',
            type=ArgTypes.nonnegative_int,
            help="Minimum number of available products (in pieces)"
            )
        self.add_argument(
            '-qmax',
            '--quantity-max',
            type=ArgTypes.nonnegative_int,
            help="Maximum number of available products (in pieces)"
            )
        self.add_argument(
            '-pmin',
            '--price-min',
            type=ArgTypes.nonnegative_float,
            help="Lowest product price"
            )
        self.add_argument(
            '-pmax',
            '--price-max',
            type=ArgTypes.nonnegative_float,
            help="Highest product price"
            )
        self.add_argument(
            '-a',
            '--available',
            action='store_true',
            help="Product is currently in stock"
            )
        self.add_argument(
            '-s',
            '--sale',
            action='store_true',
            help="Product is on sale"
            )
        self.add_argument(
            '-g',
            '--glutenfree',
            action='store_true',
            help="Product is gluten free"
            )
        self.add_argument(
            '-v',
            '--vegetarian',
            action='store_true',
            help="Product is vegetarian"
            )
        self.add_argument(
            '-sd',
            '--setdefault',
            action='store_true',
            help="Set the default query"
            )

    @property
    def optional_args(self) -> list[tuple[str, str]]:
        optional_args = []
        for action in self._actions:
            if len(action.option_strings) == 2:
                short, full = action.option_strings
            elif len(action.option_strings) == 1:
                arg = action.option_strings[0]
                short, full = arg, arg
            else:  # empty or more than 2 option strings, should not happen
                continue
            optional_args.append((short, full))
        return optional_args

    @staticmethod
    def split_args(args: str) -> list[str]:
        try:
            return shlex.split(args)
        except ValueError:
            try:
                return shlex.split(f'{args}"')
            except ValueError:
                try:
                    return shlex.split(f'{args}\'')
                except Exception:  # should not happen
                    return []

    def parse_args(  # type: ignore[override]
        self,
        args: typing.Optional[typing.Sequence[str]] = None,
        namespace: typing.Optional[argparse.Namespace] = None,
    ) -> argparse.Namespace:
        parsed_args = super().parse_args(args=args, namespace=namespace)
        if parsed_args is None:
            raise SystemExit
        parsed_args.name = parsed_args.name or parsed_args.positional_name
        delattr(parsed_args, 'positional_name')
        return parsed_args

    def parse_args_safe(
        self,
        args: typing.Optional[typing.Sequence[str]] = None,
        namespace: typing.Optional[argparse.Namespace] = None,
    ) -> typing.Optional[argparse.Namespace]:
        try:
            return self.parse_args(args, namespace)
        except SystemExit:
            return None


def get_constraints(
    args: argparse.Namespace
) -> list[typing.Callable[[Product], bool]]:
    constraints: list[typing.Callable[[Product], bool]] = []
    if args.name is not None:
        constraints.append(
            lambda p: format_str(args.name) in p.name_lowercase_ascii
            )
    if args.category is not None:
        constraints.append(
            lambda p: format_str(args.category) in p.category_lowercase_ascii
            )
    if args.quantity_min is not None:
        constraints.append(lambda p: p.quantity >= args.quantity_min)
    if args.quantity_max is not None:
        constraints.append(lambda p: p.quantity <= args.quantity_max)
    if args.price_min is not None:
        constraints.append(lambda p: p.price_curr >= args.price_min)
    if args.price_max is not None:
        constraints.append(lambda p: p.price_curr <= args.price_max)
    if args.available:
        constraints.append(lambda p: p.is_available)
    if args.sale:
        constraints.append(lambda p: p.is_on_sale)
    if args.glutenfree:
        constraints.append(lambda p: p.is_gluten_free)
    if args.vegetarian:
        constraints.append(lambda p: p.is_vegetarian)
    return constraints
