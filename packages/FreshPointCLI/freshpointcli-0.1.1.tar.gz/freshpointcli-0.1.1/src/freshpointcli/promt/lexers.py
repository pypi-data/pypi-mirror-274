from pygments.lexer import RegexLexer
from pygments.token import Text, String, Number, Error, Keyword, Token
from prompt_toolkit.lexers import PygmentsLexer  # noqa: F401


# custom tokens
Keyword.Flag = Token.Keyword.Flag  # type: ignore

# nested Price and Quantity tokens under OneArg
Keyword.Flag.Price = Token.Keyword.Flag.Price  # type: ignore
Keyword.Flag.Price.Max = Token.Keyword.Flag.Price.Max  # type: ignore
Keyword.Flag.Price.Min = Token.Keyword.Flag.Price.Min  # type: ignore

Keyword.Flag.Quantity = Token.Keyword.Flag.Quantity  # type: ignore
Keyword.Flag.Quantity.Max = Token.Keyword.Flag.Quantity.Max  # type: ignore
Keyword.Flag.Quantity.Min = Token.Keyword.Flag.Quantity.Min  # type: ignore


class QueryLexer(RegexLexer):
    name = 'QueryLexer'
    aliases = ['querylexer']
    tokens = {
        'root': [
            (r'\s*(-pmax|--price-max)\s*', Keyword.Flag.Price.Max, 'nonnegfloat'),      # noqa
            (r'\s*(-pmin|--price-min)\s*', Keyword.Flag.Price.Min, 'nonnegfloat'),      # noqa
            (r'\s*(-qmax|--quantity-max)\s*', Keyword.Flag.Quantity.Max, 'nonengint'),  # noqa
            (r'\s*(-qmin|--quantity-min)\s*', Keyword.Flag.Quantity.Min, 'nonengint'),  # noqa
            (r'(\s+|^)-\w+(?=\s|$)', Keyword.Flag),            # short flags
            (r'(\s+|^)--\w+[\w+\d-]*(?=\s|$)', Keyword.Flag),  # long flags
            (r'"[^"]*"', String.Double),
            (r"'[^']*'", String.Single),
            (r'\b-?\d+\.\d+\b', Number.Float),
            (r'\b-?\d+\b', Number.Integer),
            (r'.|\s', Text),
        ],
        'nonengint': [
            (r'\d+(?=\s|$)', Number.Integer, '#pop'),
            (r'\S+', Error, '#pop'),
        ],
        'nonnegfloat': [
            (r'\d+(?=\s|$)', Number.Integer, '#pop'),
            (r'\d+\.\d*(?=\s|$)', Number.Float, '#pop'),
            (r'\S+', Error, '#pop'),
        ],
    }
