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

_E='MixtureSameFamily'
_D='Weights'
_C='MultiTriL'
_B='CombinedDist'
_A='GaussianMixture'
import tensorflow as _tf,tensorflow_probability as _tfp
_tfd=_tfp.distributions
def createCovMatrix(stdDevTensor,correlationTensor,size,name='CorrelationMatrix'):
	I='AddCorrelation';B=stdDevTensor;E=correlationTensor;A=size
	with _tf.name_scope(name):
		G=_tf.shape(B)[0];F=A-1;C=[-1]
		for J in range(A-1):F=F-1;C.append(C[-1]+F)
		D=_tf.matmul(_tf.reshape(B,[G,A,1],name='colVec'),_tf.reshape(B,[G,1,A],name='rowVec'),name='CovMatrix')
		if _tf.shape(E).shape[0]==1:
			with _tf.name_scope(I):H=[[D[:,A,B]if A==B else D[:,A,B]*E[B+C[A]]if A<B else D[:,A,B]*E[A+C[B]]for A in range(A)]for B in range(A)]
		else:
			with _tf.name_scope(I):H=[[D[:,A,B]if A==B else D[:,A,B]*E[:,B+C[A]]if A<B else D[:,A,B]*E[:,A+C[B]]for A in range(A)]for B in range(A)]
		return _tf.transpose(H,name=name+'Transpose')
def regularizeCovMatrix(covMatrix,epsilon=.999):B=epsilon;A=covMatrix;C=_tf.sqrt(_tf.linalg.diag_part(A));D=_tf.expand_dims(C,-1);E=D*_tf.linalg.matrix_transpose(D);F=_tf.clip_by_value(_tf.divide(A,E),-B,B);G=_tf.linalg.set_diag(F,_tf.ones_like(C));return _tf.multiply(G,E)
def createMixDistBYmeanCovWeight(meanTensor,covTensor,weightTensor,mixSize,matrixSize,name=_A):
	with _tf.name_scope(name):
		with _tf.name_scope(_B):A=_tf.linalg.cholesky(covTensor);B=_tfd.MultivariateNormalTriL(loc=meanTensor,scale_tril=A,name=_C);C=_tfd.Categorical(probs=weightTensor,name=_D);D=_tfp.distributions.MixtureSameFamily(mixture_distribution=C,components_distribution=B,name=_E)
		return D
def createMixDistribution(meanTensor,stdDevTensor,correlationTensor,weightTensor,mixSize,matrixSize,name=_A):
	C=meanTensor;A=matrixSize
	with _tf.name_scope(name):
		D=_tf.shape(C)[0];E=[];F=[]
		with _tf.name_scope('SeparateDists'):
			for B in range(mixSize):
				with _tf.name_scope('Part_'+str(B+1)):G=C[:,B];H=stdDevTensor[:,B];I=correlationTensor[:,B];J=createCovMatrix(H,I,A);K=_tf.linalg.cholesky(J);E.append(_tf.reshape(G,[D,1,A],name='Center'));F.append(_tf.reshape(K,[D,1,A,A],name='Scale'))
		with _tf.name_scope(_B):L=_tf.concat(E,1,name='Centers');M=_tf.concat(F,1,name='Scales');N=_tfd.MultivariateNormalTriL(loc=L,scale_tril=M,name=_C);O=_tfd.Categorical(probs=weightTensor,name=_D);P=_tfp.distributions.MixtureSameFamily(mixture_distribution=O,components_distribution=N,name=_E)
		return P