import pandas
import re
from IPython.display import display


_VALID_METHOD_NAME = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')
_OPTION_ALIASES = {
    'wide': {'display.max_columns': None},
    'long': {'display.max_rows': None},
    'uncut': {'display.max_colwidth': None},
    'imprecise': {'display.precision': 3},
}


def patch(**kwargs):
    def _format_args(opts):
        formatted = []
        for opt in opts:
            if isinstance(opt, dict):
                items = opt.items()
            else:
                items = _OPTION_ALIASES[opt].items()
            for k, v in items:
                formatted += [k, v]
        return formatted

    def _display(self, *opts):
        if opts:
            options = _format_args(opts)
            with pandas.option_context(*options):
                display(self)
        else:
            display(self)

    def _is_valid_method_name(name):
        return bool(_VALID_METHOD_NAME.match(name))

    pandas.core.generic.NDFrame.display = _display
    pandas.core.generic.NDFrame.full = lambda frame: _display(frame, *_OPTION_ALIASES)

    for method_name, opts in {**_OPTION_ALIASES, **kwargs}.items():
        if _is_valid_method_name(method_name):
            # TODO: more robust multi-key custom logic
            setattr(
                pandas.core.generic.NDFrame,
                method_name,
                lambda frame, opts=opts: _display(frame, opts),
            )

__all__ = ['patch']
