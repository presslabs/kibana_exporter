from kibana_exporter import DataReader
from elasticsearch import Elasticsearch
from pprint import pprint


def test_index_names():
    DataReader(Elasticsearch(['localhost:9300']), '*logstash*').index_names()

def test_get_documents():
    ret = DataReader(Elasticsearch(['localhost:9300']), '*logstash*').get_documents(
        '2017-01-19-00', '2017-01-19-01')
    for doc in ret:
        # print(doc)
        pass
