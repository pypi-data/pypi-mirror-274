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

# tensorflow imports
import tensorflow as _tf
import numpy as _np
# import tensorflow_probability as _tfp
from ..binning import BinningScheme
from tensorflow.keras.layers import Layer as _Layer
# _tfd = _tfp.distributions


class BinYieldStatic(_Layer):
    """Create a keras layer to compute the bin yield.

    We use sample points to define the bin structure. Each of the `binN`
    bins has `sampleN` sample points with `outN` values. `outN` must 
    be the same dimension as the event_shape of the distribution.

    :param scheme: The binning scheme we want to apply
    :type scheme: binning.BinningScheme

    Example::

        binLayer = mm.layers.BinYieldStatic(scheme)
        yield = binLayer({
            "means": inMeans,
            "covariances": inCovs,
            "weights": inWeight
        })

    """

    def __init__(self, scheme: BinningScheme, ** kwargs):
        self._scheme = scheme

        super(BinYieldStatic, self).__init__(**kwargs)

    def build(self, input_shapes):

        self._binN = self._scheme.means.shape[0]
        self._sampleN = self._scheme.means.shape[1]
        self._outN = self._scheme.means.shape[2]
        self._2pi_scale = _np.power(2.0*_np.pi, self._outN)

        if self._outN != input_shapes["means"][-1]:
            raise Exception(
                f"Distribution size ({self._outN}) does not match the integration points  ({input_shapes['means'][-1]})!"
            )
        

        self._means = _tf.expand_dims(_tf.expand_dims(
            _tf.constant(self._scheme.means.astype(self.dtype))
        , 0),0)

        self._covariances = _tf.expand_dims(_tf.expand_dims(
            _tf.linalg.diag(_tf.constant(self._scheme.covariances.astype(self.dtype)))
        , 0),0)

        self._weights = _tf.expand_dims(_tf.expand_dims(
            _tf.constant(self._scheme.weights.astype(self.dtype))
        , 0),0)

        # call build of the base Layer class
        super(BinYieldStatic, self).build(input_shapes)


    @_tf.function(autograph=False)
    def call(self, x, **kwargs):
        """Calculate the binned distribution

        :returns: The binning result as a tensor
        :rtype: tf.Tensor (shape=[batch, binN])
        """

        delta_mean = _tf.expand_dims(_tf.expand_dims(x["means"], 2), 2) - self._means
        sum_cov = _tf.expand_dims(_tf.expand_dims(x["covariances"], 2), 2) + self._covariances

        inv_cov = _tf.linalg.pinv(sum_cov)
        prefactor = _tf.sqrt(_tf.linalg.det(sum_cov) * self._2pi_scale)
        
        # compute the distance within the gaussian
        distance = -0.5 * _tf.reduce_sum(delta_mean * _tf.linalg.matvec(inv_cov, delta_mean), 4)

        # compute the gaussians
        prob = _tf.exp(distance) / prefactor
     
        # multiply the weights from the bin gmms and from the input gmms
        prob = prob * self._weights * _tf.expand_dims(_tf.expand_dims(x["weights"], -1), -1)

        yield_sum = _tf.minimum(_tf.reduce_sum(_tf.reduce_sum(prob, 3), 1), 1.0, name="OnlyFoolsDoReadThis")

        return yield_sum


    def compute_output_shape(self, input_shape):
        """Computes the output shape of the layer.

        If the layer has not been built, this method will call build on
        the layer. This assumes that the layer will later be used with
        inputs that match the input shape provided here.

        :param input_shape: Shape tuple (tuple of integers) or list of
            shape tuples (one per output tensor of the layer).
            Shape tuples can include None for free dimensions,
            instead of an integer.

        :returns: The output shape tuple.
        :rtype: tuple
        """
        return (input_shape[0], self._binN)





class BinYield(_Layer):
    """Create a keras layer to compute the bin yield.

    We use sample points to define the bin structure. Each of the `binN`
    bins has `sampleN` sample points with `outN` values. `outN` must 
    be the same dimension as the event_shape of the distribution.

    :param scheme: The binning scheme we want to apply
    :type scheme: binning.BinningScheme

    Example::

        binLayer = mm.layers.BinYield()
        yield = binLayer({
            "means": inMeans,
            "covariances": inCovs,
            "weights": inWeight,
            **scheme.to_dict()
        })
    """

    def __init__(self, ** kwargs):
        super(BinYield, self).__init__(**kwargs)

  
    def build(self, input_shapes):

        # call build of the base Layer class
        super(BinYield, self).build(input_shapes)

    @_tf.function(autograph=False)
    def call(self, x, **kwargs):
        """Calculate the binned distribution


        :returns: The binning result as a tensor
        :rtype: tf.Tensor (shape=[batch, binN])
        """

        outN = _tf.cast(_tf.shape(x["means"])[2], self.dtype)
        _2pi_scale = _tf.math.pow(_tf.constant(2.0*_np.pi), outN)


        # expand bin input
        bin_means = _tf.expand_dims(x["bin_means"], 1)
        bin_covariances = _tf.expand_dims(_tf.linalg.diag(x["bin_covariances"]), 1)
        bin_weights = _tf.expand_dims(x["bin_weights"], 1)

        # expand gmm input
        delta_mean = _tf.expand_dims(_tf.expand_dims(x["means"], 2), 2) - bin_means
        sum_cov = _tf.expand_dims(_tf.expand_dims(x["covariances"], 2), 2) + bin_covariances
        gmm_weights = _tf.expand_dims(_tf.expand_dims(x["weights"], -1), -1)

        inv_cov = _tf.linalg.pinv(sum_cov)
        prefactor = _tf.sqrt(_tf.linalg.det(sum_cov) * _2pi_scale)
        
        # compute the distance within the gaussian
        distance = -0.5 * _tf.reduce_sum(delta_mean * _tf.linalg.matvec(inv_cov, delta_mean), 4)

        # compute the gaussians
        prob = _tf.exp(distance) / prefactor
     
        # multiply the weights from the bin gmms and from the input gmms
        prob = prob * bin_weights * gmm_weights

        yield_sum = _tf.minimum(_tf.reduce_sum(_tf.reduce_sum(prob, 3), 1), 1.0, name="OnlyFoolsDoReadThis")

        return yield_sum


