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

_C='regularize'
_B='output_dim'
_A=True
import tensorflow as _tf,tensorflow_probability as _tfp
_tfd=_tfp.distributions
from tensorflow.keras.layers import Layer as _Layer
from._mapping import _M
from..distributions import createCovMatrix as _createCovMatrix
from..distributions import regularizeCovMatrix as _r
class TrainableCovMatrix(_Layer):
	def __init__(A,output_dim,regularize=None,**B):A._output_dim=output_dim;A._regularize=regularize;super(TrainableCovMatrix,A).__init__(**B)
	def build(A,input_shapes):
		D='uniform';E=input_shapes[0];A.spread=A.add_weight(name='spread',shape=(1,A._output_dim),initializer=D,trainable=_A);C=int(A._output_dim*(A._output_dim-1)/2)
		if C>0:A.corr=A.add_weight(name='correlation',shape=(C,),initializer=D,trainable=_A)
		else:A.corr=[0]
		B=_createCovMatrix(_tf.exp(A.spread),_tf.tanh(A.corr),A._output_dim)
		if A._regularize:B=_r(B,A._regularize)
		A.matrix=B;super(TrainableCovMatrix,A).build(E)
	@_tf.function(autograph=False)
	def call(self,x,**B):A=_tf.shape(x)[0];return _tf.tile(self.matrix,[A,1,1])
	def compute_output_shape(A,input_shape):return input_shape[0],A._output_dim,A._output_dim
	def get_config(A):B=super().get_config().copy();B.update({_B:A._output_dim,_C:A._regularize});return B
class VarCovMatrix(_M):
	def __init__(A,output_dim,regularize=None,**C):B=output_dim;A._output_dim=B;A._regularize=regularize;super(VarCovMatrix,A).__init__(output_dim=B,**C)
	def build(A,input_shapes):
		B='normal';D=input_shapes[0];A.spread_mean=A.add_weight(name='spread_mean',shape=(A._output_dim,),initializer=B,trainable=_A);A.spread_std=A.add_weight(name='spread_std',shape=(A._output_dim,),initializer=B,trainable=_A);A.spread=_tfd.Normal(A.spread_mean,_tf.exp(A.spread_std));C=int(A._output_dim*(A._output_dim-1)/2)
		if C>0:A.corr=A.add_weight(name='correlation_mean',shape=(C,),initializer=B,trainable=_A)
		else:A.corr=[0]
		super(VarCovMatrix,A).build(D)
	@_tf.function(autograph=False)
	def call(self,x,**F):
		A=self;C=_tf.shape(x)[0];D=_tf.cond(A.sampling,lambda:_tf.exp(A.spread.sample(C)),lambda:_tf.expand_dims(_tf.exp(A.spread_mean),0));E=_tf.expand_dims(_tf.tanh(A.corr),0);B=_createCovMatrix(D,E,A._output_dim)
		if A._regularize:B=_r(B,A._regularize)
		A.matrix=B;return B
	def compute_output_shape(A,input_shape):return input_shape[0],A._output_dim,A._output_dim
	def get_config(A):B=super().get_config().copy();B.update({_B:A._output_dim,_C:A._regularize});return B