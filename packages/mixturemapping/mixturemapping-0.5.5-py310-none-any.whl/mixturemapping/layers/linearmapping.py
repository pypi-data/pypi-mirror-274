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

_B='weights'
_A='means'
import tensorflow as _tf,tensorflow_probability as _tfp
_tfd=_tfp.distributions
from._mapping import _M
from..distributions import regularizeCovMatrix as _r
class LinearMapping(_M):
	def build(A,input_shapes):
		D=True;C='normal';B=input_shapes
		if not(_A in B and _B in B):raise Exception('means and weights are needed to construct the mapping layer!')
		A.mix_dim=B[_A][1];A.input_dim=B[_A][2];A.kernel_mean=A.add_weight(name='kernel_mean',shape=(A.input_dim,A.output_dim),initializer=C,trainable=D);A.kernel_std=A.add_weight(name='kernel_std',shape=(A.input_dim,A.output_dim),initializer=C,trainable=D);A.bias_mean=A.add_weight(name='bias_mean',shape=(A.output_dim,),initializer=C,trainable=D);A.bias_std=A.add_weight(name='bias_std',shape=(A.output_dim,),initializer=C,trainable=D);A.kernel=_tfd.Normal(A.kernel_mean,_tf.exp(A.kernel_std));A.bias=_tfd.Normal(A.bias_mean,_tf.exp(A.bias_std));super(LinearMapping,A).build(B[_A])
	@_tf.function(autograph=False)
	def call(self,x,**M):
		I='covariances';H='stdDevs';D='covB';C='covA';A=self;F=_tf.shape(x[_A])[0];J=_tf.cond(A.sampling,lambda:_tf.matmul(x[_A],A.kernel.sample(F))+_tf.expand_dims(A.bias.sample(F),1),lambda:_tf.matmul(x[_A],A.kernel_mean)+A.bias_mean);G=_tf.expand_dims(_tf.expand_dims(_tf.stop_gradient(A.kernel_mean),0),0)
		if H in x:K=_tf.transpose(_tf.expand_dims(x[H],2),[0,1,3,2]);E=_tf.multiply(K,G)
		else:L=_tf.linalg.sqrtm(x[I]);E=_tf.matmul(L,G)
		A.mappingCov=_tf.matmul(_tf.transpose(E,[0,1,3,2]),E);B=A.mappingCov
		if C in x:
			if len(x[C].shape.dims)==3:B=B+_tf.expand_dims(x[C],1)
			else:B=B+x[C]
		if D in x:
			if len(x[D].shape.dims)==3:B=B+_tf.expand_dims(x[D],1)
			else:B=B+x[D]
		if A._regularize_cov_epsilon:A.covMatrix=_r(B,A._regularize_cov_epsilon)
		else:A.covMatrix=B
		return{_A:J,I:A.covMatrix,_B:x[_B]}