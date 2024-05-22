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
from ..distributions import regularizeCovMatrix as _r
from ._mapping import _M
import tensorflow as _tf
import tensorflow_probability as _tfp
_tfd = _tfp.distributions

# internal imports


class GeneralMapping(_M):
    """ A free general mapping layer, that maps centers and distributions independently.

    This layers can be used if the relationship between input distributions
    and output distributions is free and general

    Parameters:
        yModel : Keras Model
            Keras Model that maps the means tensor to the output tensor
            input: [batch, mix, inDim]
            output: [batch, mix, outDim]
        yDeltaModel : KerasModel
            Keras Model that maps the means tensor the the output uncertainty
            input: [batch, mix, inDim]
            output: [batch, mix, outDim]    

    Example::

        import mixturemapping as mm  
        import tensorflow as tf

        inMeans = tf.keras.Input(shape=(mixN, inputMixM), name="Means", dtype=dataType)
        inStdDevs = tf.keras.Input(shape=(mixN, inputMixM), name="StdDevs", dtype=dataType)
        inWeight = tf.keras.Input(shape=(mixN), name="Weights", dtype=dataType)

        mapModel = tf.keras.Sequential()
        mapModel.add( tf.keras.layers.Dense(40, activation="relu", kernel_regularizer=regularizers.l2(0.001)) )
        mapModel.add( tf.keras.layers.Dense(40, activation="relu", kernel_regularizer=regularizers.l2(0.001)) )
        mapModel.add( tf.keras.layers.Dense(outputMixM))
        y = mapModel(inMeans)

        deltaModel = tf.keras.Sequential()
        deltaModel.add( tf.keras.layers.Dense(40, activation="relu", kernel_regularizer=regularizers.l2(0.001)) )
        deltaModel.add( tf.keras.layers.Dense(40, activation="relu", kernel_regularizer=regularizers.l2(0.001)) )
        deltaModel.add( tf.keras.layers.Dense(outputMixM))
        yDelta = deltaModel(inMeans)

        covALayer = mm.layers.TrainableCovMatrix(outputMixM, name="CovA")
        covA = covALayer(inMeans)

        mapLayer = mm.layers.GeneralMapping(outputMixM, name="Mapping", dtype=dataType, yModel=mapModel, yDeltaModel=yDeltaModel)
        newDist = mapLayer({'means': inMeans, 'stdDevs': inStdDevs, 'weights': inWeight, 'covA': covA})

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


    def __init__(self,
        *args,
        yModel = None,
        yDeltaModel = None,
        **kwargs
        ):
        super(GeneralMapping, self).__init__(*args, **kwargs)

        self.yModel = yModel
        self.yDeltaModel = yDeltaModel


    def build(self, input_shapes):
        if not ("means" in input_shapes and "weights" in input_shapes):
            raise Exception(
                "means,  weights are needed to construct the mapping layer!")

        # deduce the input shape from the x tensor
        self.mix_dim = input_shapes["means"][1]
        self.input_dim = input_shapes["means"][2]

        # call build of the base Layer class
        super(GeneralMapping, self).build(input_shapes["means"])

        self.yModel.build(input_shapes["means"])
        # add variables of the external models to the train variables
        for v in self.yModel.trainable_variables:
            self._trainable_weights.append(v)
                
        if self.yDeltaModel:
            self.yDeltaModel.build(input_shapes["means"])
            # add variables of the external models to the train variables
            for v in self.yDeltaModel.trainable_variables:
                        self._trainable_weights.append(v)                        


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
            covariances : Instance of `tf.Tensor`
                Cov Matrix Tensor of the input mixture distribution
                shape: [batch, mix, inDim, inDim]
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

        # apply the mapping model and compute the gradiens
        # we need this to map the distribution sizes!
        with _tf.GradientTape(persistent=True) as tape:
            inMeans = x["means"]

            # slice the input for all input dimensions
            inMeansArray = [inMeans[:, :, i] for i in range(self.input_dim)]

            # track the gradients individually for each input dimension
            for el in inMeansArray:
                tape.watch(el)
            newInMeans = _tf.stack(inMeansArray, 2)
            y = self.yModel(newInMeans)

            # slice the output for all output axis
            outMeansArray = [y[:, :, i] for i in range(self.output_dim)]

        # calculate the Jacobi Matrix for this external model with respect to the
        # input mean values in order to compute a mapping of the input distribution
        # sizes to the output
        self.jacobian = _tf.stack([_tf.stack([
            tape.gradient(outMeansArray[o], inMeansArray[i])
            for i in range(self.input_dim)
        ], 2) for o in range(self.output_dim)], 3, name="jacobian")

        # the mapping of the distributions centers is given by an external model
        # => the centers of the distributions are given by a sampeled distribution
        # if yDelta is given or just the values
        if self.yDeltaModel:
            yDelta = self.yDeltaModel(inMeans)
            self.mean_dist = _tfd.Normal(y, _tf.exp(yDelta))
            means = _tf.cond(self.sampling,
                             lambda: self.mean_dist.sample(),
                             lambda: y
                             )
        else:
            means = y


        if "stdDevs" in x:

            # assume the input x["stdDev"] contains standard deviations
            # and uses a vector form
            assert(x["stdDevs"].shape.ndims == 3)

            # extend stdDev Vector and bring it to the right order
            bigStdDev = _tf.expand_dims(x["stdDevs"], 3)

            # compute the transformed standard deviation with repect to the jacobi
            # transformation of the external model
            scaledKernel = _tf.multiply(
                bigStdDev, _tf.stop_gradient(self.jacobian))
        else:
            # assume the input contains a covariance matrix x["covariancesd"]

            # compute the squareroot of the covariance matrix
            sqrtCov = _tf.linalg.sqrtm(x["covariances"])

            # transform the standard deviation matrix with repect to the jacobi
            # transformation of the external model
            scaledKernel = _tf.matmul(
                sqrtCov, _tf.stop_gradient(self.jacobian))
        # END two ways to compute the scaled standard deviations

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


    def get_config(self):
        config = super().get_config().copy()
        config.update({
            'yModel': self.yModel.get_config()
        })

        if self.yDeltaModel:
            config.update({
                'yDeltaModel': self.yDeltaModel.get_config()
            })
        return config
