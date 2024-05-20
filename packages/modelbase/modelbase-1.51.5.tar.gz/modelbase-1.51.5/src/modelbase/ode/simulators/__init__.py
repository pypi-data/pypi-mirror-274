from __future__ import annotations

__all__ = [
    "BASE_MODEL_TYPE",
    "RATE_MODEL_TYPE",
    "Simulator",
    "_AbstractRateModel",
    "_AbstractStoichiometricModel",
    "_BaseRateSimulator",
    "_BaseSimulator",
    "_LabelSimulate",
    "_LinearLabelSimulate",
    "_Simulate",
]

import warnings
from typing import Dict, List, Type, Union, overload

from ...typing import Array, ArrayLike
from ..integrators import AbstractIntegrator, Scipy
from ..models import BASE_MODEL_TYPE, RATE_MODEL_TYPE
from ..models import LabelModel as _LabelModel
from ..models import LinearLabelModel as _LinearLabelModel
from ..models import Model as _Model
from ..models import _AbstractRateModel, _AbstractStoichiometricModel
from .abstract_simulator import _BaseRateSimulator, _BaseSimulator
from .labelsimulator import _LabelSimulate
from .linearlabelsimulator import _LinearLabelSimulate
from .simulator import _Simulate

try:
    from ..integrators import Assimulo

    default_integrator: Type[AbstractIntegrator] = Assimulo
except ImportError:  # pragma: no cover
    warnings.warn("Assimulo not found, disabling sundials support.")
    default_integrator = Scipy


@overload
def Simulator(model: _Model) -> _Simulate:
    ...


@overload
def Simulator(model: _LabelModel) -> _LabelSimulate:
    ...


@overload
def Simulator(model: _LinearLabelModel) -> _LinearLabelSimulate:
    ...


def Simulator(
    model: Union[_LabelModel, _LinearLabelModel, _Model],
    integrator: Type[AbstractIntegrator] = default_integrator,
    y0: ArrayLike | None = None,
    time: List[Array] | None = None,
    results: List[Array] | None = None,
    parameters: List[Dict[str, float]] | None = None,
) -> Union[_LabelSimulate, _LinearLabelSimulate, _Simulate]:
    """Choose the simulator class according to the model type.

    If a simulator different than assimulo is required, it can be chosen
    by the integrator argument.

    Parameters
    ----------
    model : modelbase.model
        The model instance

    Returns
    -------
    Simulate : object
        A simulate object according to the model type
    """
    if isinstance(model, _LabelModel):
        return _LabelSimulate(
            model=model,
            integrator=integrator,
            y0=y0,
            time=time,
            results=results,
            parameters=parameters,
        )
    if isinstance(model, _LinearLabelModel):
        return _LinearLabelSimulate(
            model=model,
            integrator=integrator,
            y0=y0,
            time=time,
            results=results,
        )
    if isinstance(model, _Model):
        return _Simulate(
            model=model,
            integrator=integrator,
            y0=y0,
            time=time,
            results=results,
            parameters=parameters,
        )
    raise NotImplementedError
