# I find out that when runing decode,
# t2t need to load all model before translate.
# It cause lots of time waiting.
# There are solution of t2t which require you to install
# some source code called server.
# For some reason, my laptop is really hard to 
# do that stuff.
# Then I try to build my own server for decoding
# which only need to keep loading model as process
# for each time translate and dont need to load again
# I find out t2t has the same similer mode called 
# interactive mode which can do that in terminal.
# But I need it to be wraped in python.
# So I try to modify and build my own server decode
# base on interactive mode of t2t but can be wraped in python
# I call it: tensorflow model non-server.
# I work with tensor2tensor 1.13.0 when creating this file

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# define prefix parameter:
data_dir = "colab/data"
Problem = "translate_envi_iwslt32k"
Model = "transformer"
hparams_set = "transformer_base"
output_dir = "colab/train"
decode_hparams = "beam_size=4,alpha=0.6"

import os
import collections
import operator
import re
import string
import time

from tensor2tensor.bin import t2t_trainer
from tensor2tensor.bin import t2t_decoder

import numpy as np
import six

from six.moves import input  # pylint: disable=redefined-builtin

# from tensor2tensor.bin import t2t_decoder
from tensor2tensor.data_generators import problem  # pylint: disable=unused-import
from tensor2tensor.data_generators import problem as problem_lib
from tensor2tensor.data_generators import text_encoder
from tensor2tensor.data_generators import text_problems

from tensor2tensor.utils import decoding
from tensor2tensor.utils import registry
from tensor2tensor.utils import trainer_lib
from tensor2tensor.utils import usr_dir
from tensor2tensor.utils import mlperf_log
from tensor2tensor.utils.hparam import HParams
from tensor2tensor.utils.decoding import make_input_fn_from_generator
from tensor2tensor.utils.decoding import _interactive_input_tensor_to_features_dict
from tensor2tensor.utils.decoding import _save_until_eos
import tensorflow as tf

flags = tf.flags
FLAGS = flags.FLAGS

FLAGS.output_dir = output_dir
FLAGS.data_dir = data_dir
FLAGS.hparams_set = hparams_set
FLAGS.problem = Problem
FLAGS.decode_hparams = decode_hparams
FLAGS.model = Model

create_hparams = t2t_decoder.create_hparams
create_decode_hparams = t2t_decoder.create_decode_hparams

# model decoder object: keeping model and decode message of user as fast as possible
class model_decoder():

  # building model when obj is created
  def __init__(self):

    tf.logging.set_verbosity(tf.logging.INFO)
    trainer_lib.set_random_seed(FLAGS.random_seed)
    usr_dir.import_usr_dir(FLAGS.t2t_usr_dir)

    # parameter to keep estimator prediction open
    self.close = False
    self.message = "Hello world"

    # store hparam and model and keep it alive during running time
    self.hp = create_hparams()
    self.decode_hp = create_decode_hparams()
    self.estimator = trainer_lib.create_estimator(FLAGS.model, 
                                              self.hp, 
                                              t2t_trainer.create_run_config(self.hp), 
                                              decode_hparams = self.decode_hp, 
                                              use_tpu = FLAGS.use_tpu)

    # we dont support TPU in here
    if self.estimator.config.use_tpu:
      raise ValueError("TPU is not support in here.")
    
    # loading model and set state to wait
    input_fn = lambda: self.input_fn(self.hp, self.decode_hp)
    self.predict = self.estimator.predict(input_fn, checkpoint_path = FLAGS.checkpoint_path)
    self.getMessage('hello world')
  
  def getMessage(self,Message):
    self.message = Message
    result = next(self.predict)
    targets_vocab = self.hp.problem_hparams.vocabulary["targets"]
    ouputMess = targets_vocab.decode(_save_until_eos(result["outputs"], False))
    tf.logging.info(ouputMess)
    return ouputMess
  
  def closeModel(self):
    self.close = True
    self.getMessage("hello world")

  def input_fn(self, hparams, decode_hp):
    gen_fn = make_input_fn_from_generator(
      self._takeValue_fn(hparams, decode_hp)
    )
    example = gen_fn()
    example = _interactive_input_tensor_to_features_dict(example,hparams)
    return example

  def _takeValue_fn(self, hparams, decode_hp):
    num_samples = decode_hp.num_samples if decode_hp.num_samples > 0 else 1
    decode_length = decode_hp.extra_length
    p_hparams = hparams.problem_hparams
    has_input = "inputs" in p_hparams.modality
    vocabulary = p_hparams.vocabulary["inputs" if has_input else "targets"]
    # This should be longer than the longest input.
    const_array_size = 10000
    while not self.close:
      # recieve messeage need to be translated
      input_string = self.message
      # translate message to end decode
      input_ids = vocabulary.encode(input_string)
      if has_input:
        input_ids.append(text_encoder.EOS_ID)
      x = [num_samples, decode_length, len(input_ids)] + input_ids
      assert len(x) < const_array_size
      x += [0] * (const_array_size - len(x))
      features = {"inputs": np.array(x).astype(np.int32),}
      for k, v in six.iteritems(
            problem_lib.problem_hparams_to_features(p_hparams)):
          features[k] = np.array(v).astype(np.int32)
      yield features





def main(_):
  obj = model_decoder()
  while True:
    message = input("enter text for testing [q = quit]:")
    if (message == 'q'):
      obj.closeModel()
      break
    print(obj.getMessage(message))
  # decode_model()

if __name__ == "__main__":
  tf.logging.set_verbosity(tf.logging.INFO)
  tf.app.run()