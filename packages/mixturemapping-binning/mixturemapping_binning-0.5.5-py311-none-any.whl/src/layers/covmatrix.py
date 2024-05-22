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
from tensorflow.keras.layers import Layer as _Layer

from ._mapping import _M

# mixturemapping imports
from ..distributions import createCovMatrix as _createCovMatrix
from ..distributions import regularizeCovMatrix as _r


class TrainableCovMatrix(_Layer):
    """Generates an independently trainable covariance matrix

    Important symmetry properties are generated automatically because the covariance matrix
    is built up from standard deviations `TrainableCovMatrix.spread`
    and correlations `TrainableCovMatrix.corr`.
    
    Params:
      output


    """

    def __init__(self, output_dim, regularize=None,  **kwargs):
        self._output_dim = output_dim
        self._regularize = regularize
        super(TrainableCovMatrix, self).__init__(**kwargs)

    def build(self, input_shapes):
        input_shape = input_shapes[0]

        # Create trainable weighs
        self.spread = self.add_weight(name='spread', shape=(
            1,  self._output_dim), initializer='uniform', trainable=True, )
        correlationSize = int(self._output_dim * (self._output_dim-1) / 2)
        if correlationSize > 0:
            self.corr = self.add_weight(name='correlation', shape=(
                correlationSize,), initializer='uniform', trainable=True )
        else:
            self.corr = [0]

        # Create the compute graph for the covariance addon part
        matrix = _createCovMatrix(_tf.exp(self.spread), _tf.tanh(self.corr), self._output_dim)

        if(self._regularize):
            matrix = _r(matrix, self._regularize)

        self.matrix = matrix

        # call build of the base Layer class
        super(TrainableCovMatrix, self).build(input_shape)

    @_tf.function(autograph=False)
    def call(self, x, **kwargs):
        batch_size = _tf.shape(x)[0]
        return _tf.tile(self.matrix, [batch_size, 1, 1])

    def compute_output_shape(self, input_shape):
        return (input_shape[0], self._output_dim, self._output_dim)


    def get_config(self):
        config = super().get_config().copy()
        config.update({
            'output_dim': self._output_dim,
            'regularize': self._regularize
        })
        return config


class VarCovMatrix(_M):
    """Generates an variational covariance matrix

    Important symmetry properties are generated automatically because the covariance matrix
    is built up from standard deviations `VarCovMatrix.spread`
    and correlations `VarCovMatrix.corr`.
    
    Params:
      output

    """

    def __init__(self, output_dim, regularize=None,  **kwargs):
        self._output_dim = output_dim
        self._regularize = regularize
        super(VarCovMatrix, self).__init__(output_dim=output_dim, **kwargs)

    def build(self, input_shapes):
        input_shape = input_shapes[0]

        # Create trainable weighs
        self.spread_mean = self.add_weight(name='spread_mean', shape=(self._output_dim,), initializer='normal', trainable=True, )
        self.spread_std = self.add_weight(name='spread_std', shape=(self._output_dim,), initializer='normal', trainable=True, )

        self.spread = _tfd.Normal(self.spread_mean, _tf.exp(self.spread_std))

        correlationSize = int(self._output_dim * (self._output_dim-1) / 2)
        if correlationSize > 0:
            self.corr = self.add_weight(name='correlation_mean', shape=(correlationSize,), initializer='normal', trainable=True)
        else:
            self.corr = [0]

        # call build of the base Layer class
        super(VarCovMatrix, self).build(input_shape)

    @_tf.function(autograph=False)
    def call(self, x, **kwargs):
        batch_size = _tf.shape(x)[0]


        # compute varational or mean depending on sampling ON and OFF
        spread = _tf.cond(self.sampling,
                           lambda: _tf.exp(self.spread.sample(batch_size)),
                           lambda: _tf.expand_dims(_tf.exp(self.spread_mean), 0)
                         )
        
        corr = _tf.expand_dims(_tf.tanh(self.corr), 0)

        # Create the compute graph for the covariance addon part
        matrix = _createCovMatrix(spread, corr, self._output_dim)

        if(self._regularize):
            matrix = _r(matrix, self._regularize)

        self.matrix = matrix

        return matrix

    def compute_output_shape(self, input_shape):
        return (input_shape[0], self._output_dim, self._output_dim)


    def get_config(self):
        config = super().get_config().copy()
        config.update({
            'output_dim': self._output_dim,
            'regularize': self._regularize
        })
        return config
