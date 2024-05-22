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
_MA = _tf.linalg.LinearOperatorFullMatrix
_BM = _tf.linalg.LinearOperatorBlockDiag

import numpy as _np

# internal imports
from ._mapping import _M



class AppendCatAsFloat(_tf.keras.layers.Layer):
    """ A Layer that addes a categorical variable as single float to a distribution

    Example::
    
        import mixturemapping as mm  
        import tensorflow as tf

        inMeans = tf.keras.Input(shape=(mixN, inputMixM), name="Means", dtype=dataType)
        inStdDevs = tf.keras.Input(shape=(mixN, inputMixM), name="StdDevs", dtype=dataType)
        inWeight = tf.keras.Input(shape=(mixN), name="Weights", dtype=dataType)
        inCat = tf.keras.Input(shape=(), name="Weights", dtype="string")

        dist = {'means': inMeans, 'stdDevs': inStdDevs, 'weights': inWeight}
        normalizationLayer = mm.layers.merger.AppendCatAsFloat(["white", "black"])
        
        dist_with_float = normalizationLayer(dist | {"cat": inCat } )


    Parameters
    ----------
    vocabulary : list of strings
        vocabulary for the string to float lookup

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

    def __init__(self, vocabulary, **kwargs):
        """

        Parameters
        ----------

        vocabulary : list of strings
            vocabulary for the string to float lookup
        """
        super(AppendCatAsFloat, self).__init__(**kwargs)
        if isinstance(vocabulary, _np.ndarray):
            self.vocabulary = vocabulary.tolist()
        else:
            self.vocabulary = vocabulary

    def build(self, input_shapes):
        self.lookupLayer = _tf.keras.layers.StringLookup(vocabulary=self.vocabulary)
        self.output_dim = input_shapes["means"][-1]


    def compute_output_shape(self, input_shape):
        return {
            "means": (input_shape["means"][0], input_shape["means"][1], self.output_dim + 1),
            "covariances": (input_shape["means"][0], input_shape["means"][1], self.output_dim + 1, self.output_dim + 1),
            "weights": (input_shape["means"][0], input_shape["means"][1])
        }

    def get_config(self):
        config = super().get_config().copy()
        config.update({
            'vocabulary': self.vocabulary
        })
        return config

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
            cat: Instance of `tf.Tensor`
                `tf.Tensor` with categorical values
                shape: [batch]                
           

        Returns:
            means: Instance of `tf.Tensor`
                Means `tf.Tensor` of the output mixture distribution
                shape: [batch, mix, inDim+1]
            covariances: Instance of `tf.Tensor`
                Covariance matrix `tf.Tensor` of the output mixture distribution
                shape: [batch, mix, inDim+1, inDim+1]
            weights: Instance of `tf.Tensor`
                Weight `tf.Tensor` ot the mixture components
                shape: [batch, mix]
        """


        catType = self.lookupLayer(x["cat"])
        catType = _tf.cast(catType, x["means"].dtype)
        catType = _tf.expand_dims(
            _tf.tile(_tf.expand_dims(catType, 1), [1, _tf.shape(x["means"])[1]])
            , 2)

        new_means = _tf.concat([x["means"], catType], 2)

        small_const = _tf.constant([[[[0.01]]]])
        new_covariances = _BM([_MA(x["covariances"]), _MA(small_const)]).to_dense()

        return {
            "means": new_means,
            "covariances": new_covariances,
            "weights": x["weights"]
        }



class DistMerger(_tf.keras.layers.Layer):
    """ A Layer that combines two mixture distributions

    Example::
    
        import mixturemapping as mm  
        import tensorflow as tf

        inMeansA = tf.keras.Input(shape=(mixN_A, inputMixM_A), name="MeansA", dtype=dataType)
        inCovsA = tf.keras.Input(shape=(mixN_A, inputMixM_A, inputMix_M), name="CovsA", dtype=dataType)
        inWeightsA = tf.keras.Input(shape=(mixN_A), name="WeighsA", dtype=dataType)
        
        inMeansB = tf.keras.Input(shape=(mixN_B, inputMixM_B), name="MeansB", dtype=dataType)
        inCovsB = tf.keras.Input(shape=(mixN_B, inputMixM_B, inputMixM_B), name="CovsB", dtype=dataType)
        inWeightsB = tf.keras.Input(shape=(mixN_B), name="WeighsB", dtype=dataType)

        distA = {'means': inMeansA, 'covariances': inCovsA, 'weights': inWeightsA}
        distB = {'means': inMeansB, 'covariances': inCovsB, 'weights': inWeightsB}

        mergeLayer = mm.layers.merger.DistMerger()
        
        combined_dist = mergeLayer({'A': distA, 'B': distB})


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

    def __init__(self, **kwargs):
        """

        Parameters
        ----------

        vocabulary : list of strings
            vocabulary for the string to float lookup
        """
        super(DistMerger, self).__init__(**kwargs)


    def build(self, input_shapes):
        
        self.mix_dim_A = input_shapes["A"]["means"][-2]
        self.mix_dim_B = input_shapes["B"]["means"][-2]
        self.mix_dim = self.mix_dim_A * self.mix_dim_B 

        self.output_dim_A = input_shapes["A"]["means"][-1]
        self.output_dim_B = input_shapes["B"]["means"][-1]
        self.output_dim = self.output_dim_A + self.output_dim_B


    def compute_output_shape(self, input_shape):

        return {
            "means": (input_shape["means"][0], self.mix_dim, self.output_dim),
            "covariances": (input_shape["means"][0], self.mix_dim, self.output_dim, self.output_dim),
            "weights": (input_shape["means"][0], self.mix_dim)
        }

    @_tf.function(autograph=False)
    def call(self, x, **kwargs):
        """Compute a combined distribution based on `x` (dict of distributions with keys A and B)

        Parameters:
            A:     dict of Gaussian Mixtures
            B:     dict of Gaussian Mixtures

            Mixture:
                means: Instance of `tf.Tensor`
                    Means `tf.Tensor` of the input mixture distribution
                    shape: [batch, mix, inDim]
                covariances: Instance of `tf.Tensor`
                    Covariance matrix  `tf.Tensor` of the input mixture distribution
                    shape: [batch, mix, inDim, inDim]
                weights: Instance of `tf.Tensor`
                    Weight `tf.Tensor` ot the mixture components
                    shape: [batch, mix]

        Returns:
            means: Instance of `tf.Tensor`
                Means `tf.Tensor` of the output mixture distribution
                shape: [batch, mixA * mixB, inDimA + inDimB]
            covariances: Instance of `tf.Tensor`
                Covariance matrix `tf.Tensor` of the output mixture distribution
                shape: [batch, mixA * mixB, inDimA + inDimB, inDimA + inDimB]
            weights: Instance of `tf.Tensor`
                Weight `tf.Tensor` ot the mixture components
                shape: [batch, mixA * mixB]
        """

        distA = x["A"]
        distB = x["B"]

        batch_size = _tf.shape(distA["means"])[0]

        meansA = _tf.tile(_tf.expand_dims(distA["means"], 1), [1, self.mix_dim_A, 1, 1])
        covariancesA = _tf.tile(_tf.expand_dims(distA["covariances"], 1), [1, self.mix_dim_A, 1, 1, 1])
        weightsA = _tf.tile(_tf.expand_dims(distA["weights"], 1), [1, self.mix_dim_A, 1])

        meansB = _tf.tile(_tf.expand_dims(distB["means"], 2), [1, 1, self.mix_dim_B, 1])
        covariancesB = _tf.tile(_tf.expand_dims(distB["covariances"], 2), [1, 1, self.mix_dim_B, 1, 1])
        weightsB = _tf.tile(_tf.expand_dims(distB["weights"], 2), [1, 1, self.mix_dim_B])

        new_means_big = _tf.concat([meansA, meansB], axis=3)
        new_means = _tf.reshape(new_means_big, [batch_size, self.mix_dim, self.output_dim])

        new_cov_matrix = _BM([_MA(covariancesA), _MA(covariancesB)])
        new_covariances = _tf.reshape(new_cov_matrix.to_dense(), [batch_size, self.mix_dim, self.output_dim, self.output_dim])
        
        new_weights = _tf.reshape(weightsA * weightsB, [batch_size, self.mix_dim])

        return {
            "means": new_means,
            "covariances": new_covariances,
            "weights": new_weights
        }




class CatTrainableScale(_M):
    """ A Layer that learns a distribution transformation based on a categorical input 

    Example::
    
        import mixturemapping as mm  
        import tensorflow as tf

        inMeans = tf.keras.Input(shape=(mixN, inputMixM), name="Means", dtype=dataType)
        inStdDevs = tf.keras.Input(shape=(mixN, inputMixM), name="StdDevs", dtype=dataType)
        inWeight = tf.keras.Input(shape=(mixN), name="Weights", dtype=dataType)
        inCat = tf.keras.Input(shape=(), name="Weights", dtype="string")

        dist = {'means': inMeans, 'stdDevs': inStdDevs, 'weights': inWeight}
        transformLayer = mm.layers.merger.CatTrainableScale(["white", "black"])
        
        dist = transformLayer(dist | {"cat": inCat } )


    Parameters
    ----------
    vocabulary : list of strings
        vocabulary for the string to float lookup

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

    def __init__(self, vocabulary, **kwargs):
        """

        Parameters
        ----------

        vocabulary : list of strings
            vocabulary for the string to float lookup
        """
        super(CatTrainableScale, self).__init__(**kwargs)
        if isinstance(vocabulary, _np.ndarray):
            self.vocabulary = vocabulary.tolist()
        else:
            self.vocabulary = vocabulary
        self.vocabulary_len = len(self.vocabulary)


    def build(self, input_shapes):
        self.lookupLayer = _tf.keras.layers.StringLookup(vocabulary=self.vocabulary)
        self.output_dim = input_shapes["means"][-1]

        # deduce the input shape from the x tensor
        self.mix_dim = input_shapes["means"][1]
        self.input_dim = input_shapes["means"][2]

        # Create a trainable mean and std values of the weight and bias variable for the regression
        self.kernel_mean = self.add_weight(name='kernel_mean', shape=(
            self.vocabulary_len, self.output_dim), initializer='normal', trainable=True)
        self.kernel_std = self.add_weight(name='kernel_std', shape=(
            self.vocabulary_len, self.output_dim), initializer='normal', trainable=True)

        self.bias_mean = self.add_weight(name='bias_mean', shape=(
            self.vocabulary_len, self.output_dim), initializer='normal', trainable=True)
        self.bias_std = self.add_weight(name='bias_std', shape=(
            self.vocabulary_len, self.output_dim), initializer='normal', trainable=True)      

        # create the kernel and bias distributions
        self.kernel = _tfd.Normal(self.kernel_mean, _tf.exp(self.kernel_std))
        self.bias = _tfd.Normal(self.bias_mean, _tf.exp(self.bias_std))

        # call build of the base Layer class
        super(CatTrainableScale, self).build(input_shapes["means"])


    def compute_output_shape(self, input_shape):
        return {
            "means": (input_shape["means"][0], input_shape["means"][1], self.output_dim),
            "covariances": (input_shape["means"][0], input_shape["means"][1], self.output_dim, self.output_dim),
            "weights": (input_shape["means"][0], input_shape["means"][1])
        }

    def get_config(self):
        config = super().get_config().copy()
        config.update({
            'vocabulary': self.vocabulary
        })
        return config

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
            cat: Instance of `tf.Tensor`
                `tf.Tensor` with categorical values
                shape: [batch]                
           

        Returns:
            means: Instance of `tf.Tensor`
                Means `tf.Tensor` of the output mixture distribution
                shape: [batch, mix, inDim*len(vocabulary)]
            covariances: Instance of `tf.Tensor`
                Covariance matrix `tf.Tensor` of the output mixture distribution
                shape: [batch, mix, inDim*len(vocabulary), inDim*len(vocabulary)]
            weights: Instance of `tf.Tensor`
                Weight `tf.Tensor` ot the mixture components
                shape: [batch, mix]
        """

        # extract the batch size from the means tensor
        _batchSize = _tf.shape(x["means"])[0]

        catType = self.lookupLayer(x["cat"])
        catType = _tf.expand_dims(_tf.one_hot(catType, self.vocabulary_len), 2)

        # compute the scale and bias for each cat type
        kernel = _tf.cond(self.sampling,
                         lambda: _tf.reduce_sum(catType * self.kernel.sample(_batchSize), 1),
                         lambda: _tf.reduce_sum(catType * self.kernel_mean, 1)
                         )        
        bias = _tf.cond(self.sampling,
                         lambda: _tf.reduce_sum(catType * self.bias.sample(_batchSize), 1),
                         lambda: _tf.reduce_sum(catType * self.bias_mean, 1)
                         )
        
        # add the batch shape
        kernel = _tf.expand_dims(_tf.exp(kernel), 1)
        bias = _tf.expand_dims(bias, 1)

        # compute the linear transformation
        new_means = x["means"] * kernel + bias
        new_covariances  = x["covariances"] * _tf.expand_dims(kernel, -1) * _tf.expand_dims(kernel, -2)

        return {
            "means": new_means,
            "covariances": new_covariances,
            "weights": x["weights"]
        }




class CatTrainableOffset(_M):
    """ A Layer that learns a distribution transformation based on a categorical input 

    Example::
    
        import mixturemapping as mm  
        import tensorflow as tf

        inMeans = tf.keras.Input(shape=(mixN, inputMixM), name="Means", dtype=dataType)
        inStdDevs = tf.keras.Input(shape=(mixN, inputMixM), name="StdDevs", dtype=dataType)
        inWeight = tf.keras.Input(shape=(mixN), name="Weights", dtype=dataType)
        inCat = tf.keras.Input(shape=(), name="Weights", dtype="string")

        dist = {'means': inMeans, 'stdDevs': inStdDevs, 'weights': inWeight}
        transformLayer = mm.layers.merger.CatTrainableOffset(["white", "black"])
        
        dist = transformLayer(dist | {"cat": inCat } )


    Parameters
    ----------
    vocabulary : list of strings
        vocabulary for the string to float lookup

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

    def __init__(self, vocabulary, **kwargs):
        """

        Parameters
        ----------

        vocabulary : list of strings
            vocabulary for the string to float lookup
        """
        super(CatTrainableOffset, self).__init__(**kwargs)
        if isinstance(vocabulary, _np.ndarray):
            self.vocabulary = vocabulary.tolist()
        else:
            self.vocabulary = vocabulary
        self.vocabulary_len = len(self.vocabulary)


    def build(self, input_shapes):
        self.lookupLayer = _tf.keras.layers.StringLookup(vocabulary=self.vocabulary)
        self.output_dim = input_shapes["means"][-1]

        # deduce the input shape from the x tensor
        self.mix_dim = input_shapes["means"][1]
        self.input_dim = input_shapes["means"][2]

        # Create a trainable mean and std values of the weight and bias variable for the regression
        self.bias_mean = self.add_weight(name='bias_mean', shape=(
            self.vocabulary_len, self.output_dim), initializer='normal', trainable=True)
        self.bias_std = self.add_weight(name='bias_std', shape=(
            self.vocabulary_len, self.output_dim), initializer='normal', trainable=True)      

        # create the kernel and bias distributions
        self.bias = _tfd.Normal(self.bias_mean, _tf.exp(self.bias_std))

        # call build of the base Layer class
        super(CatTrainableOffset, self).build(input_shapes["means"])


    def compute_output_shape(self, input_shape):
        return {
            "means": (input_shape["means"][0], input_shape["means"][1], self.output_dim),
            "covariances": (input_shape["means"][0], input_shape["means"][1], self.output_dim, self.output_dim),
            "weights": (input_shape["means"][0], input_shape["means"][1])
        }

    def get_config(self):
        config = super().get_config().copy()
        config.update({
            'vocabulary': self.vocabulary
        })
        return config


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
            cat: Instance of `tf.Tensor`
                `tf.Tensor` with categorical values
                shape: [batch]                
           

        Returns:
            means: Instance of `tf.Tensor`
                Means `tf.Tensor` of the output mixture distribution
                shape: [batch, mix, inDim*len(vocabulary)]
            covariances: Instance of `tf.Tensor`
                Covariance matrix `tf.Tensor` of the output mixture distribution
                shape: [batch, mix, inDim*len(vocabulary), inDim*len(vocabulary)]
            weights: Instance of `tf.Tensor`
                Weight `tf.Tensor` ot the mixture components
                shape: [batch, mix]
        """

        # extract the batch size from the means tensor
        _batchSize = _tf.shape(x["means"])[0]

        catType = self.lookupLayer(x["cat"])
        catType = _tf.expand_dims(_tf.one_hot(catType, self.vocabulary_len), 2)

        # compute thie bias for each cat type
        bias = _tf.cond(self.sampling,
                         lambda: _tf.reduce_sum(catType * self.bias.sample(_batchSize), 1),
                         lambda: _tf.reduce_sum(catType * self.bias_mean, 1)
                         )
        
        # add the batch shape
        bias = _tf.expand_dims(bias, 1)

        # compute the linear transformation
        new_means = x["means"] + bias


        return {
            "means": new_means,
            "covariances": x["covariances"],
            "weights": x["weights"]
        }