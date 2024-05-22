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


import numpy as _np
from dataclasses import dataclass as _dataclass
from typing import List
import itertools


@_dataclass
class SingleBin:
    """
    define a single bin as a Gaussian mixture with a
    diagonal covariance matrix
    """
    means: _np.ndarray
    weights: _np.ndarray
    covariances: _np.ndarray
    area: float
    name: str

    @property
    def as_gmm(self):
        """ return the SingleBin dataclass as sklean GaussianMixture
        """
        from sklearn.mixture import GaussianMixture

        gmm = GaussianMixture(
            n_components=(len(self.weights)),
            covariance_type="diag"
        )
        gmm.fit(self.means)
        gmm.means_ = self.means
        gmm.weights_ = self.weights
        gmm.covariances_ = self.covariances

        return gmm
    
    def sample(self, n):
        return self.as_gmm.sample(n)[0]
    
    def plot(self, dims=None, **kwargs):
        import plotly.express as px

        if dims:
            return px.scatter(
                x=self.means[:, dims[0]],
                y=self.means[:, dims[1]],
                error_x=_np.sqrt(self.covariances[:, dims[0]]),
                error_y=_np.sqrt(self.covariances[:, dims[1]]),
                size=self.weights,
                **kwargs
            )              

        if self.means.shape[1] > 1:
            return px.scatter(
                x=self.means[:, 0],
                y=self.means[:, 1],
                error_x=_np.sqrt(self.covariances[:, 0]),
                error_y=_np.sqrt(self.covariances[:, 1]),
                size=self.weights,
                **kwargs
            )
        return px.scatter(
            x=self.means[:, 0],
            error_x=_np.sqrt(self.covariances[:, 0]),
            size=self.weights,
            **kwargs
        )        



class BinningScheme:
    """
    define a single bin by an array of sample points
    and an area weight
    """

    def __init__(self) -> None:
        self.bins: List[SingleBin] = []

    def append(self, input: SingleBin):
        """
        Append SingleBin to the end of the list
        """
        self.bins.append(input)

    def extend(self, input):
        """
        Extend SingleBin list or iterable to the end of the list
        """
        self.bins.extend(input)        

    @property
    def means(self):
        """Combined integration sample points."""
        return _np.stack([b.means for b in self.bins])

    @property
    def weights(self):
        """Combined weights"""
        return _np.stack([b.weights*b.area for b in self.bins])
    
    @property
    def covariances(self):
        """Combined diagonal part of the covariance matrix"""
        return _np.stack([b.covariances for b in self.bins])
    
    def to_dict(self, batch_tiles=1):
        return {
            "bin_means": [self.means.tolist()]*batch_tiles,
            "bin_covariances": [self.covariances.tolist()]*batch_tiles,
            "bin_weights": [self.weights.tolist()]*batch_tiles,
        }

    def __repr__(self):
        return f"BinningScheme(bins=[{', '.join([b.name for b in self.bins if b.name])}])"


def combine(bins: SingleBin) -> SingleBin:
    """
    combine muptiple SingleBins

    Parameters:
        bins:   array of SingleBins
                the bins to combine

   Returns:
        A new SingleBin
    """
    
    def product(*point_lists):
        return _np.stack(
            [_np.concatenate(combination) for combination in itertools.product(*point_lists)]
        )

    return SingleBin(
        means=product(*[el.means for el in bins]),
        covariances=product(*[el.covariances for el in bins]),
        weights=_np.prod(product(*[_np.expand_dims(el.weights, 1) for el in bins]), axis=1),
        area=_np.prod([b.area for b in bins]),
        name="_".join([b.name for b in bins if b.name])
    )    


def getPolygonBin(points,
                  name=None,
                  n=250,
                  n_start=None,
                  n_oversample=100.0,
                  tol = 1e-1,
                  max_iter = 5000,
                  ) -> SingleBin:
    """
    compute `n` sample points inside a polygon, such that the polygon is optimaly covered

    Parameters:
        points:   array, shape (n_points, 2)
                  the points of the polygon (in 2d)

        name:     str
                  Name of the bin

        n:        int
                  number of points to compute

        n_start:  int
                  number of points to start with

        n_oversample:  float
                  factor used to multiply the number of output points for optimization                 

        tol:      float
                  tolerance of the fitting process

        max_iter: int
                  number of maximal iterations of the fitting process

   Returns:
        A `SingleBin` of sample points with dimension (n, 2)

    """
    from shapely.geometry import Point
    from shapely.geometry.polygon import Polygon
    #from sklearn.mixture import BayesianGaussianMixture
    from sklearn.mixture import GaussianMixture

    polygon = Polygon(points)

    polygon_area_ratio = polygon.area / \
        (polygon.bounds[2]-polygon.bounds[0]) / \
        (polygon.bounds[3]-polygon.bounds[1])

    if n_start == None:
        n_start = int(n * n_oversample / polygon_area_ratio)

    # the outer bounds of the polygon:
    x0 = _np.array([polygon.bounds[0], polygon.bounds[1]])
    x1 = _np.array([polygon.bounds[2], polygon.bounds[3]])

    # compute the bound lengts and grid spacing
    l0 = abs(x1[0]-x0[0])
    l1 = abs(x1[1]-x0[1])
    factor = _np.sqrt(n_start/(l0*l1))

    # compute a meshgrid
    grid = _np.meshgrid(
        _np.linspace(x0[0], x1[0], abs(int(factor*l0))),
        _np.linspace(x0[1], x1[1], abs(int(factor*l1)))
    )

    # samples that cover the outer bound
    samples = _np.stack(
        [
            grid[0].flatten(),
            grid[1].flatten()
        ], 1
    )
    _np.random.shuffle(samples)

    # samples only within the polygon
    samples = _np.stack([s for s in samples if polygon.contains(Point(s))])

    bgm = GaussianMixture(
        n_components=n,
        random_state=42,
        covariance_type="diag",
        max_iter=max_iter,
        tol=tol,
        n_init=1,
        reg_covar=1e-20
    ).fit(samples)

    return SingleBin(
        means=bgm.means_,
        covariances=bgm.covariances_,
        weights=bgm.weights_,
        area=polygon.area,
        name=name)




def getRangeBin(min, max, name=None, 
                n=30,
                n_start=None,                
                n_oversample=200.0,
                tol = 1e-2,
                max_iter = 5000,
                ) -> SingleBin:
    """
    compute `n` sample points inside [min, max], such that the range is optimaly covered
    Parameters:
        min:      float
                  the minimum of the range
        max:      float
                  the maximum of the range    
        name:     str
                  Name of the bin              
        n:        int
                  number of points to compute
        n_start:  int
                  number of points to start with

        n_oversample:  float
                  factor used to multiply the number of output points for optimization                 

        tol:      float
                  tolerance of the fitting process

        max_iter: int
                  number of maximal iterations of the fitting process

              
   Returns:
        A `SingleBin` of sample points with dimension (n, 1)
    """
    from sklearn.mixture import GaussianMixture

    if n_start == None:
        n_start = int(n*n_oversample)

    spacing = (max-min)/(n_start)
    train_points =  _np.linspace(min+spacing/2, max-spacing/2, abs(n_start))
    train_points = _np.expand_dims(train_points, 1)

    bgm = GaussianMixture(
        n_components=n,
        random_state=42,
        covariance_type="diag",
        max_iter=max_iter,
        tol=tol,
        n_init=1
    ).fit(train_points)

    return SingleBin(
        means=bgm.means_,
        covariances=bgm.covariances_,
        weights=bgm.weights_,
        area=abs(max-min),
        name=name)    
