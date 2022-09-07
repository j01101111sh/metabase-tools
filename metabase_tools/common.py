# """Module for common tools used throughout the project
# """

# import logging
# from functools import wraps
# from typing import Any, Callable, TypeVar

# T = TypeVar("T")


# def log_call(func: Callable[..., T]) -> Callable[..., T]:
#     """Used to log calls to the function provided"""

#     @wraps(func)
#     def wrapper(*args: Any, **kwargs: Any) -> T:
#         logging.debug(
#             "%s called\n\targs: %s\n\tkwargs: %s",
#             func.__name__,
#             "\n\t\t".join([str(s) for s in args]),
#             "\n\t\t".join(
#                 [f"{key}: {value}" for key, value in kwargs.items()],
#             ),
#         )
#         return func(*args, **kwargs)

#     return wrapper


# def untested(func: Callable[..., T]) -> Callable[..., T]:
#     """Used to log a warning that the decorated function has not been tested"""

#     @wraps(func)
#     def wrapper(*args: Any, **kwargs: Any) -> T:
#         logging.warning("Calling untested function: %s", func.__name__)
#         return func(*args, **kwargs)

#     return wrapper
