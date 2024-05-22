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
from..distributions import createMixDistBYmeanCovWeight as _c,regularizeCovMatrix as _r
import tensorflow as _tf,tensorflow_probability as _tfp
from tensorflow.keras.layers import Layer as _Layer
class Distribution(_Layer):
	def __init__(A,regularize_cov_epsilon=_B,**B):super(Distribution,A).__init__(**B);A._regularize_cov_epsilon=regularize_cov_epsilon
	def build(B,input_shapes):
		A=input_shapes
		if not(_A in A and _C in A and _D in A):raise Exception('means, covariances and weights are needed to construct the gaussian mixture distribution!')
		C=A[_A];B.mix_dim=C[1];B.output_dim=C[2];super(Distribution,B).build(A[_A])
	def call(A,x,**E):
		C=x[_A];B=x[_C];D=x[_D]
		if A._regularize_cov_epsilon:A.covMatrix=_r(B,A._regularize_cov_epsilon)
		else:A.covMatrix=B
		A.distribution=_tfp.layers.DistributionLambda(lambda t:_c(t[0],t[1],t[2],A.mix_dim,A.output_dim))([C,A.covMatrix,D]);return A.distribution
	def compute_output_shape(B,input_shape):A=input_shape;return A[0],A[1],B.output_dim
	def get_config(B):A=super().get_config().copy();A.update({'regularize_cov_epsilon':B._regularize_cov_epsilon});return A
class DistributionMean(_Layer):
	def __init__(A,**B):super(DistributionMean,A).__init__(**B)
	def call(A,x,**B):return x.mean()
class DistributionSampleLoss(_Layer):
	def __init__(A,**B):super(DistributionSampleLoss,A).__init__(**B);A.loss=_B
	def call(A,x,**D):B=x['dist'];C=x['samples'];A.loss=-_tf.reduce_mean(B.log_prob(C));A.add_loss(A.loss);return A.loss
class DistributionKLLoss(_Layer):
	def __init__(A,n_samples=100,symmetric=False,fix_na=True,**B):super(DistributionKLLoss,A).__init__(**B);A.n_samples=n_samples;A.loss=_B;A.ideal_dist=_B;A.samples=_B;A.kl_divergence=_B;A.symmetric=symmetric;A.fix_na=fix_na
	def build(B,input_shapes):
		A=input_shapes
		if not(_A in A and _C in A and _D in A):raise Exception('means, covariances and weights are needed to construct the ideal GMM!')
		C=A[_A];B.mix_dim=C[1];B.output_dim=C[2];super(DistributionKLLoss,B).build(A[_A])
	def call(A,x,**I):
		D=x['dist'];A.ideal_dist=_tfp.layers.DistributionLambda(lambda t:_c(t[0],t[1],t[2],A.mix_dim,A.output_dim))([x[_A],x[_C],x[_D]]);E=A.ideal_dist.sample(A.n_samples);A.samples_ideal=_tf.transpose(E,[1,0,2]);B=A.ideal_dist.log_prob(E)-D.log_prob(E)
		if A.fix_na:G=_tf.stop_gradient(_tf.reduce_max(_tf.where(_tf.math.is_nan(B),_tf.zeros_like(B),B)));B=_tf.where(_tf.math.is_nan(B),_tf.ones_like(B)*G,B)
		if A.symmetric:
			F=D.sample(A.n_samples);A.samples_pred=_tf.transpose(F,[1,0,2]);C=D.log_prob(F)-A.ideal_dist.log_prob(F)
			if A.fix_na:H=_tf.stop_gradient(_tf.reduce_max(_tf.where(_tf.math.is_nan(C),_tf.zeros_like(C),C)));C=_tf.where(_tf.math.is_nan(C),_tf.ones_like(C)*H,C)
			A.kl_divergence=_tf.reduce_mean(_tf.transpose(B,[1,0]),1)+_tf.reduce_mean(_tf.transpose(C,[1,0]),1)
		else:A.kl_divergence=_tf.reduce_mean(_tf.transpose(B,[1,0]),1)
		A.loss=A.kl_divergence;A.add_loss(A.loss);return A.loss
class DistributionSamples(_Layer):
	def __init__(A,n_samples,**B):A.n_samples=n_samples;super(DistributionSamples,A).__init__(**B)
	def call(A,x,**C):B=_tf.transpose(x.sample(A.n_samples),[1,2,0]);return B
	def get_config(B):A=super().get_config().copy();A.update({'n_samples':B.n_samples});return A