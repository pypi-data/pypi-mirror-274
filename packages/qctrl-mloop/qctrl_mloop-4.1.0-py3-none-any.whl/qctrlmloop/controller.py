# Copyright 2024 Q-CTRL. All rights reserved.
#
# Licensed under the Q-CTRL Terms of service (the "License"). Unauthorized
# copying or use of this file, via any medium, is strictly prohibited.
# Proprietary and confidential. You may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#    https://q-ctrl.com/terms
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS. See the
# License for the specific language.

"""
Controller for integration of Boulder Opal automated closed-loop optimizers and M-LOOP.
"""
from __future__ import annotations

from typing import (
    Any,
    Optional,
)
from warnings import warn

import boulderopal as bo
import mloop.learners as mll
import numpy as np
from mloop.controllers import Controller
from mloop.interfaces import Interface
from qctrlcommons.exceptions import QctrlArgumentsValueError
from qctrlcommons.preconditions import check_argument


class BoulderOpalController(Controller):
    """
    Controller for optimizations that uses Boulder Opal automated
    closed-loop optimizers.

    You can use this controller to integrate an experiment managed by
    M-LOOP to a Boulder Opal automated closed-loop optimizer. Notice that
    you need to set up an M-LOOP Interface to your experiment, initiate a
    Boulder Opal session, and define your choice of Boulder Opal automated
    closed-loop optimizer prior to using this class.

    Parameters
    ----------
    interface : mloop.interfaces.Interface
        The M-LOOP interface from where you obtain the cost value of the
        test points.
    optimizer : boulderopal.closed_loop.ClosedLoopOptimizer or str
        The Boulder Opal automated closed-loop optimizer that you want to
        use. It must be a valid optimizer object (either an
        optimizer object or a str that represents the state from a previous optimization run),
        as described in the Boulder Opal reference documentation.
    test_point_count : int or None, optional
        The requested number of test points that the Boulder Opal automated
        closed-loop optimizer generates at each step. If chosen, it must be
        greater than zero. This is a hint only. The Boulder Opal automated
        closed-loop optimizer might choose differently.
    learner : mloop.learners.Learner or None, optional
        The M-LOOP Learner that this controller uses to obtain extra test
        points, before there are enough results to run a step of the
        Boulder Opal automated closed-loop optimizer. Defaults to None, in
        which case this controller uses a `RandomLearner`.
    training_run_count : int, optional
        The minimum number of training points that the controller obtains
        before calling the Boulder Opal automated closed-loop optimizer.
        Defaults to 0, in which case the controller uses the minimum number
        of points that the Boulder Opal automated closed-loop optimizer
        requires.
    interleaved_run_count : int, optional
        The minimum number of test points that the controller obtains from
        the `learner` between two calls of the Boulder Opal automated
        closed-loop optimizer, in addition to the points that Boulder Opal
        requested. Defaults to 0.
    kwargs : dict
        All the extra arguments that the Controller class from M-LOOP
        accepts.
    """

    def __init__(
        self,
        interface: Interface,
        optimizer: bo.closed_loop.ClosedLoopOptimizer | str,
        test_point_count: Optional[int] = None,
        learner: Optional[mll.Learner] = None,
        training_run_count: int = 0,
        interleaved_run_count: int = 0,
        **kwargs,
    ):
        super().__init__(interface, **kwargs)

        # Auxiliary learner, used to get the initial test points before
        # there are enough points to run Boulder Opal automated closed-loop
        # optimization.
        self.learner = learner
        if self.learner is None:
            self.learner = mll.RandomLearner(**self.remaining_kwargs)
        self._update_controller_with_learner_attributes()

        if test_point_count is not None:
            check_argument(
                test_point_count > 0,
                "The value of test_point_count must be greater than zero.",
                {"test_point_count": test_point_count},
            )

        self._test_point_count = test_point_count

        if isinstance(optimizer, str):
            minimum_training_run_count = 0
        elif isinstance(optimizer, bo.closed_loop.GaussianProcess):
            minimum_training_run_count = 2
        elif isinstance(optimizer, bo.closed_loop.Cmaes):
            minimum_training_run_count = 4 + np.floor(
                3 * np.log(self.learner.num_params)
            )
        else:
            minimum_training_run_count = 2 * self.learner.num_params
            if not isinstance(
                optimizer,
                (bo.closed_loop.NeuralNetwork, bo.closed_loop.SimulatedAnnealing),
            ):
                warn(
                    f"Unrecognized optimizer {optimizer}, falling back to "
                    f"{minimum_training_run_count} as the minimum number of "
                    "training runs."
                )

        self._training_run_count = max(training_run_count, minimum_training_run_count)

        check_argument(
            interleaved_run_count >= 0,
            "The value of interleaved_run_count must not be negative.",
            {"interleaved_run_count": interleaved_run_count},
        )

        self._interleaved_run_count = interleaved_run_count

        self._optimizer = optimizer

    def _call_boulder_opal(self, cost_function_results: Any) -> list[np.ndarray]:
        """
        Manages each call to Boulder Opal.
        """
        result = bo.closed_loop.step(
            optimizer=self._optimizer,
            results=cost_function_results,
            test_point_count=self._test_point_count,
        )

        self._optimizer = result["state"]

        return list(result["test_points"])

    def _transform_cost(self) -> float | np.ndarray:
        """
        Adapts the cost values according to the needs of each learner.
        """
        cost = self.curr_cost

        if self.curr_bad:
            cost = float("inf")

        return cost

    def _optimization_routine(self):
        """
        The main optimization routine.

        This overrides a method from the parent class in M-LOOP.
        """
        current_parameters: list[Any] = []
        current_costs: list[Any] = []
        current_uncertainties: list[Any] = []
        boulder_opal_parameters: list[np.ndarray] = []

        # Number of costs obtained before this function calls the Boulder
        # Opal automated closed-loop optimizer.
        required_run_count = self._training_run_count

        while self.check_end_conditions():
            # Call Boulder Opal only if the number of required runs has
            # been reached and there is at least one result to pass.
            if (self.num_in_costs >= required_run_count) and (
                len(current_parameters) > 0
            ):
                boulder_opal_parameters = self._call_boulder_opal(
                    bo.closed_loop.Results(
                        parameters=np.asarray(current_parameters),
                        costs=np.asarray(current_costs),
                        cost_uncertainties=np.asarray(current_uncertainties),
                    )
                )
                current_parameters = []
                current_costs = []
                current_uncertainties = []
                # The total number of runs before the next call to Boulder
                # Opal, which is: the current number of runs, plus the
                # number of runs that Boulder Opal requested, plus the
                # number of extra interleaved runs that the auxiliary
                # learner requests.
                required_run_count = (
                    self.num_in_costs
                    + len(boulder_opal_parameters)
                    + self._interleaved_run_count
                )

            # Obtain parameters from the Boulder Opal automated closed-loop
            # optimizer if any are available.
            use_boulder_opal_parameters = len(boulder_opal_parameters) > 0
            if use_boulder_opal_parameters:
                parameters = boulder_opal_parameters.pop(0)
            # Use auxiliary learner if the Boulder Opal automated
            # closed-loop optimizer doesn't have more parameters to suggest.
            else:
                parameters = self.learner_params_queue.get()

            # Communicate parameters to the experimental interface, and
            # obtain the results of the cost function.
            self._put_params_and_out_dict(parameters)
            self._get_cost_and_in_dict()

            self.save_archive()

            # Store cost function result in the learner's queue if it was
            # requested by the auxiliary learner.
            if not use_boulder_opal_parameters:
                self.learner_costs_queue.put(
                    (parameters, self._transform_cost(), self.curr_uncer, self.curr_bad)
                )

            # Store cost function result in the list to be used by Boulder Opal.
            if not self.curr_bad:
                current_parameters.append(self.curr_params)
                current_costs.append(self.curr_cost)
                current_uncertainties.append(self.curr_uncer)


def boulder_opal_controller(
    interface: Interface,
    optimizer: bo.closed_loop.ClosedLoopOptimizer,
    test_point_count: Optional[int] = None,
    learner_name: Optional[str] = None,
    training_run_count: int = 0,
    interleaved_run_count: int = 0,
    **kwargs,
) -> BoulderOpalController:
    """
    A helper function to create a `BoulderOpalController` object.

    You can use this to create a `BoulderOpalController` when calling Boulder
    Opal from an M-LOOP configuration file. To do this, add the line
    ``controller_type="qctrlmloop:boulder_opal_controller"`` to the configuration
    file, and follow it with all the parameters that you want to pass to
    this function.

    Parameters
    ----------
    interface : mloop.interfaces.Interface
        The M-LOOP interface from where you obtain the cost value of the
        test points.
    optimizer : bo.closed_loop.ClosedLoopOptimizer
        A closed-loop optimizer from the Boulder Opal package.
    test_point_count : int or None, optional
        The requested number of test points that the Boulder Opal automated
        closed-loop optimizer generates at each step. If chosen, it must be
        greater than zero. This is a hint only. The Boulder Opal automated
        closed-loop optimizer might choose differently.
    learner_name : str or None, optional
        The name of the M-LOOP Learner that this controller uses to obtain
        extra test points, before there are enough results to run a step of
        the Boulder Opal automated closed-loop optimizer. Defaults to
        None, in which case this controller uses a `RandomLearner`.
    training_run_count : int, optional
        The minimum number of training points that the controller obtains
        before calling the Boulder Opal automated closed-loop optimizer.
        Defaults to 0, in which case the controller uses the minimum number
        of points that the Boulder Opal automated closed-loop optimizer
        requires.
    interleaved_run_count : int, optional
        The minimum number of test points that the controller obtains from
        the learner between two calls of the Boulder Opal automated
        closed-loop optimizer, in addition to the points that Boulder Opal
        requested. Defaults to 0.
    **kwargs : dict
        All the extra arguments that the Controller class from M-LOOP
        accepts.

    Returns
    -------
    BoulderOpalController
        The controller that integrates Boulder Opal with M-LOOP.

    Raises
    ------
    QctrlArgumentsValueError
        Raised if the provided `learner_name` doesn't match a valid object class.
    """
    # Create Learner object.
    learner: Optional[mll.Learner] = None
    if learner_name is not None:
        try:
            learner_class = getattr(mll, learner_name)
        except AttributeError as exception:
            raise QctrlArgumentsValueError(
                f"Unable to find learner class mloop.learners.{learner_name}.",
                {"learner_name": learner_name},
            ) from exception
        learner = learner_class(**kwargs)

    return BoulderOpalController(
        interface=interface,
        optimizer=optimizer,
        test_point_count=test_point_count,
        learner=learner,
        training_run_count=training_run_count,
        interleaved_run_count=interleaved_run_count,
        **kwargs,
    )
