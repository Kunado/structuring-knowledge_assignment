#!/bin/bash

if [ ! -e ./data ]; then
  mkdir ./data
fi

curl -L -o data/index.tsv.gz https://github.com/vopaldragon/knstr/raw/master/index.tsv.gz
curl -L -o data/ndc.tsv.gz https://github.com/vopaldragon/knstr/raw/master/ndc.tsv.gz
curl -L -o data/wakati.tsv.gz https://github.com/vopaldragon/knstr/raw/master/wakati.tsv.gz

curl -L -o data/model_ndc3.bin.gz https://lab.ndl.go.jp/ndc/model/model_ndc3.bin.gz
gzip -d -c data/model_ndc3.bin.gz > data/model_ndc3.bin
