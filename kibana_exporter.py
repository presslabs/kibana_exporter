from __future__ import print_function

import argparse
import sys

from elasticsearch import Elasticsearch
import json


GUARD = object()


def slice_indices(indices, start, end):
    s_index = 0
    e_index = len(indices)
    if start is not None:
        for i, name in enumerate(indices):
            # print('>', name)
            if start in name:
                s_index = i
                break
        else:
            raise AssertionError('failed to find start index')
    if end is not None:
        for i, name in enumerate(reversed(indices)):
            # print('<', name)
            if end in name:
                e_index = len(indices) - i
                break
        else:
            raise AssertionError('failed to find end index')
    return indices[s_index:e_index]


class DataReader(object):
    def __init__(self, client, index_patterns=""):
        self._client = client
        self._index_patterns = index_patterns
        self._cache = {}

    def index_names(self):
        names = self._cache.get('index_names', GUARD)
        if names is GUARD:
            names = self._client.indices.get(index=[self._index_patterns]).keys()
            self._cache['index_names'] = names
        return sorted(names)

    def get_documents(self, start=None, end=None, query=None):
        if query is None:
            query = {'match_all': {}}
        indices = self.index_names()
        # print(" ".join(indices))
        indices = slice_indices(indices, start, end)
        last = None
        done = False
        for name in indices:
            while not done:
                sys.stderr.write('fetching {} {}\n'.format(name, last))
                body = {
                    'query': query,
                    'sort': [
                        {'time': 'asc'},
                        {'request_id': 'asc'},
                    ],
                    'size': 1000,
                }
                if last is not None:
                    body['search_after'] = last
                results = self._client.search(
                    body=body,
                    index=name,
                )['hits']['hits']
                for doc in results:
                    yield doc['_source']
                    last = doc['sort']
                done = (len(results) == 0)


def parse_args():
    parser = argparse.ArgumentParser(
        description='Export logs from kibana',
    )
    # parser.add_argument('outfile', help='filename to output to')
    parser.add_argument('--instance', help='only extract logs for this instance')
    parser.add_argument('--host',
                        action='append',
                        default=list(),
                        help='ES server host, in hostname:port format')
    parser.add_argument('--pattern',
                        default='*logstash*')
    parser.add_argument('--start')
    parser.add_argument('--end')
    return parser.parse_args()


def main():
    args = parse_args()
    # with open(args.outfile, 'wb') as outfile:
    query = None
    if args.instance:
        query = {
            "match": {
                "instance": {
                    "query": args.instance,
                    "type": "phrase"
                }
            }
        }
    sys.stderr.write('connecting to {}\n'.format(args.host))
    documents = DataReader(Elasticsearch(args.host), args.pattern).get_documents(
            args.start, args.end, query=query)
    for document in documents:
        sys.stdout.write(json.dumps(document))
        sys.stdout.write('\n')


if __name__ == '__main__':
    main()
