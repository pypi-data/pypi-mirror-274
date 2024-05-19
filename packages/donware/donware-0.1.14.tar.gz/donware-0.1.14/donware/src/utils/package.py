from terminal import banner
from rich import print
import inspect


def inspect_package(package):
    """
    Lists all functions within a given package along with their docstrings.

    This function uses the `inspect` module to retrieve all functions from the
    specified package. For each function, it prints the function name and its
    corresponding docstring. If a function does not have a docstring, it will
    indicate that no docstring is available.

    Args:
        package (module): The package from which to list functions and their docstrings.

    Returns:
        None
    """
    functions = inspect.getmembers(package, inspect.isfunction)
    for index, (function_name, function_obj) in enumerate(functions, start=1):
        docstring = function_obj.__doc__ or "No docstring available"
        banner(f"{index}. Function: {function_name}", text_position="LEFT")
        print(f"Docstring: {docstring}\n")
