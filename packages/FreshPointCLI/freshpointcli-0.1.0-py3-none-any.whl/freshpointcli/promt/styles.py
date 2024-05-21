import enum

from pygments.style import Style as PygmentsStyle
from pygments.token import Number, Error, Text, Keyword, String
from prompt_toolkit.styles import Style as PromptToolkitStyle
from prompt_toolkit.styles import style_from_pygments_cls, merge_styles


class AppColors(enum.Enum):
    DEFAULT = "default"
    FRESHPOINT = "#78BC2C"
    GREEN = "#30BC2C"
    YELLOW = "#BCB82C"
    RED = "#BC2C30"
    TEAL = "#2CBCB8"
    BLUE = "#2C30BC"
    PURPLE = "#702CBC"
    GRAY = "#9E9E9E"
    GRAY_DARK = "#333333"


class FreshpointPygmentsStyle(PygmentsStyle):
    default_style = ""
    styles = {
        Text:                      "",

        Keyword:                   AppColors.TEAL.value,
        Keyword.Flag:              "",
        Keyword.Flag.Price:        "",
        Keyword.Flag.Price.Max:    "",
        Keyword.Flag.Price.Min:    "",
        Keyword.Flag.Quantity:     "",
        Keyword.Flag.Quantity.Max: "",
        Keyword.Flag.Quantity.Min: "",

        String:                    AppColors.YELLOW.value,
        String.Double:             "",
        String.Single:             "",

        Number:                    AppColors.GREEN.value,
        Number.Float:              "",
        Number.Integer:            "",

        Error:                     AppColors.RED.value
    }


FreshpointPromptToolkitStyle = PromptToolkitStyle.from_dict(
    {
        "app_name":
            f"bg:{AppColors.DEFAULT.value} fg:{AppColors.FRESHPOINT.value}",
        "at":
            f"bg:{AppColors.DEFAULT.value} fg:{AppColors.DEFAULT.value}",
        "location":
            f"bg:{AppColors.DEFAULT.value} fg:{AppColors.YELLOW.value}",
        "prompt_arrow":
            f"bg:{AppColors.DEFAULT.value} fg:{AppColors.DEFAULT.value}",
        "completion-menu.completion":
            f"bg:{AppColors.GRAY.value} fg:{AppColors.GRAY_DARK.value}",
        "completion-menu.completion.current":
            f"bg:{AppColors.DEFAULT.value} fg:{AppColors.YELLOW.value}",
        "scrollbar.background":
            f"bg:{AppColors.GRAY_DARK.value} fg:{AppColors.DEFAULT.value}",
        "scrollbar.button":
            f"bg:{AppColors.FRESHPOINT.value} fg:{AppColors.DEFAULT.value}",
    }
)


FreshpointStyle = merge_styles(
    [
        style_from_pygments_cls(FreshpointPygmentsStyle),
        FreshpointPromptToolkitStyle,
    ]
)
