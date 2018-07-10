#ifndef _EXOPLANET_KEPLER_H_
#define _EXOPLANET_KEPLER_H_

#include <cmath>

#include "exoplanet/cuda_utils.h"

namespace exoplanet {
  namespace kepler {

    template <typename T>
    EXOPLANET_CUDA_CALLABLE
    inline T solve_kepler (T M, T e, int maxiter, float tol) {
      T E0 = M, E = M;
      if (fabs(e) < tol) return E;
      for (int i = 0; i < maxiter; ++i) {
        T g = E0 - e * sin(E0) - M, gp = 1.0 - e * cos(E0);
        E = E0 - g / gp;
        if (fabs((E - E0) / E) <= T(tol)) {
          return E;
        }
        E0 = E;
      }
      return E;
    }

  };
};

#endif