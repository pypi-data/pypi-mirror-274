## Copyright 2020-2023 Viktor Krueckl. All Rights Reserved.
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

_B='diag'
_A=None
import numpy as _np
from dataclasses import dataclass as _dataclass
from typing import List
import itertools
@_dataclass
class SingleBin:
	means:0;weights:0;covariances:0;area:0;name:0
	@property
	def as_gmm(self):A=self;from sklearn.mixture import GaussianMixture as C;B=C(n_components=len(A.weights),covariance_type=_B);B.fit(A.means);B.means_=A.means;B.weights_=A.weights;B.covariances_=A.covariances;return B
	def sample(A,n):return A.as_gmm.sample(n)[0]
	def plot(A,dims=_A,**C):
		B=dims;import plotly.express as D
		if B:return D.scatter(x=A.means[:,B[0]],y=A.means[:,B[1]],error_x=_np.sqrt(A.covariances[:,B[0]]),error_y=_np.sqrt(A.covariances[:,B[1]]),size=A.weights,**C)
		if A.means.shape[1]>1:return D.scatter(x=A.means[:,0],y=A.means[:,1],error_x=_np.sqrt(A.covariances[:,0]),error_y=_np.sqrt(A.covariances[:,1]),size=A.weights,**C)
		return D.scatter(x=A.means[:,0],error_x=_np.sqrt(A.covariances[:,0]),size=A.weights,**C)
class BinningScheme:
	def __init__(A):A.bins=[]
	def append(A,input):A.bins.append(input)
	def extend(A,input):A.bins.extend(input)
	@property
	def means(self):return _np.stack([A.means for A in self.bins])
	@property
	def weights(self):return _np.stack([A.weights*A.area for A in self.bins])
	@property
	def covariances(self):return _np.stack([A.covariances for A in self.bins])
	def to_dict(A,batch_tiles=1):B=batch_tiles;return{'bin_means':[A.means.tolist()]*B,'bin_covariances':[A.covariances.tolist()]*B,'bin_weights':[A.weights.tolist()]*B}
	def __repr__(A):return f"BinningScheme(bins=[{', '.join([A.name for A in A.bins if A.name])}])"
def combine(bins):
	A=bins
	def B(*A):return _np.stack([_np.concatenate(A)for A in itertools.product(*A)])
	return SingleBin(means=B(*[A.means for A in A]),covariances=B(*[A.covariances for A in A]),weights=_np.prod(B(*[_np.expand_dims(A.weights,1)for A in A]),axis=1),area=_np.prod([A.area for A in A]),name='_'.join([A.name for A in A if A.name]))
def getPolygonBin(points,name=_A,n=250,n_start=_A,n_oversample=1e2,tol=.1,max_iter=5000):
	E=n_start;from shapely.geometry import Point;from shapely.geometry.polygon import Polygon as K;from sklearn.mixture import GaussianMixture as L;A=K(points);M=A.area/(A.bounds[2]-A.bounds[0])/(A.bounds[3]-A.bounds[1])
	if E==_A:E=int(n*n_oversample/M)
	B=_np.array([A.bounds[0],A.bounds[1]]);C=_np.array([A.bounds[2],A.bounds[3]]);G=abs(C[0]-B[0]);H=abs(C[1]-B[1]);I=_np.sqrt(E/(G*H));J=_np.meshgrid(_np.linspace(B[0],C[0],abs(int(I*G))),_np.linspace(B[1],C[1],abs(int(I*H))));D=_np.stack([J[0].flatten(),J[1].flatten()],1);_np.random.shuffle(D);D=_np.stack([B for B in D if A.contains(Point(B))]);F=L(n_components=n,random_state=42,covariance_type=_B,max_iter=max_iter,tol=tol,n_init=1,reg_covar=1e-20).fit(D);return SingleBin(means=F.means_,covariances=F.covariances_,weights=F.weights_,area=A.area,name=name)
def getRangeBin(min,max,name=_A,n=30,n_start=_A,n_oversample=2e2,tol=.01,max_iter=5000):
	A=n_start;from sklearn.mixture import GaussianMixture as E
	if A==_A:A=int(n*n_oversample)
	D=(max-min)/A;B=_np.linspace(min+D/2,max-D/2,abs(A));B=_np.expand_dims(B,1);C=E(n_components=n,random_state=42,covariance_type=_B,max_iter=max_iter,tol=tol,n_init=1).fit(B);return SingleBin(means=C.means_,covariances=C.covariances_,weights=C.weights_,area=abs(max-min),name=name)