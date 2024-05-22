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

# import tensorflow parts
import tensorflow as _tf
import tensorflow_probability as _tfp
_tfd = _tfp.distributions


def createCovMatrix(stdDevTensor, correlationTensor, size, name="CorrelationMatrix"):
    """Create a covariance matrix from stdDev, correlation and the desired output size

    The function computes a square covariance matrix from the input standard
    deviations and then reduces correlation values based on the correlationTensor

    Args:
      stdDevTensor: tensorflow::Tensor
        A tensorflow::Tensor with all standard deviations (shape=[batch, dim])
      corrTensor: tensorflow::Tensor
        A tensorflow::Tensor will all correlation values (shape=[batch, dim2])
      size: int
        Python int of the output matrix size used for index mapping between stdDev and
        correlation

    Returns: 
      A Tensor with a batch of covariance matrices (shape=[batch, dim, dim])
    """

    with _tf.name_scope(name):
        # extract the batch size from the stdDeviation tensor
        batchSize = _tf.shape(stdDevTensor)[0]

        # offset matrix used to compute the index of the correlationTensor entry for the final matrix
        step = size-1
        offset = [-1]
        for i in range(size-1):
            step = step - 1
            offset.append(offset[-1] + step)

        # compute the full [size x size] matrix from the stdDev tensor
        baseCovMatrix = _tf.matmul(_tf.reshape(stdDevTensor, [batchSize, size, 1], name="colVec"),
                                   _tf.reshape(stdDevTensor, [
                                               batchSize, 1, size], name="rowVec"),
                                   name="CovMatrix")
        
        # apply the correlation
        if _tf.shape(correlationTensor).shape[0] == 1:
          # correlation different fo each entry
          with _tf.name_scope("AddCorrelation"):
              output = [[baseCovMatrix[:, x, y] if x == y else
                        baseCovMatrix[:, x, y] * correlationTensor[y + offset[x]] if x < y else
                        baseCovMatrix[:, x, y] *
                        correlationTensor[x + offset[y]]
                        for x in range(size)] for y in range(size)]
        else:
          # same correlation for each entry
          with _tf.name_scope("AddCorrelation"):
              output = [[baseCovMatrix[:, x, y] if x == y else
                        baseCovMatrix[:, x, y] * correlationTensor[:, y + offset[x]] if x < y else
                        baseCovMatrix[:, x, y] *
                        correlationTensor[:, x + offset[y]]
                        for x in range(size)] for y in range(size)]            

        # transform to bring the batch index back to
        return _tf.transpose(output, name=name+"Transpose")


def regularizeCovMatrix(covMatrix, epsilon=0.999):
    """regularize a covariance matrix to prevent cholesky transform errors

    The code assumes the last two components of the input tensor to be a covariance matrix.
    We regularize by multiplying all off diagonal elements with epsilon (default: 0.999)

    Args:
      covMatrix: tensorflow:Tensor of the covariance. Dimensions: (..., M, M) with M of the covariance
      epsilon: correlation reduction (default:0.999)
    """

    # extract the diagonal part and compute the square root
    diagMatrix = _tf.sqrt(_tf.linalg.diag_part(covMatrix))

    # compute a covariance matrix with full correlation 1
    n = _tf.expand_dims(diagMatrix, -1)
    maxCorr = n*_tf.linalg.matrix_transpose(n)

    # reduce the covariance matrix
    corr = _tf.clip_by_value(_tf.divide(covMatrix, maxCorr), -epsilon, epsilon)
    # set the diagonal elements back to one
    newCorr = _tf.linalg.set_diag(corr, _tf.ones_like(diagMatrix))

    # compute a new covariance matrix from the max Values and the reduced off diagonal elements
    return _tf.multiply(newCorr, maxCorr)


def createMixDistBYmeanCovWeight(meanTensor, covTensor, weightTensor, mixSize, matrixSize, name="GaussianMixture"):
    """Create a TensorflowProbability mixture distribution as defined by the input Tensors

    The function computes a TensorflowProbability mixture distribution for the full batch based on
    gaussian distributions of the input parameters.
    The dimensions of the input tensors are ordered by [batch, mixCompnent, InputDimension]

    Args:
      meanTensor: tensorflow::Tensor
        Tensor with all mean values of the distributions (shape=[batch, mixSize, dim])
      covTensor: tensorflow::Tensor
        Tensor with all covariance Matrices (shape=[batch, mixSize, dim, dim])
      weightTensor: tensorflow::Tensor
        A tensorflow::Tensor with the mixture weights (shape=[batch, mixSize, dim2])
      mixSize: python int
        Python int of the distribution size
      matrixSize: python int
        Python int with the size of the output distribution

    Returns:
      A TensorflowProbability mixture distribution

    """

    with _tf.name_scope(name):

        # add name scope of the combined distribution
        with _tf.name_scope("CombinedDist"):

            # compute the cholesky from of all covariance matrices
            choleskyTensor = _tf.linalg.cholesky(covTensor)

            # create all Gaussian distribution
            dists = _tfd.MultivariateNormalTriL(
                loc=meanTensor, scale_tril=choleskyTensor, name="MultiTriL")

            # create the distribution weights
            cathegoricalWeights = _tfd.Categorical(
                probs=weightTensor, name="Weights")

            fullDist = _tfp.distributions.MixtureSameFamily(
                mixture_distribution=cathegoricalWeights,
                components_distribution=dists,
                name="MixtureSameFamily"
            )

        return fullDist


def createMixDistribution(meanTensor, stdDevTensor, correlationTensor, weightTensor, mixSize, matrixSize, name="GaussianMixture"):
    """Create a TensorflowProbability mixture distribution as defined by the input Tensors

    The function computes a TensorflowProbability mixture distribution for the full batch based on
    gaussian distributions of the input parameters.
    The dimensions of the input tensors are ordered by [batch, mixCompnent, InputDimension]

    Args:
      meanTensor: A tensorflow::Tensor with all mean values of the distributions (shape=[batch, mixSize, dim])
      stdDevTensor: A tensorflow::Tensor with all standard deviations (shape=[batch, mixSize, dim])
      correlationTensor: A tensorflow::Tensor with all correlation values (shape=[batch, mixSize, dim2])
      weightTensor: A tensorflow::Tensor with the mixture weights (shape=[batch, mixSize, dim2])
      mixSize: Python int of the distribution size
      matrixSize: Python int with the size of the output distribution

    Returns:
      A TensorflowProbability mixture distribution

    """

    with _tf.name_scope(name):
        # extract the batch size from the mean tensor
        batchSize = _tf.shape(meanTensor)[0]

        # arrays with all distribution centers and scales used for the gaussian mixture
        centers = []
        scales = []

        # add an extra name scope for all separated singe distributions
        with _tf.name_scope("SeparateDists"):

            # loop all mix model components
            for mId in range(mixSize):
                with _tf.name_scope("Part_"+str(mId+1)):

                    # extract values for single component
                    singleCenter = meanTensor[:, mId]
                    singleCov = stdDevTensor[:, mId]
                    singleCorr = correlationTensor[:, mId]

                    singleCovMat = createCovMatrix(
                        singleCov, singleCorr, matrixSize)

                    singleScale = _tf.linalg.cholesky(singleCovMat)

                    # add the components of a single distribtion to the array of the full distribution
                    centers.append(_tf.reshape(
                        singleCenter, [batchSize, 1, matrixSize], name="Center"))
                    scales.append(_tf.reshape(
                        singleScale, [batchSize, 1, matrixSize, matrixSize], name="Scale"))

        # add name scope of the combined distribution
        with _tf.name_scope("CombinedDist"):
            # combine all distribution components
            allCenters = _tf.concat(centers, 1, name="Centers")
            allScales = _tf.concat(scales, 1, name="Scales")

            # create all Gaussian distribution
            dists = _tfd.MultivariateNormalTriL(
                loc=allCenters, scale_tril=allScales, name="MultiTriL")

            # create the distribution weights
            cathegoricalWeights = _tfd.Categorical(
                probs=weightTensor, name="Weights")

            fullDist = _tfp.distributions.MixtureSameFamily(
                mixture_distribution=cathegoricalWeights,
                components_distribution=dists,
                name="MixtureSameFamily"
            )

        return fullDist
