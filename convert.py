import csv
import random
import json
import os
import jsonlines

def load_jsonl(filename):
    data = []
    with jsonlines.open('./data/'+filename+'.jsonl') as reader:
        for row in reader:
            data.append(row)
    return data

def get_cmv(data):
    cnt = 0
    for row in data:
        cnt += 1
        if cnt < 1000:
            continue
        if cnt > 1200:
            break
        book = {
            'id': row['claim_id'],
            'claim_index': row['post_sent_idx'],
            'claim_context': row['post_sents'],
            'con_evidence': []
        }
        for con_evidence in row['con_evidence']:
            book['con_evidence'].append({
                'ev_id': con_evidence['id'],
                'ev_url': con_evidence['ev_url'],
                'ev_netloc': con_evidence['ev_url_netloc'],
                'ev_text': con_evidence['ev_text'],
                'ev_context': con_evidence['ev_context']
            })
        with open('./data/contexts/%s.json' % book['id'], 'w') as f:
            json.dump(book, f, sort_keys=True, indent=4)

def get_kialo(data):
    for row in data:
        book = {
            'id': row['claim_id'],
            'claim_text': row['claim_text'],
            'claim_context': row['claim_text'],
            'con_evidence': []
        }
        for con_evidence in row['con_evidence']:
            book['con_evidence'].append({
                'ev_id': con_evidence['id'],
                'ev_url': con_evidence['ev_url'],
                'ev_netloc': con_evidence['ev_url_netloc'],
                'ev_text': con_evidence['ev_text'],
                'ev_context': con_evidence['ev_context']
            })
        with open('./data/contexts/%s.json' % book['id'], 'w') as f:
            json.dump(book, f, sort_keys=True, indent=4)

def conv(filename):
    if not os.path.exists('./data/contexts'):
        os.makedirs('./data/contexts')

    if filename.startswith('cmv'):
        get_cmv(load_jsonl(filename))
    elif filename.startswith('kialo'):
        get_kialo(load_jsonl(filename))

def main():
    conv('cmv-annot-1')

if __name__ == "__main__":
    main()