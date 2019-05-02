t2t-decoder \
  --data_dir=colab/data \
  --problem=translate_envi_iwslt32k \
  --model=transformer \
  --hparams_set=transformer_base \
  --output_dir=colab/train \
  --decode_hparams="beam_size=4,alpha=0.6" \
  --decode_interactive
