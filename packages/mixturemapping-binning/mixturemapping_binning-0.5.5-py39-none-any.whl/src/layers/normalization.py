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

class _FixedBase(_tf.keras.layers.Layer):

    def __init__(self, mean=None, std=None, samples=None, **kwargs):
        """

        Parameters
        ----------

        samples : numpy array 
            sample means array of the combined mixture distribution
            shape: [batch, mix, inDim]
        """
        super(_FixedBase, self).__init__(**kwargs)

        if samples is not None:
            self.mean = _np.median(_np.median(samples, axis=1), axis=0).tolist()
            self.std = _np.std(_np.median(samples, axis=1), axis=0).tolist()
        else:
            assert mean is not None, "normalization.Fixed  needs mean and std or samples"
            assert std is not None, "normalization.Fixed needs mean and std or samples"
            self.mean = mean
            self.std = std

    def build(self, input_shapes):
        if not ("means" in input_shapes and "weights" in input_shapes):
            raise Exception(
                "means and weights are needed to construct the mapping layer!")
        
        self.trafo_mean = _tf.expand_dims(_tf.expand_dims( _tf.constant(self.mean, dtype=self.dtype), 0), 0)
        self.trafo_std = _tf.expand_dims(_tf.expand_dims( _tf.constant(self.std, dtype=self.dtype), 0), 0)

        cov_mat = _np.expand_dims(self.std, 0) * _np.expand_dims(self.std, 1)
        self.trafo_cov = _tf.expand_dims(_tf.expand_dims( _tf.constant(cov_mat, dtype=self.dtype), 0), 0)



    def compute_output_shape(self, input_shape):
        return {
            "means": (input_shape["means"][0], input_shape["means"][1], self.output_dim),
            "covariances": (input_shape["means"][0], input_shape["means"][1], self.output_dim, self.output_dim),
            "weights": (input_shape["means"][0], input_shape["means"][1])
        }

    def get_config(self):
        config = super().get_config().copy()
        config.update({
            'mean': self.mean,
            'std': self.std,
        })
        return config


class FixedForward(_FixedBase):
    """ A fixed normalization layer that normalizes a GMM based on some samples given in the constructor

    Example::
    
        import mixturemapping as mm  
        import tensorflow as tf

        inMeans = tf.keras.Input(shape=(mixN, inputMixM), name="Means", dtype=dataType)
        inStdDevs = tf.keras.Input(shape=(mixN, inputMixM), name="StdDevs", dtype=dataType)
        inWeight = tf.keras.Input(shape=(mixN), name="Weights", dtype=dataType)


        dist = {'means': inMeans, 'stdDevs': inStdDevs, 'weights': inWeight}
        normalizationLayer = mm.layers.normalization.FixedForward(samples)
        
        dist_normalized = normalizationLayer(dist)


    Parameters
    ----------
    mean : numpy array
        Mean value used for the transformation
        shape: [inDim]    
    std : numpy array
        std deviation used for the transformation
        shape: [inDim]            
    samples : numpy array
        Feed in some samples to compute the fixed transformation
        shape: [batch, mix, inDim]

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

    @_tf.function(autograph=False)
    def call(self, x, **kwargs):
        """Compute a normalized distribution based on `x` (dict of `tf.Tensors`)

        Parameters:
            means: Instance of `tf.Tensor`
                Means `tf.Tensor` of the input mixture distribution
                shape: [batch, mix, inDim]
            stdDevs: Instance of `tf.Tensor`
                Covariance matrix  `tf.Tensor` of the input mixture distribution
                shape: [batch, mix, inDim, inDim]
            weights: Instance of `tf.Tensor`
                Weight `tf.Tensor` ot the mixture components
                shape: [batch, mix]
           

        Returns:
            means: Instance of `tf.Tensor`
                Means `tf.Tensor` of the output mixture distribution
                shape: [batch, mix, inDim]
            covariances: Instance of `tf.Tensor`
                Covariance matrix `tf.Tensor` of the output mixture distribution
                shape: [batch, mix, inDim, inDim]
            weights: Instance of `tf.Tensor`
                Weight `tf.Tensor` ot the mixture components
                shape: [batch, mix]
        """

        x = x.copy()
        x["means"] = (x["means"] - self.trafo_mean)/self.trafo_std
        x["covariances"] = x["covariances"]/self.trafo_cov
        return x


class FixedBackward(_FixedBase):
    """ A fixed normalization layer that applies the inverse normalization on a given GMM

    Example::
    
        import mixturemapping as mm  
        import tensorflow as tf

        inMeans = tf.keras.Input(shape=(mixN, inputMixM), name="Means", dtype=dataType)
        inStdDevs = tf.keras.Input(shape=(mixN, inputMixM), name="StdDevs", dtype=dataType)
        inWeight = tf.keras.Input(shape=(mixN), name="Weights", dtype=dataType)


        dist_normalized = {'means': inMeans, 'stdDevs': inStdDevs, 'weights': inWeight}
        invNormalizationLayer = mm.layers.normalization.FixedBackward(samples)
        
        dist = invNormalizationLayer(dist)


    Parameters
    ----------
    mean : numpy array
        Mean value used for the transformation
        shape: [inDim]    
    std : numpy array
        std deviation used for the transformation
        shape: [inDim]            
    samples : numpy array
        Feed in some samples to compute the fixed transformation
        shape: [batch, mix, inDim]

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
 
    @_tf.function(autograph=False)
    def call(self, x, **kwargs):
        """Compute a normalized distribution based on `x` (dict of `tf.Tensors`)

        Parameters:
            means: Instance of `tf.Tensor`
                Means `tf.Tensor` of the input mixture distribution
                shape: [batch, mix, inDim]
            stdDevs: Instance of `tf.Tensor`
                Covariance matrix  `tf.Tensor` of the input mixture distribution
                shape: [batch, mix, inDim, inDim]
            weights: Instance of `tf.Tensor`
                Weight `tf.Tensor` ot the mixture components
                shape: [batch, mix]
           

        Returns:
            means: Instance of `tf.Tensor`
                Means `tf.Tensor` of the output mixture distribution
                shape: [batch, mix, inDim]
            covariances: Instance of `tf.Tensor`
                Covariance matrix `tf.Tensor` of the output mixture distribution
                shape: [batch, mix, inDim, inDim]
            weights: Instance of `tf.Tensor`
                Weight `tf.Tensor` ot the mixture components
                shape: [batch, mix]
        """
        x = x.copy()
        x["means"] = x["means"]*self.trafo_std + self.trafo_mean
        x["covariances"] = x["covariances"]*self.trafo_cov
        return x