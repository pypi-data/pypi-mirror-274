# roms/_nonparametric.py
"""Nonparametric ROM classes."""

__all__ = [
    "ROM",
]

# import warnings

from .. import (
    # pre,
    # basis as _basis,
    # ddt,
    models,
    # lstsq,
    # errors,
)


class ROM:
    """Nonparametric reduced-order model class.

    Parameters
    ----------
    lifter
    transformer
    basis
    ddt_estimator
        Function for estimating time derivatives of the training states.
        Must obey the following syntax.

        .. code-block:: python
           >>> states, ddts, inputs = ddt_func(states, inputs)

    model
    solver (or make this part of the model?
    """

    def __init__(
        self,
        *,
        lifter=None,
        transformer=None,
        basis=None,
        ddt_estimator=None,
        model=None,
        solver=None,
    ):
        """Store each argument as an attribute."""
        self.__lifter = lifter
        self.__transformer = transformer
        self.__basis = basis
        self.__ddter = ddt_estimator
        self.__model = model
        self.__solver = solver

    # Properties --------------------------------------------------------------
    @property
    def lifter(self):
        return self.__lifter

    @property
    def transformer(self):
        return self.__transformer

    @property
    def basis(self):
        return self.__basis

    @property
    def ddt_estimator(self):
        return self.__ddter

    @property
    def model(self):
        return self.__model

    @property
    def iscontinuous(self):
        return isinstance(self.model, models.ContinuousModel)

    @property
    def solver(self):
        return self.__solver

    # Printing ----------------------------------------------------------------
    def __str__(self):
        """String representation."""
        lines = ["Nonparametric reduced-order model"]

        def indent(text):
            return "\n".join("\t" + line for line in text.rstrip().split("\n"))

        def addfuncstr(label, func):
            if func is not None:
                lines.append(f"{label} function: {func.__name__}()")

        def addobjstr(label, obj):
            if obj is not None:
                lines.append(f"{label}:")
                lines.append(indent(str(obj)))

        addfuncstr("Lifting", self.lifter)
        addfuncstr("Unlifting", self.unlifter)
        addobjstr("Transformer", self.transformer)
        addobjstr("Basis", self.basis)
        addfuncstr("Time derivative function", self.ddt_func)
        addobjstr("Model", self.model)
        addobjstr("Solver", self.solver)

        return "\n".join(lines)

    def __repr__(self):
        return str(self)

    # Training ----------------------------------------------------------------
    def fit(self, states, lhs=None, inputs=None):
        if self.transformer is not None:
            states = self.transformer.fit_transform(states)

        if self.basis is not None:
            states = self.basis.fit(states).compress(states)

        # If
        if lhs is not None:
            lhs = self.basis.compress(self.transformer.transform(lhs))

        # Time derivatives (if not provided).
        elif isinstance(self.model, models.ContinuousModel):
            if lhs is None and self.ddt_func is not None:
                states, lhs, inputs = self.ddt_func(states)
            else:
                raise ValueError(
                    "state time derivatives required as argument 'lhs' "
                    "because since 'ddt_func' not provided"
                )

    # Evaluation --------------------------------------------------------------
