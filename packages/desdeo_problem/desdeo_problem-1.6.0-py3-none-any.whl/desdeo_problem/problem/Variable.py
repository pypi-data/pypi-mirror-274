"""Desdeo-problem variable related definitions.

This file includes definition of Variable class (with initial and current
values and value bounds), variable_builder, and error classes for Variable
and VariableBuilder.
"""
import numpy as np


class VariableError(Exception):
    """Raised when an error is encountered during the handling of the
    Variable objects.

    """


class VariableBuilderError(Exception):
    """Raised when an error is encountered during the handling of the
    Variable objects.

    """


class Variable:
    """Simple variable with a name, initial value and bounds.

    Arguments:
        name (str): Name of the variable
        initial_value (float): The initial value of the variable.
        lower_bound (float, optional): Lower bound of the variable. Defaults
            to negative infinity.
        upper_bound (float, optional): Upper bound of the variable. Defaults
            to positive infinity.

    Attributes:
        name (str): Name of the variable.
        initial_value (float): Initial value of the variable.
        lower_bound (float): Lower bound of the variable.
        upper_bound (float): Upper bound of the variable.
        current_value (float): The current value the variable holds.

    Raises:
        VariableError: Bounds are incorrect.

    """

    def __init__(
        self, name: str, initial_value: float, lower_bound: float = -np.inf, upper_bound: float = np.inf
    ) -> None:
        self.__name: str = name
        self.__initial_value: float
        self.__lower_bound: float
        self.__upper_bound: float
        self.__current_value: float  # NOTE: This is probably a useless attr
        # Check that the bounds make sense
        if not (lower_bound < upper_bound):
            msg = f"Lower bound {lower_bound} should be less than the upper bound {upper_bound}."
            raise VariableError(msg)

        # Check that the initial value is between the bounds
        if not (lower_bound <= initial_value <= upper_bound):
            msg = (
                f"The initial value {initial_value} should be between"
                f"the upper ({upper_bound}) and lower ({lower_bound}) bounds."
            )
            raise VariableError(msg)

        self.__lower_bound = lower_bound
        self.__upper_bound = upper_bound
        self.__initial_value = initial_value
        self.__current_value = initial_value

    @property
    def name(self) -> str:
        """Property: name

        Returns:
            str: The name of the variable.
        """
        return self.__name

    @property
    def initial_value(self) -> float:
        """Property: initial_value

        Returns:
            float: The initial value of the variable.
        """
        return self.__initial_value

    @property
    def current_value(self) -> float:
        """Property: current_value

        Returns:
            float: The current value of the variable
        """
        return self.__current_value

    @current_value.setter
    def current_value(self, value: float):
        """Setter: current_value

        Args:
            float: The updated value for the current_value variable.

        """
        self.__current_value = value

    def get_bounds(self) -> tuple[float, float]:
        """Return the bounds of the variables as a tuple.

        Returns:
            tuple(float, float): A tuple consisting of (lower_bound,
                upper_bound)

        """
        return (self.__lower_bound, self.__upper_bound)


def variable_builder(
    names: list[str],
    initial_values: list[float] | np.ndarray,
    lower_bounds: list[float] | np.ndarray | None = None,
    upper_bounds: list[float] | np.ndarray | None = None,
) -> list[Variable]:
    """Automatically build all variable objects.

    Arguments:
        names (List[str]): Names of the variables
        initial_values (np.ndarray): Initial values taken by the variables.
        lower_bounds (Union[List[float], np.ndarray], optional): Lower bounds of the
            variables. If None, it defaults to negative infinity. Defaults to None.
        upper_bounds (Union[List[float], np.ndarray], optional): Upper bounds of the
            variables. If None, it defaults to positive infinity. Defaults to None.

    Raises:
        VariableError: Lengths of the input arrays are different.

    Returns:
        List[Variable]: List of variable objects
    """
    # assert that all inputs have the same size
    num_of_variables = len(names)
    if initial_values is None:
        initial_values = [None] * num_of_variables
    if num_of_variables != len(initial_values):
        msg = (
            "The length of the list of names and the number of elements in the "
            "initial_values array should be the same"
        )
        raise VariableBuilderError(msg)
    if lower_bounds is None:
        lower_bounds = [-np.inf] * num_of_variables
    if num_of_variables != len(lower_bounds):
        msg = (
            "The length of the list of names and the number of elements in the " "lower_bounds array should be the same"
        )
        raise VariableBuilderError(msg)
    if upper_bounds is None:
        upper_bounds = [np.inf] * num_of_variables
    if num_of_variables != len(upper_bounds):
        msg = (
            "The length of the list of names and the number of elements in the " "upper_bounds array should be the same"
        )
        raise VariableBuilderError(msg)
    # if most checks passed
    variables = [
        Variable(*var_data) for var_data in zip(names, initial_values, lower_bounds, upper_bounds, strict=True)
    ]
    return variables
