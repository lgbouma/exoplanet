#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function

import numpy as np
from pymc3.step_methods.step_sizes import DualAverageAdaptation

__all__ = ["WindowedDualAverageAdaptation"]


class WindowedDualAverageAdaptation(DualAverageAdaptation):
    def __init__(self, update_steps, initial_step, target, *args, **kwargs):
        self.update_steps = np.atleast_1d(update_steps).astype(int)
        self.targets = np.atleast_1d(target) + np.zeros_like(self.update_steps)
        super(WindowedDualAverageAdaptation, self).__init__(
            initial_step, self.targets[0], *args, **kwargs
        )
        self._initial_step = initial_step
        self._n_samples = 0
        self.reset()

    def reset(self):
        self.restart()
        self._n_samples = 0

    def restart(self):
        self._hbar = 0.0
        self._log_step = np.log(self._initial_step)
        self._log_bar = self._log_step
        self._count = 1

    def update(self, accept_stat, tune):
        if self._n_samples in self.update_steps:
            self._target = float(
                self.targets[np.where(self.update_steps == self._n_samples)]
            )
            self._n_samples += 1
            self.restart()
            return

        self._n_samples += 1
        super(WindowedDualAverageAdaptation, self).update(accept_stat, tune)
