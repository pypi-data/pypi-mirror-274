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

_J='bias_std'
_I='bias_mean'
_H='cat'
_G='vocabulary'
_F=False
_E=True
_D='normal'
_C='weights'
_B='covariances'
_A='means'
import tensorflow as _tf,tensorflow_probability as _tfp
_tfd=_tfp.distributions
_MA=_tf.linalg.LinearOperatorFullMatrix
_BM=_tf.linalg.LinearOperatorBlockDiag
import numpy as _np
from._mapping import _M
class AppendCatAsFloat(_tf.keras.layers.Layer):
	def __init__(A,vocabulary,**C):
		B=vocabulary;super(AppendCatAsFloat,A).__init__(**C)
		if isinstance(B,_np.ndarray):A.vocabulary=B.tolist()
		else:A.vocabulary=B
	def build(A,input_shapes):A.lookupLayer=_tf.keras.layers.StringLookup(vocabulary=A.vocabulary);A.output_dim=input_shapes[_A][-1]
	def compute_output_shape(B,input_shape):A=input_shape;return{_A:(A[_A][0],A[_A][1],B.output_dim+1),_B:(A[_A][0],A[_A][1],B.output_dim+1,B.output_dim+1),_C:(A[_A][0],A[_A][1])}
	def get_config(B):A=super().get_config().copy();A.update({_G:B.vocabulary});return A
	@_tf.function(autograph=_F)
	def call(self,x,**E):A=self.lookupLayer(x[_H]);A=_tf.cast(A,x[_A].dtype);A=_tf.expand_dims(_tf.tile(_tf.expand_dims(A,1),[1,_tf.shape(x[_A])[1]]),2);B=_tf.concat([x[_A],A],2);C=_tf.constant([[[[.01]]]]);D=_BM([_MA(x[_B]),_MA(C)]).to_dense();return{_A:B,_B:D,_C:x[_C]}
class DistMerger(_tf.keras.layers.Layer):
	def __init__(A,**B):super(DistMerger,A).__init__(**B)
	def build(A,input_shapes):B=input_shapes;A.mix_dim_A=B['A'][_A][-2];A.mix_dim_B=B['B'][_A][-2];A.mix_dim=A.mix_dim_A*A.mix_dim_B;A.output_dim_A=B['A'][_A][-1];A.output_dim_B=B['B'][_A][-1];A.output_dim=A.output_dim_A+A.output_dim_B
	def compute_output_shape(A,input_shape):B=input_shape;return{_A:(B[_A][0],A.mix_dim,A.output_dim),_B:(B[_A][0],A.mix_dim,A.output_dim,A.output_dim),_C:(B[_A][0],A.mix_dim)}
	@_tf.function(autograph=_F)
	def call(self,x,**P):A=self;B=x['A'];C=x['B'];D=_tf.shape(B[_A])[0];E=_tf.tile(_tf.expand_dims(B[_A],1),[1,A.mix_dim_A,1,1]);F=_tf.tile(_tf.expand_dims(B[_B],1),[1,A.mix_dim_A,1,1,1]);G=_tf.tile(_tf.expand_dims(B[_C],1),[1,A.mix_dim_A,1]);H=_tf.tile(_tf.expand_dims(C[_A],2),[1,1,A.mix_dim_B,1]);I=_tf.tile(_tf.expand_dims(C[_B],2),[1,1,A.mix_dim_B,1,1]);J=_tf.tile(_tf.expand_dims(C[_C],2),[1,1,A.mix_dim_B]);K=_tf.concat([E,H],axis=3);L=_tf.reshape(K,[D,A.mix_dim,A.output_dim]);M=_BM([_MA(F),_MA(I)]);N=_tf.reshape(M.to_dense(),[D,A.mix_dim,A.output_dim,A.output_dim]);O=_tf.reshape(G*J,[D,A.mix_dim]);return{_A:L,_B:N,_C:O}
class CatTrainableScale(_M):
	def __init__(A,vocabulary,**C):
		B=vocabulary;super(CatTrainableScale,A).__init__(**C)
		if isinstance(B,_np.ndarray):A.vocabulary=B.tolist()
		else:A.vocabulary=B
		A.vocabulary_len=len(A.vocabulary)
	def build(A,input_shapes):B=input_shapes;A.lookupLayer=_tf.keras.layers.StringLookup(vocabulary=A.vocabulary);A.output_dim=B[_A][-1];A.mix_dim=B[_A][1];A.input_dim=B[_A][2];A.kernel_mean=A.add_weight(name='kernel_mean',shape=(A.vocabulary_len,A.output_dim),initializer=_D,trainable=_E);A.kernel_std=A.add_weight(name='kernel_std',shape=(A.vocabulary_len,A.output_dim),initializer=_D,trainable=_E);A.bias_mean=A.add_weight(name=_I,shape=(A.vocabulary_len,A.output_dim),initializer=_D,trainable=_E);A.bias_std=A.add_weight(name=_J,shape=(A.vocabulary_len,A.output_dim),initializer=_D,trainable=_E);A.kernel=_tfd.Normal(A.kernel_mean,_tf.exp(A.kernel_std));A.bias=_tfd.Normal(A.bias_mean,_tf.exp(A.bias_std));super(CatTrainableScale,A).build(B[_A])
	def compute_output_shape(B,input_shape):A=input_shape;return{_A:(A[_A][0],A[_A][1],B.output_dim),_B:(A[_A][0],A[_A][1],B.output_dim,B.output_dim),_C:(A[_A][0],A[_A][1])}
	def get_config(B):A=super().get_config().copy();A.update({_G:B.vocabulary});return A
	@_tf.function(autograph=_F)
	def call(self,x,**H):A=self;E=_tf.shape(x[_A])[0];B=A.lookupLayer(x[_H]);B=_tf.expand_dims(_tf.one_hot(B,A.vocabulary_len),2);C=_tf.cond(A.sampling,lambda:_tf.reduce_sum(B*A.kernel.sample(E),1),lambda:_tf.reduce_sum(B*A.kernel_mean,1));D=_tf.cond(A.sampling,lambda:_tf.reduce_sum(B*A.bias.sample(E),1),lambda:_tf.reduce_sum(B*A.bias_mean,1));C=_tf.expand_dims(_tf.exp(C),1);D=_tf.expand_dims(D,1);F=x[_A]*C+D;G=x[_B]*_tf.expand_dims(C,-1)*_tf.expand_dims(C,-2);return{_A:F,_B:G,_C:x[_C]}
class CatTrainableOffset(_M):
	def __init__(A,vocabulary,**C):
		B=vocabulary;super(CatTrainableOffset,A).__init__(**C)
		if isinstance(B,_np.ndarray):A.vocabulary=B.tolist()
		else:A.vocabulary=B
		A.vocabulary_len=len(A.vocabulary)
	def build(A,input_shapes):B=input_shapes;A.lookupLayer=_tf.keras.layers.StringLookup(vocabulary=A.vocabulary);A.output_dim=B[_A][-1];A.mix_dim=B[_A][1];A.input_dim=B[_A][2];A.bias_mean=A.add_weight(name=_I,shape=(A.vocabulary_len,A.output_dim),initializer=_D,trainable=_E);A.bias_std=A.add_weight(name=_J,shape=(A.vocabulary_len,A.output_dim),initializer=_D,trainable=_E);A.bias=_tfd.Normal(A.bias_mean,_tf.exp(A.bias_std));super(CatTrainableOffset,A).build(B[_A])
	def compute_output_shape(B,input_shape):A=input_shape;return{_A:(A[_A][0],A[_A][1],B.output_dim),_B:(A[_A][0],A[_A][1],B.output_dim,B.output_dim),_C:(A[_A][0],A[_A][1])}
	def get_config(B):A=super().get_config().copy();A.update({_G:B.vocabulary});return A
	@_tf.function(autograph=_F)
	def call(self,x,**F):A=self;D=_tf.shape(x[_A])[0];B=A.lookupLayer(x[_H]);B=_tf.expand_dims(_tf.one_hot(B,A.vocabulary_len),2);C=_tf.cond(A.sampling,lambda:_tf.reduce_sum(B*A.bias.sample(D),1),lambda:_tf.reduce_sum(B*A.bias_mean,1));C=_tf.expand_dims(C,1);E=x[_A]+C;return{_A:E,_B:x[_B],_C:x[_C]}