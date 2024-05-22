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

from doctest import OutputChecker
import tensorflow.python.ops
from tensorflow.python.ops import control_flow_ops as _control_flow_ops
import tensorflow as _tf
def getSkleanGM(weights,means,stdOrCov):
	D=stdOrCov;C=means;from numpy import square as G,shape as A;from sklearn.mixture import GaussianMixture as H;from sklearn.mixture._gaussian_mixture import _compute_precision_cholesky as I
	if len(A(C))!=len(A(D)):
		if A(C)[-1]==A(D)[-1]and A(C)[-1]==A(D)[-2]and A(C)[0]==A(D)[0]:E='full';F=D
		else:raise'Full covariance matrices not implemented yet?'
	else:E='diag';F=G(D)
	J=A(C)[-2];B=H(J,covariance_type=E);B.means_=C;B.weights_=weights;B.covariances_=F;B.precisions_cholesky_=I(B.covariances_,B.covariance_type);return B
def lastEntryJacobian(ys,xs,use_pfor=True,parallel_iterations=None,name='Jacobian',stop_gradients=None):
	G=stop_gradients;F=parallel_iterations;A=ys
	with _tf.name_scope(name):
		C=A.shape.ndims-1;D=A.shape[C]
		if use_pfor:
			def E(i):return _tf.gradients(_tf.gather(A,i,axis=C),xs,stop_gradients=G)[0]
			B=_control_flow_ops.pfor(E,D,parallel_iterations=F)
		else:
			def E(i):return _tf.gradients(_tf.gather(A,i,axis=C),xs,stop_gradients=G)
			B=_control_flow_ops.for_loop(E,A.dtype,D,parallel_iterations=F)
		B=_tf.transpose(B,[*[A+1 for A in range(A.shape.ndims)],0],name='OrderMatrix');B.set_shape([*[A for A in A.shape[0:-1]],xs.shape[-1],D]);return B