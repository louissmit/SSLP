

## What train-model.perl does:
# (1) prepare corpus
# (2) run GIZA
# (3) align words
# (4) learn lexical translation
# (5) extract phrases
# (6) score phrases
# (7) learn reordering model
# (8) learn generation model
# (9) create decoder config file

### BASELINE
# http://www.statmt.org/moses/?n=Moses.Baseline

# From tips:
LM="-lm 0:3:/home/bart/project2_data/lm/europarl-v7.nl-en.train.blm.en:8"
MGIZA="-external-bin-dir /apps/smt_tools/alignment/mgizapp-0.7.3/manual-compile -mgiza -mgiza-cpus 4"

# Should comtain all dirs (training, dev, test)
# DATASET=/home/bart/project2_data
DATASET=~/p2test


## Training
# Assume clean corpus (tokenized and all)
CORPUS=$DATASET/training/p2_training #path to both

~/mosesdecoder/scripts/training/train-model.perl -root-dir train \
 $LM $MGIZA \
 -corpus $CORPUS \
 -f en -e nl -alignment grow-diag-final-and -reordering msd-bidirectional-fe \
 &> training.out &
 
## Tuning
DEV=$DATASET/dev/p2_dev

~/mosesdecoder/scripts/training/mert-moses.pl \
  $DEV.en $DEV.nl \
  ~/mosesdecoder/bin/moses train/model/moses.ini --mertdir ~/mosesdecoder/bin/ \
  --decoder-flags="-threads 4" &> mert.out &

## Testing
TEST=$DATASET/test/p2_test

~/mosesdecoder/bin/moses \
   -f train/model/moses.ini \
   < $TEST.en \
   > translated.en \
   2> translating.out 
~/mosesdecoder/scripts/generic/multi-bleu.perl \
   -lc $TEST.nl \
   < translated.en


