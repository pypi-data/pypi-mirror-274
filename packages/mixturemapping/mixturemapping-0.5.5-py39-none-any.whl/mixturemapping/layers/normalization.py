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

_D='weights'
_C='covariances'
_B=None
_A='means'
import tensorflow as _tf,numpy as _np
class _FixedBase(_tf.keras.layers.Layer):
	def __init__(A,mean=_B,std=_B,samples=_B,**C):
		B=samples;super(_FixedBase,A).__init__(**C)
		if B is not _B:A.mean=_np.median(_np.median(B,axis=1),axis=0).tolist();A.std=_np.std(_np.median(B,axis=1),axis=0).tolist()
		else:assert mean is not _B,'normalization.Fixed  needs mean and std or samples';assert std is not _B,'normalization.Fixed needs mean and std or samples';A.mean=mean;A.std=std
	def build(A,input_shapes):
		B=input_shapes
		if not(_A in B and _D in B):raise Exception('means and weights are needed to construct the mapping layer!')
		A.trafo_mean=_tf.expand_dims(_tf.expand_dims(_tf.constant(A.mean,dtype=A.dtype),0),0);A.trafo_std=_tf.expand_dims(_tf.expand_dims(_tf.constant(A.std,dtype=A.dtype),0),0);C=_np.expand_dims(A.std,0)*_np.expand_dims(A.std,1);A.trafo_cov=_tf.expand_dims(_tf.expand_dims(_tf.constant(C,dtype=A.dtype),0),0)
	def compute_output_shape(B,input_shape):A=input_shape;return{_A:(A[_A][0],A[_A][1],B.output_dim),_C:(A[_A][0],A[_A][1],B.output_dim,B.output_dim),_D:(A[_A][0],A[_A][1])}
	def get_config(A):B=super().get_config().copy();B.update({'mean':A.mean,'std':A.std});return B
class FixedForward(_FixedBase):
	@_tf.function(autograph=False)
	def call(self,x,**B):A=self;x=x.copy();x[_A]=(x[_A]-A.trafo_mean)/A.trafo_std;x[_C]=x[_C]/A.trafo_cov;return x
class FixedBackward(_FixedBase):
	@_tf.function(autograph=False)
	def call(self,x,**B):A=self;x=x.copy();x[_A]=x[_A]*A.trafo_std+A.trafo_mean;x[_C]=x[_C]*A.trafo_cov;return x