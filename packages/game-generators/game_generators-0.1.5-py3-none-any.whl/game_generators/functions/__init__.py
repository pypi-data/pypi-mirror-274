from game_generators.functions.ces import ces
from game_generators.functions.cobb_douglas import cobb_douglas
from game_generators.functions.concave import concave
from game_generators.functions.leontief import leontief
from game_generators.functions.linear import linear
from game_generators.functions.monotonic import increasing, decreasing
from game_generators.functions.polynomial import polynomial

available_functions = [
    "ces",
    "cobb_douglas",
    "concave",
    "leontief",
    "linear",
    "increasing",
    "decreasing",
    "polynomial",
]


def generate_function(name, *args, **kwargs):
    """Generate a function."""
    if name == "ces":
        return ces(*args, **kwargs)
    elif name == "cobb_douglas":
        return cobb_douglas(*args, **kwargs)
    elif name == "concave":
        return concave(*args, **kwargs)
    elif name == "leontief":
        return leontief(*args, **kwargs)
    elif name == "linear":
        return linear(*args, **kwargs)
    elif name == "increasing":
        return increasing(*args, **kwargs)
    elif name == "decreasing":
        return decreasing(*args, **kwargs)
    elif name == "polynomial":
        return polynomial(*args, **kwargs)
    else:
        raise ValueError(f"Function {name} not available. Choose one of {available_functions}.")
