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

from tensorflow.keras.layers import Layer as _Layer
import tensorflow as _tf
class _M(_Layer):
	def __init__(A,output_dim,regularize_cov_epsilon=None,**B):super(_M,A).__init__(**B);A.output_dim=output_dim;A._regularize_cov_epsilon=regularize_cov_epsilon;A.sampling=_tf.Variable(True,trainable=False,name='sampling')
	def sampling_ON(A):_tf.keras.backend.eval(A.sampling.assign(True))
	def sampling_OFF(A):_tf.keras.backend.eval(A.sampling.assign(False))
	def compute_output_shape(C,input_shape):B=input_shape;A='means';return{A:(B[A][0],B[A][1],C.output_dim),'covariances':(B[A][0],B[A][1],C.output_dim,C.output_dim),'weights':(B[A][0],B[A][1])}
	def get_config(B):A=super().get_config().copy();A.update({'regularize_cov_epsilon':B._regularize_cov_epsilon});return A