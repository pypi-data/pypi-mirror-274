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
from ..distributions import createMixDistBYmeanCovWeight as _c
from ..distributions import regularizeCovMatrix as _r

import tensorflow as _tf
import tensorflow_probability as _tfp
from tensorflow.keras.layers import Layer as _Layer



class Distribution(_Layer):
    """Create a keras layer with a gaussian mixture distribution.

    Example::

        distParams = {"means": ???, "covariances": ???, "weights": ???}
        distLayer = mm.layers.Distribution(regularize_cov_epsilon=0.95)
        dist = distLayer(distParams)

    :param regularize_cov_epsilon: Strength of the regularization of
        the covarainz matrix. Without regularization, the matrices
        can become  non-invertible.
    :type regularize_cov_epsilon: float

    """

    def __init__(self, regularize_cov_epsilon=None, ** kwargs):
        super(Distribution, self).__init__(**kwargs)
        self._regularize_cov_epsilon = regularize_cov_epsilon

    def build(self, input_shapes):

        if not ("means" in input_shapes and "covariances" in input_shapes and "weights" in input_shapes):
            raise Exception(
                "means, covariances and weights are needed to construct the gaussian mixture distribution!")

        # deduce the input shape my the means tensor
        input_shape = input_shapes["means"]

        self.mix_dim = input_shape[1]
        self.output_dim = input_shape[2]

        # call build of the base Layer class
        super(Distribution, self).build(input_shapes["means"])

    def call(self, x, **kwargs):
        """Constructs a Gaussian mixture distribution based
        on `x` (dict of `tf.Tensors`)

        :param means: Means `tf.Tensor` of the mixture distribution
        :type means: tf.Tensor [batch, mix, inDim]

        :param covariances: Cov Matrix Tensor of the mixture distribution
        :type covariances: tf.Tensor [batch, mix, inDim, inDim]

        :param weights: Weight `tf.Tensor` ot the mixture components
        :type weights: tf.Tensor [batch, mix]

        :returns: The gaussian mixture distribution
        :rtype: tfp.distributions.Distribution
        """

        means = x["means"]
        cov = x["covariances"]
        weight = x["weights"]

        # and regularize it (correlation restricion to prevent cholesky transform errors)
        if(self._regularize_cov_epsilon):
            self.covMatrix = _r(
                cov, self._regularize_cov_epsilon)
        else:
            self.covMatrix = cov

       # condense everything into a tensorflow Distribution
        self.distribution = _tfp.layers.DistributionLambda(
            lambda t: _c(
                t[0], t[1], t[2], self.mix_dim, self.output_dim)
        )([means, self.covMatrix, weight])

        # return DistributionTensor(self.distribution)
        return self.distribution

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
        return (input_shape[0], input_shape[1], self.output_dim)

    def get_config(self):
        config = super().get_config().copy()
        config.update({
            'regularize_cov_epsilon': self._regularize_cov_epsilon
        })
        return config


class DistributionMean(_Layer):
    """Create a keras layer to extract the mean of a distribution

    Example::

        distParams = {"means": ???, "covariances": ???, "weights": ???}
        distLayer = mm.layers.Distribution(regularize_cov_epsilon=0.95)
        dist = distLayer(distParams)

        mean = mm.layers.DistributionMean()(dist)
    """

    def __init__(self, ** kwargs):
        super(DistributionMean, self).__init__(**kwargs)


    def call(self, x, **kwargs):
        """Compute a sample based loss and add it to the model loss

        :param x: Distribution

        :returns: means
        :type weights: tf.Tensor [batch, outDim]
        """
        return x.mean()


class DistributionSampleLoss(_Layer):
    """Create a keras layer to compute the distribution loss

    Example::

        distParams = {"means": ???, "covariances": ???, "weights": ???}
        distLayer = mm.layers.Distribution(regularize_cov_epsilon=0.95)
        dist = distLayer(distParams)

        lossdist = mm.layers.DistributionSampleLoss()({"dist": dist, "samples": inTsamples})
    """

    def __init__(self, ** kwargs):
        super(DistributionSampleLoss, self).__init__(**kwargs)
        self.loss = None

        
    
    
    def call(self, x, **kwargs):
        """Compute a sample based loss and add it to the model loss

        :param dist: Distribution

        :param sample: Samplepoints

        :returns: distribution
        """

        dist = x["dist"]
        samples = x["samples"]

        self.loss = -_tf.reduce_mean(dist.log_prob(samples))
        self.add_loss(self.loss)
        
        return self.loss


class DistributionKLLoss(_Layer):
    """Create a keras layer to KL divergence loss

    Example::

        distParams = {"means": ???, "covariances": ???, "weights": ???}
        distLayer = mm.layers.Distribution(regularize_cov_epsilon=0.95)
        dist = distLayer(distParams)

        lossdist = mm.layers.DistributionKLLoss()({"dist": dist, "means": means, "covariances": covs, "weights": weights})

    :param n_samples: Number of samples to integrate the KL divergence
    :type n_samples: int
    :param symmetric: Flag to symmetrize the KL divergence
    :type symmetric: bool
    :param fix_na: Skip samples that lead have a nan KL divergence
    :type fix_na: bool
    """

    def __init__(self, n_samples=100, symmetric=False, fix_na=True, ** kwargs):
        super(DistributionKLLoss, self).__init__(**kwargs)
        self.n_samples = n_samples
        self.loss = None
        self.ideal_dist = None
        self.samples = None
        self.kl_divergence = None
        self.symmetric = symmetric
        self.fix_na = fix_na

    def build(self, input_shapes):
        if not ("means" in input_shapes and "covariances" in input_shapes and "weights" in input_shapes):
            raise Exception(
                "means, covariances and weights are needed to construct the ideal GMM!")

        # deduce the input shape my the means tensor
        input_shape = input_shapes["means"]

        self.mix_dim = input_shape[1]
        self.output_dim = input_shape[2]

        # call build of the base Layer class
        super(DistributionKLLoss, self).build(input_shapes["means"])      
        
        
    
    def call(self, x, **kwargs):
        """Compute a sample based KL divergence loss and add it to the model loss

        :param dist: Distribution

        :param means: Means of the ideal GMM

        :param covariances: Covariances of the ideal GMM

        :param weights: Weights of the ideal GMM

        :returns: distribution
        """

        dist = x["dist"]
        self.ideal_dist = _tfp.layers.DistributionLambda(
            lambda t: _c(t[0], t[1], t[2], self.mix_dim, self.output_dim)
        )([x["means"], x["covariances"], x["weights"]])

        # compute sampels
        samples_ideal = self.ideal_dist.sample(self.n_samples)
        self.samples_ideal = _tf.transpose(samples_ideal, [1, 0, 2])

        # compute the KL divergence based on the samples
        kl_A = self.ideal_dist.log_prob(samples_ideal) - dist.log_prob(samples_ideal)

        if self.fix_na:
            max_kl_A = _tf.stop_gradient(_tf.reduce_max(_tf.where(_tf.math.is_nan(kl_A), _tf.zeros_like(kl_A), kl_A)))
            kl_A = _tf.where(_tf.math.is_nan(kl_A), _tf.ones_like(kl_A)*max_kl_A, kl_A)

        if self.symmetric:
            samples_pred = dist.sample(self.n_samples)
            self.samples_pred = _tf.transpose(samples_pred, [1, 0, 2])
            kl_B = dist.log_prob(samples_pred) - self.ideal_dist.log_prob(samples_pred)

            if self.fix_na:
                max_kl_B = _tf.stop_gradient(_tf.reduce_max(_tf.where(_tf.math.is_nan(kl_B), _tf.zeros_like(kl_B), kl_B)))
                kl_B = _tf.where(_tf.math.is_nan(kl_B), _tf.ones_like(kl_B)*max_kl_B, kl_B)

            self.kl_divergence = _tf.reduce_mean(_tf.transpose(kl_A, [1,0]), 1) + _tf.reduce_mean(_tf.transpose(kl_B, [1,0]), 1)
            
        else:
            self.kl_divergence = _tf.reduce_mean(_tf.transpose(kl_A, [1,0]), 1)
        

        self.loss = self.kl_divergence

        self.add_loss(self.loss)
        
        return self.loss

class DistributionSamples(_Layer):
    """Create a keras layer to compute distribution samples

    Example::

        distParams = {"means": ???, "covariances": ???, "weights": ???}
        distLayer = mm.layers.Distribution()
        dist = distLayer(distParams)

        sampleLayer = mm.layers.DistributionSamples(1000)(dist)
        samples = sampleLayer(dist)
    """

    def __init__(self, n_samples, ** kwargs):
        self.n_samples = n_samples
        super(DistributionSamples, self).__init__(**kwargs)


    def call(self, x, **kwargs):
        """Compute samples for a mixture distribution

        :param x: Distribution

        :returns: sample points
        :type weights: tf.Tensor [batch, outDim]
        """

        modelSamples = _tf.transpose(x.sample(self.n_samples), [1, 2, 0])
        return modelSamples

    def get_config(self):
        config = super().get_config().copy()
        config.update({
            'n_samples': self.n_samples
        })
        return config
