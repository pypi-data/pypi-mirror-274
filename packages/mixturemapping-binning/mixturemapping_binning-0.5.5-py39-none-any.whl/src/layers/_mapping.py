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
from tensorflow.keras.layers import Layer as _Layer
import tensorflow as _tf

class _M(_Layer):

    def __init__(self, output_dim, regularize_cov_epsilon=None, **kwargs):
        """
        Args:
          output_dim: size of the output dimension
          regularize_cov_epsilon: if not None cov matrix corelation is restricted (eg. 0.995)
        """
        
        super(_M, self).__init__(**kwargs)
        
        self.output_dim = output_dim
        self._regularize_cov_epsilon = regularize_cov_epsilon
        self.sampling = _tf.Variable(True, trainable=False, name="sampling")

    def sampling_ON(self):
        _tf.keras.backend.eval(self.sampling.assign(True))

    def sampling_OFF(self):
        _tf.keras.backend.eval(self.sampling.assign(False))

    def compute_output_shape(self, input_shape):
        return {
            "means": (input_shape["means"][0], input_shape["means"][1], self.output_dim),
            "covariances": (input_shape["means"][0], input_shape["means"][1], self.output_dim, self.output_dim),
            "weights": (input_shape["means"][0], input_shape["means"][1])
        }
    

    def get_config(self):
        config = super().get_config().copy()
        config.update({
            'regularize_cov_epsilon': self._regularize_cov_epsilon
        })
        return config


    