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
from ._mapping import _M
import numpy as _np
import tensorflow as _tf
import tensorflow_probability as _tfp
_tfd = _tfp.distributions

# internal inmports
from ..distributions import regularizeCovMatrix as _r


class DynamicGMR(_M):
    """ A trainable mapping layer using gaussian mixtures.

    This layers can be used if an initial guess of a trained Gaussian mixture of the combined input and
    output coordinates is available.

    Example::

        import mixturemapping as mm

        gmr = mm.layers.DynamicGMR(
            output_dim=2,
            input_dim=2,
            mix_size=30,
        )

        transformedDist = gmr({"means": inMeans, "covariances": cov, "weights": inWeight})

        distLayer = mm.layers.Distribution(dtype=dataType, regularize_cov_epsilon=0.98)
        dist = distLayer(transformedDist)

        sample_loss = distLayer.sample_loss(inTsamples)  


    Parameters
    ----------
    output_dim: int
        size of the output dimension
    input_dim:  int
        size of the input dimension
    mix_size:   int
        size of the internally used GMM to represent the distribution
    n_components: int
        if set, the output GMM is limited to the most important n_components
    regularize_cov_epsilon: float
        if set, a maximal correlation is introduced (default: 0.98)
    inv_rcond: float
        singular value cutoffs for inverse (default: 1e-5)    
           


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

    def __init__(
            self,
            output_dim,
            input_dim,
            mix_size,
            n_components=None,
            regularize_cov_epsilon=0.95,
            inv_rcond = 1e-5,
            **kwargs):
        super(DynamicGMR, self).__init__(output_dim, **kwargs)
        self.mix_size = mix_size
        self.input_dim = input_dim
        self.var_size = self.output_dim + self.input_dim
        self.output_indices = list(range(self.input_dim, self.var_size))
        self._r = regularize_cov_epsilon
        self._rcond = inv_rcond

        # compute the input indices by inversion of the output indices
        inv = _np.ones(self.var_size, dtype=bool)
        inv[self.output_indices] = False
        inv, = _np.where(inv)
        self.input_indices = inv

        self.n_components = n_components
        self.corr_size = int(self.var_size * (self.var_size-1) / 2)



    def _to_np(self, a):
        if isinstance(a, _np.ndarray):
            return a
        else:
            return _np.array(a, dtype=self.dtype)


    def set_gmm_values(self, means, covariances, weights):
        """ Set the GMM parameters without creating new tensorflow operations

        Parameters
        ----------
        means : numpy array 
            Means array of the combined mixture distribution
            shape: [mix, inDim]
        covariances : numpy array 
            Covariances array of the combined mixture distribution
            shape: [mix, inDim, inDim]    
        weights : numpy array 
            Weights array of the combined mixture distribution
            shape: [mix]           
        """

        # transform inputs into the right shape
        input_spread = _np.array([_np.sqrt(_np.diagonal(m))
                                 for m in covariances])
        input_corr = covariances / _np.reshape(input_spread, [self.mix_size, 1, self.var_size]) / _np.reshape(
            input_spread, [self.mix_size, self.var_size, 1])
        triu_indices = _np.triu_indices(self.var_size, 1)
        input_corr = input_corr[:, triu_indices[0], triu_indices[1]]

        # const_input_corr_idx = [idx for idx, (x, y) in enumerate(_np.transpose(
        #     triu_indices)) if x in self._input_indices and y in self._input_indices]
        # var_input_corr_idx = [idx for idx in range(
        #     self._corr_size) if idx not in const_input_corr_idx]

        # set the trainable variable parts
        _tf.keras.backend.set_value(self.model_cov_stddev_i, _np.log(input_spread)[:, self.input_indices])
        _tf.keras.backend.set_value(self.model_cov_stddev_o, _np.log(input_spread)[:, self.output_indices])
        _tf.keras.backend.set_value(self.model_cov_stddev_o_spread, _np.ones( (self.mix_size, self.output_dim))*-2.0)
        _tf.keras.backend.set_value(self.model_m_i, means[:, self.input_indices])
        _tf.keras.backend.set_value(self.model_m_o, means[:, self.output_indices])
        _tf.keras.backend.set_value(self.model_cov_corr, _np.arctanh(input_corr))
        _tf.keras.backend.set_value(self.model_w, weights)


    def fit_gmms(self, np_inputs, tf_inputs, input_gmm, output_gmm, n_samples=10):
        """fit_gmms can be used to pretrain the internal gmm

        Parameters
        ----------
        np_inputs:  dict of np.array
            The numpy inputs needed to train the model
        tf_inputs:  dict of input tensors
            The inputs needed to compute the tensorflow model      
        input_gmm:  mixturemaping gmm
            dict of means, covariances and weights to define the input gmm
        output_gmm: mixturemaping gmm
            dict of means, covariances and weights to define the output gmm
        n_samples: int
            number of sampels to model each input gmm
        """

        from sklearn.mixture import GaussianMixture
        from .distribution import Distribution, DistributionSamples

        # create the model for the input samples
        input_dist = Distribution()(input_gmm)
        input_samples_tf = DistributionSamples(n_samples)(input_dist)

        # create the model for the output samples
        output_dist = Distribution()(output_gmm)
        output_samples_tf = DistributionSamples(n_samples)(output_dist)

        # combine the samples
        samples_tf = _tf.reshape(
                _tf.transpose(
                _tf.concat([input_samples_tf, output_samples_tf], axis=1),
                [0, 2, 1]
            ),
            [-1, self.var_size]
        )

        sample_model =_tf.keras.Model(inputs=tf_inputs, outputs=samples_tf)
        sample_model.compile()
        samples = sample_model.predict(np_inputs)  

        trainModel = GaussianMixture(n_components=self.mix_size)

        # remove all nan rows
        samples_without_nan = samples[~_np.isnan(samples).any(axis=1)]
        trainModel.fit(samples_without_nan)

        self.set_gmm_values(
            means=trainModel.means_,
            covariances=trainModel.covariances_,
            weights=trainModel.weights_
        )


    def build(self, input_shapes):
        if not ("means" in input_shapes and "weights" in input_shapes):
            raise Exception(
                "means and weights are needed to construct the mapping layer!")

        # create the trainable parts
        # note the parts, which are describing the inputs, cannot be trained via backpropagation
        # thats why we split it up in input _i and output _o
        self.model_m_i = self.add_weight(
            name='mean_var_i',
            shape=(self.mix_size, self.input_dim),
            initializer='uniform',
            trainable=False            
        )
        self.model_cov_stddev_i = self.add_weight(
            name='cov_stddev_var_i',
            shape=( self.mix_size,  self.input_dim),
            initializer='uniform',
            trainable=True            
        )


        self.model_m_o = self.add_weight(
            name='mean_var_o',
            shape=(self.mix_size, self.output_dim),
            initializer='uniform',
            trainable=True            
        )
        self.model_cov_stddev_o = self.add_weight(
            name='cov_stddev_var_o',
            shape=( self.mix_size,  self.output_dim),
            initializer='uniform',
            trainable=True            
        )
        self.model_cov_stddev_o_spread = self.add_weight(
            name='cov_stddev_var_o_delta',
            shape=( self.mix_size,  self.output_dim),
            initializer='uniform',
            trainable=True            
        )        

        self.model_cov_corr = self.add_weight(
            name='cov_corr_var',
            shape=( self.mix_size,  self.corr_size),
            initializer='uniform',
            trainable=True            
        )

        self.model_w = self.add_weight(
            name='weight_var',
            shape=(self.mix_size,),
            initializer='uniform',
            trainable=False         
        )

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

        # extract the important keys from the input dict
        means = x["means"]
        covariances = x["covariances"]
        weights = x["weights"]

        # extract the batch size from the means tensor
        _batchSize = _tf.shape(means)[0]

        # combine the trainable an non trainable parts for the means
        model_m = _tf.concat([self.model_m_i, self.model_m_o], axis=-1)

        # combine the trainable and non trainable parts for for a 100% correlated cov matrix
        # we make this variational
        def get_base_cov():
            model_cov_stddev = _tf.concat([self.model_cov_stddev_i, self.model_cov_stddev_o], axis=-1)
            model_cov_stddev = _tf.exp(model_cov_stddev)
            return _tf.tile(_tf.expand_dims(
                _tf.matmul(_tf.reshape(model_cov_stddev, [self.mix_size, self.var_size, 1], name="colVec"),
                           _tf.reshape(model_cov_stddev, [self.mix_size, 1, self.var_size], name="rowVec"),
                           name="baseCovMatrix"),
                           0), [_batchSize, 1, 1, 1])
        
        def get_base_cov_var():

            model_cov_stddev_o = _tfd.Normal(self.model_cov_stddev_o, _tf.exp(self.model_cov_stddev_o_spread)).sample(_batchSize)
            model_cov_stddev_i = _tf.tile(_tf.expand_dims(self.model_cov_stddev_i, 0), [_batchSize, 1, 1])

            model_cov_stddev = _tf.concat([model_cov_stddev_i, model_cov_stddev_o], axis=-1)

            model_cov_stddev = _tf.exp(model_cov_stddev)
            return _tf.matmul(_tf.reshape(model_cov_stddev, [_batchSize, self.mix_size, self.var_size, 1], name="colVec"),
                              _tf.reshape(model_cov_stddev, [_batchSize, self.mix_size, 1, self.var_size], name="rowVec"),
                              name="baseCovMatrix")
        
        baseCovMatrix = _tf.cond(self.sampling, get_base_cov_var, get_base_cov)

        # 1. rescale trainable vars
        model_cov_corr = _tf.expand_dims(_tf.tanh(self.model_cov_corr), 0)
        
        # 3. add the correlation values from the model_cov_corr tensor
        step = self.var_size-1
        offset = [-1]
        for i in range(self.var_size-1):
            step = step - 1
            offset.append(offset[-1] + step)
        with _tf.name_scope("TransposedCorrelation"):
            output = [[baseCovMatrix[:, :, x, y] if x == y else
                       baseCovMatrix[:, :, x, y] * model_cov_corr[:, :, y + offset[x]] if x < y else
                       baseCovMatrix[:, :, x, y] * model_cov_corr[:, :, x + offset[y]]
                       for x in range(self.var_size)] for y in range(self.var_size)]
        
        model_cov = _tf.transpose(output, [2, 3, 0, 1], name="TransposeBack")     

        # 4. extend the array sizes because we have to compute multiple overlaps between all Gaussians
        model_m = _tf.expand_dims(_tf.expand_dims(model_m, 0), 2)
        model_w = _tf.expand_dims(_tf.expand_dims(self.model_w, 0), 2)       
        # note the cov matrix might be already different for each entry of the batch
        model_cov = _tf.expand_dims(model_cov, 2) 

        # regularize the covmatrix if needed
        if self._r:
            model_cov = _r(model_cov, self._r)


        # 5. cut the parts from means and covariances based on the input and output indices
        s11 = _tf.stop_gradient(_tf.gather(_tf.gather(model_cov, self.input_indices, axis=3), self.input_indices, axis=4))
        s22 = _tf.gather(_tf.gather(model_cov, self.output_indices, axis=3), self.output_indices, axis=4)

        s11I = _tf.linalg.pinv(s11, self._rcond)
        s21 = _tf.gather(_tf.gather(
            model_cov, self.output_indices, axis=3), self.input_indices, axis=4)
        s12 = _tf.linalg.matrix_transpose(s21)

        mu1 = _tf.gather(model_m, self.input_indices, axis=3)
        mu2 = _tf.gather(model_m, self.output_indices, axis=3)

        p = _tfd.MultivariateNormalTriL(
            loc=mu1,
            scale_tril=_tf.linalg.cholesky(s11)
        )

        # 6. extract input sizes
        shape = _tf.shape(means)
        batch_dim = shape[0]
        input_mix_dim = shape[1]

        # 7. expand the input gmm to allow the tensor thing
        m = _tf.expand_dims(means, 1)
        cov = _tf.expand_dims(covariances, 1)
        w = _tf.expand_dims(weights, 1)

        # 8. some lin algebra :D
        out_m = mu2 + _tf.linalg.matmul(
            _tf.linalg.matmul(s21, s11I),
            _tf.expand_dims((m - mu1), 4)
        )[:, :, :, :, 0]

        sigma_addon = _tf.linalg.matmul(_tf.linalg.matmul(_tf.linalg.matmul(
            _tf.linalg.matmul(s21, s11I),
            cov),
            s11I), s12)

        out_cov = s22 - _tf.matmul(_tf.matmul(s21, s11I), s12) + sigma_addon

        prop = model_w * p.prob(m)

        total_prop = _tf.reduce_sum(prop, axis=1, keepdims=True)
        prop = prop/total_prop
        prop *= w

        out_m = _tf.reshape(
            out_m, shape=[batch_dim, input_mix_dim*self.mix_size, self.output_dim])
        out_cov = _tf.reshape(out_cov, shape=[
                              batch_dim, input_mix_dim*self.mix_size, self.output_dim, self.output_dim])
        out_w = _tf.reshape(prop, shape=[batch_dim, input_mix_dim*self.mix_size])

        if self.n_components:
            k = _tf.minimum(self.n_components,
                            input_mix_dim*self.mix_size)
            topk = _tf.math.top_k(out_w, k=k)

            out_w = topk.values
            total_prop = _tf.reduce_sum(out_w, axis=1, keepdims=True)
            out_w = out_w/total_prop

            out_m = _tf.gather(out_m, topk.indices, axis=1, batch_dims=1)
            out_cov = _tf.gather(out_cov, topk.indices, axis=1, batch_dims=1)

        return {
                "means": out_m,
                "covariances": out_cov,
                "weights": out_w
            }
    
    

    def get_config(self):
        config = super().get_config().copy()

        config.update({
            'output_dim': self.output_dim,
            'input_dim': self.input_dim,
            'mix_size': self.mix_size,
            'n_components  ': self.n_components,
            'regularize_cov_epsilon': self._r,
            'inv_rcond': self._rcond
        })
        return config    