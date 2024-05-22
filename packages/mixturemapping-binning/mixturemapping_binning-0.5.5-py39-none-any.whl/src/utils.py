# Copyright 2023 Viktor Krückl. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

# import tensorflow parts
from doctest import OutputChecker
import tensorflow.python.ops
from tensorflow.python.ops import control_flow_ops as _control_flow_ops
import tensorflow as _tf




def getSkleanGM(weights, means, stdOrCov):
    """
    create a Gaussian Mixture Model from Sklearn based on weights, means and stdDev or covariances

    Parameters:
        weights:      array-like, shape (n_components,)
                      The weights of each mixture components.

        means:       array-like, shape (n_components, n_features)
                     The mean of each mixture component.

        stdOrCov:    array-like, shape (n_components, n_features) or  (n_components, n_features, n_features)
                     The standard deviations or the covariaes of the mixture

    """

    # import numpy parts
    from numpy import square as _square
    from numpy import shape as _shape

    # import sklean parts
    from sklearn.mixture import GaussianMixture as _skGM
    from sklearn.mixture._gaussian_mixture import _compute_precision_cholesky as _skGM_compute_precision_cholesky    

    if(len(_shape(means)) != len(_shape(stdOrCov))):
        if _shape(means)[-1] == _shape(stdOrCov)[-1] and _shape(means)[-1] == _shape(stdOrCov)[-2] and _shape(means)[0] == _shape(stdOrCov)[0]:
            covariance_type='full'
            covar = stdOrCov
        else:
            raise "Full covariance matrices not implemented yet?"
    else:
        covariance_type='diag'
        covar = _square(stdOrCov)
        

    # extract the component size
    n_components = _shape(means)[-2]

    # initialize gaussian mixture
    mix = _skGM(n_components, covariance_type=covariance_type)
    mix.means_ = means
    mix.weights_ = weights
    mix.covariances_ = covar
    mix.precisions_cholesky_ = _skGM_compute_precision_cholesky(mix.covariances_, mix.covariance_type)

    return mix


def lastEntryJacobian(ys, xs, use_pfor=True, parallel_iterations=None, name='Jacobian', stop_gradients=None):
    """ Constructs the Jacobi Matrix based of the last entries of `ys(xs)` w.r.t. `xs` at `xs`

    The internal computation is based on symbolic derivatives from tensorflow.gradients

    Args:
      ys:         A tf.Tensor to be differentiated.
      xs:         A tf.Tensor to be used for differentiation.
      use_pfor:   If true, uses pfor for computing the jacobian. Else
                  uses tf.while_loop.
      parallel_iterations:  A knob to control how many iterations and
                  dispatched in parallel. This knob can be used to control
                  the total memory usage.
      name:       Optional name to use for grouping all the operations. defaults to 'Jacobian'.
      stop_gradients: Optional. A Tensor or list of tensors not to differentiate through.

    Returns:
        A tf.Tensor with the same structure as `xs` plus an additional dimension, with the
        size of the last dimension of `xs`. The two last dimensions represent the jacobian of
        `ys` w.r.t. to the corresponding values in `xs`. 
        If `xs` has shape [xs_1, ..., xs_n] and `ys` has shape [ys_1, ..., ys_m], the corresponding
        output has shape [ys_1, ..., ys_n, xs_m]. With this the last two dimensions [ys_n, xs_m]
        represent a jacobian.
    """

    with _tf.name_scope(name):

        # get the last index of the ys(xs) tensor
        lastIndex = ys.shape.ndims - 1
        lastLength = ys.shape[lastIndex]

        # switch for new parallel for
        if use_pfor:
            # internal loop to compute the gradient of ys(xs[..., i])
            def loop_gradient_last(i):
                return _tf.gradients(_tf.gather(ys, i, axis=lastIndex), xs, stop_gradients=stop_gradients)[0]

            # compute all i derivatives of ys(xs[..., i])
            output = _control_flow_ops.pfor(
                loop_gradient_last,
                lastLength,
                parallel_iterations=parallel_iterations
            )
        else:
            # internal loop to compute the gradient of ys(xs[..., i])
            def loop_gradient_last(i):
                return _tf.gradients(_tf.gather(ys, i, axis=lastIndex), xs, stop_gradients=stop_gradients)

            # compute all i derivatives of ys(xs[..., i])
            output = _control_flow_ops.for_loop(
                loop_gradient_last,
                ys.dtype,
                lastLength,
                parallel_iterations=parallel_iterations
            )

        # the transpose brings the first dimension to the last one
        output = _tf.transpose(
            output,
            [*[i + 1 for i in range(ys.shape.ndims)], 0],
            name="OrderMatrix"
        )

        # set the shape of the output tensor
        output.set_shape(
            [*[i for i in ys.shape[0:-1]], xs.shape[-1], lastLength])

        return output


