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
model = "transformer"
hparams_set = "transformer_base"
output_dir = "colab/train"
decode_hparams = "beam_size=4,alpha=0.6"
message_dir = "colab/en.txt" # file where serving model will read translate needed message

import os
import collections
import operator
import re
import string
import time

from tensor2tensor.bin import t2t_trainer

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

flags.DEFINE_string("checkpoint_path", None,
                    "Path to the model checkpoint. Overrides output_dir.")
flags.DEFINE_integer("decode_shards", 1, "Number of decoding replicas.")
flags.DEFINE_bool("decode_in_memory", False, "Decode in memory.")

def create_hparams():
  
  return trainer_lib.create_hparams(
      hparams_set,
      FLAGS.hparams,
      data_dir=os.path.expanduser(data_dir),
      problem_name=Problem)

def create_decode_hparams():
  decode_hp = decoding.decode_hparams(decode_hparams)
  decode_hp.shards = FLAGS.decode_shards
  decode_hp.shard_id = FLAGS.worker_id
  decode_in_memory = FLAGS.decode_in_memory or decode_hp.decode_in_memory
  decode_hp.decode_in_memory = decode_in_memory
  decode_hp.decode_to_file = FLAGS.decode_to_file
  decode_hp.decode_reference = FLAGS.decode_reference
  return decode_hp


def decode(estimator, hparams, decode_hp):
  if estimator.config.use_tpu:
    raise ValueError("TPU can only decode from dataset.")
  usr_define_decode_from_file(estimator, hparams, decode_hp, checkpoint_path=FLAGS.checkpoint_path)


# function for real decoding of user define
def usr_define_decode_from_file(estimator, hparams, decode_hp, checkpoint_path=None):

  def _takeValueFromFile_input_fn(hparams, decode_hp):
    num_samples = decode_hp.num_samples if decode_hp.num_samples > 0 else 1
    decode_length = decode_hp.extra_length
    p_hparams = hparams.problem_hparams
    has_input = "inputs" in p_hparams.modality
    vocabulary = p_hparams.vocabulary["inputs" if has_input else "targets"]
    # This should be longer than the longest input.
    const_array_size = 10000

    # read file for translate
    input_string = ""
    while True:
      try:
        while True:
          file = open(message_dir,"r")
          check = file.readline()
          if (check == "true\n"):
            input_string = file.readline()
            file.close()
            break
          elif (check == "false\n"):
            file.close()
            return
          file.close()
          print("checking code running: ",check)
          time.sleep(2)
      except Exception:
        pass

      input_ids = vocabulary.encode(input_string)
      if has_input:
        input_ids.append(text_encoder.EOS_ID)
      x = [num_samples, decode_length, len(input_ids)] + input_ids
      assert len(x) < const_array_size
      x += [0] * (const_array_size - len(x))
      features = {
          "inputs": np.array(x).astype(np.int32),
      }

      for k, v in six.iteritems(
            problem_lib.problem_hparams_to_features(p_hparams)):
          features[k] = np.array(v).astype(np.int32)
      yield features

  is_image = "image" in hparams.problem.name
  is_text2class = isinstance(hparams.problem,
                             text_problems.Text2ClassProblem)
  skip_eos_postprocess = (
      is_image or is_text2class or decode_hp.skip_eos_postprocess)


  def input_fn():
    gen_fn = make_input_fn_from_generator(
      _takeValueFromFile_input_fn(hparams,decode_hp))
    example = gen_fn()
    example = example = _interactive_input_tensor_to_features_dict(example, hparams)
    return example

  result_iter = estimator.predict(input_fn, checkpoint_path=checkpoint_path)
  for result in result_iter:
    targets_vocab = hparams.problem_hparams.vocabulary["targets"]
    if decode_hp.identity_output:
      tf.logging.info(" ".join(map(str, result["outputs"].flatten())))
    else:
      translated_word = targets_vocab.decode(_save_until_eos(result["outputs"], skip_eos_postprocess))
      tf.logging.info(translated_word)
      print("can be pass out: ",translated_word)



def main(_):
  tf.logging.set_verbosity(tf.logging.INFO)
  trainer_lib.set_random_seed(FLAGS.random_seed)
  usr_dir.import_usr_dir(FLAGS.t2t_usr_dir)

  hp = create_hparams()
  decode_hp = create_decode_hparams()
  
  estimator = trainer_lib.create_estimator(
    model,
    hp,
    t2t_trainer.create_run_config(hp),
    decode_hparams=decode_hp,
    use_tpu=FLAGS.use_tpu)
  
  usr_define_decode_from_file(estimator, hp, decode_hp)

if __name__ == "__main__":
  tf.logging.set_verbosity(tf.logging.INFO)
  tf.app.run()