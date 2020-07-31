FROM docker.elastic.co/elasticsearch/elasticsearch:7.8.1
RUN elasticsearch-plugin install analysis-kuromoji
RUN elasticsearch-plugin install analysis-icu
COPY elasticsearch.yml /usr/share/elasticsearch/config/elasticsearch.yml
