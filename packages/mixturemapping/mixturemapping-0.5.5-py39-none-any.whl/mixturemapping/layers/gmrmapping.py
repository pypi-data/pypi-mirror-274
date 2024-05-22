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
_C='means'
_B=False
_A=True
from._mapping import _M
import numpy as _np,tensorflow as _tf,tensorflow_probability as _tfp
_tfd=_tfp.distributions
from..distributions import regularizeCovMatrix as _r
class DynamicGMR(_M):
	def __init__(A,output_dim,input_dim,mix_size,n_components=None,regularize_cov_epsilon=.95,inv_rcond=1e-05,**C):super(DynamicGMR,A).__init__(output_dim,**C);A.mix_size=mix_size;A.input_dim=input_dim;A.var_size=A.output_dim+A.input_dim;A.output_indices=list(range(A.input_dim,A.var_size));A._r=regularize_cov_epsilon;A._rcond=inv_rcond;B=_np.ones(A.var_size,dtype=bool);B[A.output_indices]=_B;B,=_np.where(B);A.input_indices=B;A.n_components=n_components;A.corr_size=int(A.var_size*(A.var_size-1)/2)
	def _to_np(A,a):
		if isinstance(a,_np.ndarray):return a
		else:return _np.array(a,dtype=A.dtype)
	def set_gmm_values(A,means,covariances,weights):E=covariances;D=means;B=_np.array([_np.sqrt(_np.diagonal(A))for A in E]);C=E/_np.reshape(B,[A.mix_size,1,A.var_size])/_np.reshape(B,[A.mix_size,A.var_size,1]);F=_np.triu_indices(A.var_size,1);C=C[:,F[0],F[1]];_tf.keras.backend.set_value(A.model_cov_stddev_i,_np.log(B)[:,A.input_indices]);_tf.keras.backend.set_value(A.model_cov_stddev_o,_np.log(B)[:,A.output_indices]);_tf.keras.backend.set_value(A.model_cov_stddev_o_spread,_np.ones((A.mix_size,A.output_dim))*-2.);_tf.keras.backend.set_value(A.model_m_i,D[:,A.input_indices]);_tf.keras.backend.set_value(A.model_m_o,D[:,A.output_indices]);_tf.keras.backend.set_value(A.model_cov_corr,_np.arctanh(C));_tf.keras.backend.set_value(A.model_w,weights)
	def fit_gmms(B,np_inputs,tf_inputs,input_gmm,output_gmm,n_samples=10):C=n_samples;from sklearn.mixture import GaussianMixture as H;from.distribution import Distribution as D,DistributionSamples as E;I=D()(input_gmm);J=E(C)(I);K=D()(output_gmm);L=E(C)(K);M=_tf.reshape(_tf.transpose(_tf.concat([J,L],axis=1),[0,2,1]),[-1,B.var_size]);F=_tf.keras.Model(inputs=tf_inputs,outputs=M);F.compile();G=F.predict(np_inputs);A=H(n_components=B.mix_size);N=G[~_np.isnan(G).any(axis=1)];A.fit(N);B.set_gmm_values(means=A.means_,covariances=A.covariances_,weights=A.weights_)
	def build(A,input_shapes):
		C=input_shapes;B='uniform'
		if not(_C in C and _D in C):raise Exception('means and weights are needed to construct the mapping layer!')
		A.model_m_i=A.add_weight(name='mean_var_i',shape=(A.mix_size,A.input_dim),initializer=B,trainable=_B);A.model_cov_stddev_i=A.add_weight(name='cov_stddev_var_i',shape=(A.mix_size,A.input_dim),initializer=B,trainable=_A);A.model_m_o=A.add_weight(name='mean_var_o',shape=(A.mix_size,A.output_dim),initializer=B,trainable=_A);A.model_cov_stddev_o=A.add_weight(name='cov_stddev_var_o',shape=(A.mix_size,A.output_dim),initializer=B,trainable=_A);A.model_cov_stddev_o_spread=A.add_weight(name='cov_stddev_var_o_delta',shape=(A.mix_size,A.output_dim),initializer=B,trainable=_A);A.model_cov_corr=A.add_weight(name='cov_corr_var',shape=(A.mix_size,A.corr_size),initializer=B,trainable=_A);A.model_w=A.add_weight(name='weight_var',shape=(A.mix_size,),initializer=B,trainable=_B)
	@_tf.function(autograph=_B)
	def call(self,x,**p):
		b='baseCovMatrix';a='rowVec';Z='colVec';Y='covariances';A=self;M=x[_C];c=x[Y];d=x[_D];D=_tf.shape(M)[0];H=_tf.concat([A.model_m_i,A.model_m_o],axis=-1)
		def e():B=_tf.concat([A.model_cov_stddev_i,A.model_cov_stddev_o],axis=-1);B=_tf.exp(B);return _tf.tile(_tf.expand_dims(_tf.matmul(_tf.reshape(B,[A.mix_size,A.var_size,1],name=Z),_tf.reshape(B,[A.mix_size,1,A.var_size],name=a),name=b),0),[D,1,1,1])
		def f():C=_tfd.Normal(A.model_cov_stddev_o,_tf.exp(A.model_cov_stddev_o_spread)).sample(D);E=_tf.tile(_tf.expand_dims(A.model_cov_stddev_i,0),[D,1,1]);B=_tf.concat([E,C],axis=-1);B=_tf.exp(B);return _tf.matmul(_tf.reshape(B,[D,A.mix_size,A.var_size,1],name=Z),_tf.reshape(B,[D,A.mix_size,1,A.var_size],name=a),name=b)
		N=_tf.cond(A.sampling,f,e);S=_tf.expand_dims(_tf.tanh(A.model_cov_corr),0);O=A.var_size-1;I=[-1]
		for q in range(A.var_size-1):O=O-1;I.append(I[-1]+O)
		with _tf.name_scope('TransposedCorrelation'):g=[[N[:,:,A,B]if A==B else N[:,:,A,B]*S[:,:,B+I[A]]if A<B else N[:,:,A,B]*S[:,:,A+I[B]]for A in range(A.var_size)]for B in range(A.var_size)]
		B=_tf.transpose(g,[2,3,0,1],name='TransposeBack');H=_tf.expand_dims(_tf.expand_dims(H,0),2);h=_tf.expand_dims(_tf.expand_dims(A.model_w,0),2);B=_tf.expand_dims(B,2)
		if A._r:B=_r(B,A._r)
		T=_tf.stop_gradient(_tf.gather(_tf.gather(B,A.input_indices,axis=3),A.input_indices,axis=4));i=_tf.gather(_tf.gather(B,A.output_indices,axis=3),A.output_indices,axis=4);J=_tf.linalg.pinv(T,A._rcond);K=_tf.gather(_tf.gather(B,A.output_indices,axis=3),A.input_indices,axis=4);U=_tf.linalg.matrix_transpose(K);V=_tf.gather(H,A.input_indices,axis=3);j=_tf.gather(H,A.output_indices,axis=3);k=_tfd.MultivariateNormalTriL(loc=V,scale_tril=_tf.linalg.cholesky(T));W=_tf.shape(M);P=W[0];L=W[1];X=_tf.expand_dims(M,1);l=_tf.expand_dims(c,1);m=_tf.expand_dims(d,1);E=j+_tf.linalg.matmul(_tf.linalg.matmul(K,J),_tf.expand_dims(X-V,4))[:,:,:,:,0];n=_tf.linalg.matmul(_tf.linalg.matmul(_tf.linalg.matmul(_tf.linalg.matmul(K,J),l),J),U);F=i-_tf.matmul(_tf.matmul(K,J),U)+n;G=h*k.prob(X);Q=_tf.reduce_sum(G,axis=1,keepdims=_A);G=G/Q;G*=m;E=_tf.reshape(E,shape=[P,L*A.mix_size,A.output_dim]);F=_tf.reshape(F,shape=[P,L*A.mix_size,A.output_dim,A.output_dim]);C=_tf.reshape(G,shape=[P,L*A.mix_size])
		if A.n_components:o=_tf.minimum(A.n_components,L*A.mix_size);R=_tf.math.top_k(C,k=o);C=R.values;Q=_tf.reduce_sum(C,axis=1,keepdims=_A);C=C/Q;E=_tf.gather(E,R.indices,axis=1,batch_dims=1);F=_tf.gather(F,R.indices,axis=1,batch_dims=1)
		return{_C:E,Y:F,_D:C}
	def get_config(A):B=super().get_config().copy();B.update({'output_dim':A.output_dim,'input_dim':A.input_dim,'mix_size':A.mix_size,'n_components  ':A.n_components,'regularize_cov_epsilon':A._r,'inv_rcond':A._rcond});return B