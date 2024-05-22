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
from..distributions import regularizeCovMatrix as _r
from._mapping import _M
import tensorflow as _tf,tensorflow_probability as _tfp
_tfd=_tfp.distributions
class GeneralMapping(_M):
	def __init__(A,*B,yModel=None,yDeltaModel=None,**C):super(GeneralMapping,A).__init__(*B,**C);A.yModel=yModel;A.yDeltaModel=yDeltaModel
	def build(A,input_shapes):
		B=input_shapes
		if not(_A in B and _B in B):raise Exception('means,  weights are needed to construct the mapping layer!')
		A.mix_dim=B[_A][1];A.input_dim=B[_A][2];super(GeneralMapping,A).build(B[_A]);A.yModel.build(B[_A])
		for C in A.yModel.trainable_variables:A._trainable_weights.append(C)
		if A.yDeltaModel:
			A.yDeltaModel.build(B[_A])
			for C in A.yDeltaModel.trainable_variables:A._trainable_weights.append(C)
	@_tf.function(autograph=False)
	def call(self,x,**S):
		L='covariances';H='stdDevs';E='covB';D='covA';A=self;T=_tf.shape(x[_A])[0]
		with _tf.GradientTape(persistent=True)as I:
			J=x[_A];F=[J[:,:,A]for A in range(A.input_dim)]
			for M in F:I.watch(M)
			N=_tf.stack(F,2);C=A.yModel(N);O=[C[:,:,A]for A in range(A.output_dim)]
		A.jacobian=_tf.stack([_tf.stack([I.gradient(O[B],F[A])for A in range(A.input_dim)],2)for B in range(A.output_dim)],3,name='jacobian')
		if A.yDeltaModel:P=A.yDeltaModel(J);A.mean_dist=_tfd.Normal(C,_tf.exp(P));K=_tf.cond(A.sampling,lambda:A.mean_dist.sample(),lambda:C)
		else:K=C
		if H in x:assert x[H].shape.ndims==3;Q=_tf.expand_dims(x[H],3);G=_tf.multiply(Q,_tf.stop_gradient(A.jacobian))
		else:R=_tf.linalg.sqrtm(x[L]);G=_tf.matmul(R,_tf.stop_gradient(A.jacobian))
		A.mappingCov=_tf.matmul(_tf.transpose(G,[0,1,3,2]),G);B=A.mappingCov
		if D in x:
			if len(x[D].shape.dims)==3:B=B+_tf.expand_dims(x[D],1)
			else:B=B+x[D]
		if E in x:
			if len(x[E].shape.dims)==3:B=B+_tf.expand_dims(x[E],1)
			else:B=B+x[E]
		if A._regularize_cov_epsilon:A.covMatrix=_r(B,A._regularize_cov_epsilon)
		else:A.covMatrix=B
		return{_A:K,L:A.covMatrix,_B:x[_B]}
	def get_config(A):
		B=super().get_config().copy();B.update({'yModel':A.yModel.get_config()})
		if A.yDeltaModel:B.update({'yDeltaModel':A.yDeltaModel.get_config()})
		return B