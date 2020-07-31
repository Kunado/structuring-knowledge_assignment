from elasticsearch import Elasticsearch
import pandas
import fasttext

index_name = 'structuring_knowledge'
es = Elasticsearch([{'host': 'localhost', 'port': 9200}], timeout=30)

es.indices.delete(index_name)
es.indices.create(index_name, body={
  "settings": {
    "analysis": {
      "analyzer": {
        "ngram_analyzer": {
          "tokenizer": "my_ngram_tokenizer",
           "char_filter": [
            "nfkc_normalizer"
          ]
        },
        "morph_analyzer": {
          "tokenizer": "kuromoji_tokenizer",
           "char_filter": [
            "nfkc_normalizer"
          ]
        }
      },
      "tokenizer": {
        "my_ngram_tokenizer": {
          "type": "ngram",
          "min_gram": 2,
          "max_gram": 2,
          "token_chars": ["letter", "digit"]
        },
        "kuromoji_tokenizer": {
          "type": "kuromoji_tokenizer",
          "mode": "extended"
        }
      },
      "char_filter": {
        "nfkc_normalizer": {
          "type": "icu_normalizer"
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "id": { "type": "keyword" },
      "title": {
        "type": "text",
        "analyzer": "ngram_analyzer",
        "copy_to": ["keywords","keywords_morph"]
      },
      "index": {
        "type": "text",
        "analyzer": "ngram_analyzer",
        "copy_to": ["keywords","keywords_morph"]
      },
      "responsibility": {
        "type": "keyword",
        "copy_to": ["keywords","keywords_morph"]
      },
       "publsihed": {
        "type": "keyword"
      },
      "publisher": {
        "type": "keyword",
        "copy_to": ["keywords","keywords_morph"]
      },
      "ndc": {
        "type": "keyword"
      },
      "keywords": {
        "type": "text",
        "analyzer": "ngram_analyzer"
      },
       "keywords_morph": {
        "type": "text",
        "analyzer": "morph_analyzer"
      }
    }
  }
})

df = pandas.read_table('data/index.tsv.gz', dtype=str, keep_default_na=False, header=0)

body = []
for index, row in df.iterrows():
  body.append({ "index" : {"_id" : row["id"] } })
  body.append( row.to_dict() )
  if(len(body)==200):
    print("flush", index)
    es.bulk(index=index_name, body=body)
    body = []
es.bulk(index=index_name, body=body)

model = fasttext.FastText.load_model('data/model_ndc3.bin')
