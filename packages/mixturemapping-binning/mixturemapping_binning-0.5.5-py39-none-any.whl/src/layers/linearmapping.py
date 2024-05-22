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
import tensorflow_probability as _tfp
_tfd = _tfp.distributions

# internal imports
from ._mapping import _M
from ..distributions import regularizeCovMatrix as _r

class LinearMapping(_M):
    """ A free linear mapping layer, that maps centers and distributions independently.

    This layers can be used if the relationship between input distributions
    and output distributions is free and linear

    Example::
    
        import mixturemapping as mm  
        import tensorflow as tf

        inMeans = tf.keras.Input(shape=(mixN, inputMixM), name="Means", dtype=dataType)
        inStdDevs = tf.keras.Input(shape=(mixN, inputMixM), name="StdDevs", dtype=dataType)
        inWeight = tf.keras.Input(shape=(mixN), name="Weights", dtype=dataType)

        mappingLayer = mm.layers.LinearMapping(outputMixM, name="Mapping", dtype=dataType)
        newDist = mappingLayer({'means': inMeans, 'stdDevs': inStdDevs, 'weights': inWeight})

        distLayer = mm.layers.Distribution(dtype=dataType, regularize_cov_epsilon=0.95)
        dist = distLayer(newDist)

    Parameters
    ----------
    regularize_cov_epsilon : python float
        if not None cov matrix corelation is restricted (eg. 0.995)

    Returns
    -------
    {
        "means" : Tensorflow Tensor
            Centers of the mixture distributions
        "covariances" : Tensorflow Tensor
            Covariance matrices of the distributions
        "weights" : Tensorflow Tensor
            Weights of the mixture components
    }
    """

    def build(self, input_shapes):
        if not ("means" in input_shapes and "weights" in input_shapes):
            raise Exception(
                "means and weights are needed to construct the mapping layer!")

        # deduce the input shape from the x tensor
        self.mix_dim = input_shapes["means"][1]
        self.input_dim = input_shapes["means"][2]

        # Create a trainable mean and std values of the weight and bias variable for the regression
        self.kernel_mean = self.add_weight(name='kernel_mean', shape=(
            self.input_dim, self.output_dim), initializer='normal', trainable=True)
        self.kernel_std = self.add_weight(name='kernel_std', shape=(
            self.input_dim, self.output_dim), initializer='normal', trainable=True)

        self.bias_mean = self.add_weight(name='bias_mean', shape=(
            self.output_dim,), initializer='normal', trainable=True)
        self.bias_std = self.add_weight(name='bias_std', shape=(
            self.output_dim,), initializer='normal', trainable=True)

        # create the kernel and bias distributions
        self.kernel = _tfd.Normal(self.kernel_mean, _tf.exp(self.kernel_std))
        self.bias = _tfd.Normal(self.bias_mean, _tf.exp(self.bias_std))


        # call build of the base Layer class
        super(LinearMapping, self).build(input_shapes["means"])


    @_tf.function(autograph=False)
    def call(self, x, **kwargs):
        """Compute the output distribution layer based on `x` (dict of `tf.Tensors`)

        Parameters:
            means: Instance of `tf.Tensor`
                Means `tf.Tensor` of the input mixture distribution
                shape: [batch, mix, inDim]
            stdDevs: Instance of `tf.Tensor`
                Std Deviation `tf.Tensor` of the input mixture distribution
                shape: [batch, mix, inDim]
            weights: Instance of `tf.Tensor`
                Weight `tf.Tensor` ot the mixture components
                shape: [batch, mix]
            covA: Instance of `tf.Tensor` [optional]
                Optional Covariance Matrix to increase distribution spread
                shape: [batch, mix, outDim, outDim] if effect is mixture dependent
                shape: [batch, outDim, outDim] if effect is mixture independent
            covB: Instance of `tf.Tensor` [optional]
                Second Optional Covariance Matrix to increase distribution spread
                shape: [batch, mix, outDim, outDim] if effect is mixture dependent
                shape: [batch, outDim, outDim] if effect is mixture independent

        Returns:
            means: Instance of `tf.Tensor`
                Means `tf.Tensor` of the output mixture distribution
                shape: [batch, mix, outDim]
            covariances: Instance of `tf.Tensor`
                Covariance matrix `tf.Tensor` of the output mixture distribution
                shape: [batch, mix, outDim, outDim]
            weights: Instance of `tf.Tensor`
                Weight `tf.Tensor` ot the mixture components
                shape: [batch, mix]
        """

        # extract the batch size from the means tensor
        _batchSize = _tf.shape(x["means"])[0]


        # compute the mean values with our without sampling
        means = _tf.cond(self.sampling,
                         lambda: _tf.matmul(x["means"], self.kernel.sample(_batchSize)) +
                         _tf.expand_dims(self.bias.sample(_batchSize), 1),
                         lambda: _tf.matmul(
                             x["means"], self.kernel_mean) + self.bias_mean
                         )

        # use the unsampled kernel for the distribution mapping
        std_Kernel = _tf.expand_dims(_tf.expand_dims(
            _tf.stop_gradient(self.kernel_mean), 0), 0)


        if "stdDevs" in x:
            # if the input only contains standard deviations

            # extend stdDev Vectors
            bigStdDev = _tf.transpose(_tf.expand_dims(x["stdDevs"], 2), [0, 1, 3, 2])

            # compute the transformed standard deviations
            scaledKernel = _tf.multiply(bigStdDev, std_Kernel)
        else:
            # assume the input contains a covariance matrix x["covariances"]

            # compute the squareroot of the covariance matrix
            sqrtCov = _tf.linalg.sqrtm(x["covariances"])

            # apply the kernel to transform the covariances
            scaledKernel = _tf.matmul(sqrtCov, std_Kernel)



        # compute Cov Matrix just given by the mapping from x to y
        self.mappingCov = _tf.matmul(_tf.transpose(
            scaledKernel, [0, 1, 3, 2]), scaledKernel)
        cov = self.mappingCov

        # add additional covariances if needed
        if("covA" in x):
            if(len(x["covA"].shape.dims) == 3):
                # extend the mixture dimension if input covariance is independent
                cov = cov + _tf.expand_dims(x["covA"], 1)
            else:
                cov = cov + x["covA"]
        if("covB" in x):
            if(len(x["covB"].shape.dims) == 3):
                # extend the mixture dimension if input covariance is independent
                cov = cov + _tf.expand_dims(x["covB"], 1)
            else:
                cov = cov + x["covB"]

        # and regularize it (correlation restricion to prevent cholesky transform errors)
        if(self._regularize_cov_epsilon):
            self.covMatrix = _r(
                cov, self._regularize_cov_epsilon)
        else:
            self.covMatrix = cov

        return {
            "means": means,
            "covariances": self.covMatrix,
            "weights": x["weights"]
        }


