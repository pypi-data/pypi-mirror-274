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

"""
Mixture Mapping
---------------

Provides:
  1. Layers to build tensorflow models to map Gaussian mixtures
  2. Tools to compute yield values of Gaussian mixtures in complex binning schemes

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

    deltaModel = tf.keras.Sequential()
    deltaModel.add( tf.keras.layers.Dense(40, activation="relu", kernel_regularizer=regularizers.l2(0.001)) )
    deltaModel.add( tf.keras.layers.Dense(40, activation="relu", kernel_regularizer=regularizers.l2(0.001)) )
    deltaModel.add( tf.keras.layers.Dense(outputMixM))

    covALayer = mm.layers.TrainableCovMatrix(outputMixM, name="CovA")
    covA = covALayer(inMeans)

    mapLayer = mm.layers.GeneralMapping(outputMixM, yModel=mapModel, yDeltaModel=deltaModel,
      name="Mapping", dtype=dataType)
    newDist = mapLayer({'means': inMeans, 'stdDevs': inStdDevs, 'weights': inWeight, 'covA': covA})

    distLayer = mm.layers.Distribution(dtype=dataType, regularize_cov_epsilon=0.95)
    dist = distLayer(newDist)
"""


from . import utils
from . import distributions
from . import layers
from . import binning


__all__ = ['utils', 'distributions', 'layers', 'binning']

__version__ = '0.5.0'



import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}
import tensorflow as tf
tf.get_logger().setLevel('INFO')
tf.autograph.set_verbosity(0)
import logging
tf.get_logger().setLevel(logging.ERROR)