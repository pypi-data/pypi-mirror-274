from jaxtyping import install_import_hook


with install_import_hook("jaxonfunctions", "beartype.beartype"):
    from .rl import value_learning

__all__ = ["value_learning"]
