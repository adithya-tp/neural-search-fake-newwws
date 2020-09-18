__copyright__ = "Copyright (c) 2020 Jina AI Limited. All rights reserved."
__license__ = "Apache-2.0"


import csv
import os
import re
import sys


def read_data(data_fn, output_fn):
    _min_sent_len = 50
    _max_sent_len = 500
    punct_chars = ['!', '.', '?', '։', '؟', '۔', '܀', '܁', '܂', '‼', '‽', '⁇', '⁈', '⁉', '⸮', '﹖', '﹗',
                   '！', '．', '？', '｡', '。']
    _slit_pat = re.compile('([{0}])+([^{0}])'.format(''.join(punct_chars)))
    _replace_pat = re.compile('{}'.format(punct_chars))

    if not os.path.exists(data_fn):
        print('file not found: {}'.format(data_fn))
    news_list = []
    character_set = set()
    with open(data_fn, 'r') as f:
        f_h = csv.reader(f)
        for _idx, l in enumerate(f_h):
            if _idx == 0:
                continue
            _, text, _, veracity = l
            veracity = veracity.strip().lower()
            text = text.strip('"').lower().rstrip("\n")
            sents = [s.strip() for s in text.split('\n') if _min_sent_len <= len(s.strip()) <= _max_sent_len]
            character_set.add(veracity)
            for s in sents:
                news_list.append('{}[SEP]{}'.format(veracity, s))
    news_list = list(frozenset(news_list))
    print('some statistics about the data:')
    print('\tnum characters: {}'.format(len(character_set)))
    print('\tnum documents: {}'.format(len(news_list)))
    with open(output_fn, 'w') as f:
        f.write('\n'.join(news_list))


if __name__ == '__main__':
    data_dir = '/tmp/jina/fake-news'
    read_data(
        os.path.join(data_dir, 'corona-news-cleaned.csv'), os.path.join(data_dir, 'extra-clean/cleanest-yet.csv'))
