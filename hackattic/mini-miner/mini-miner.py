#!/user/bin/python

import sys
import urllib.request
import json
import hashlib


def request_data(url: str, token: str):

    response: object

    with urllib.request.urlopen(f'{url}?access_token={token}') as f:
        response = json.loads(f.read().decode('utf-8'))

    return response


def sort_dict(data: dict):

    sorted_dict = {}

    for pair in sorted(data.items(), key=lambda x: x[0]):
        sorted_dict[pair[0]] = pair[1]

    return sorted_dict


def compute_hash(data: str):

    hash: str

    h = hashlib.sha256()
    h.update(data.encode())
    hash = h.digest()

    return hash


def is_valid(hash: bytes, difficulty: int):

    hex = hash.hex()
    
    digits: int
    if difficulty % 4 == 0:
        digits = difficulty
    else:
        digits = 4 * (difficulty // 4 + 1)

    number = int(hex[:digits // 4], 16)

    return (number >> (digits % 4)) == 0


def find_nonce(params: object):

    difficulty = params['difficulty']
    block = sort_dict(params['block'])

    for nonce in range(10 ** 100):
        block['nonce'] = nonce
        data = json.dumps(block).replace(' ', '')
        
        hash = compute_hash(data)
        if is_valid(hash, difficulty):
            return nonce   


def send_nonce(nonce: int, url: str, token: str):

    data = { 'nonce' : nonce }
    data = json.dumps(data).encode()

    req = urllib.request.Request(url=f'{url}?access_token={token}', data=data, method='POST')
    with urllib.request.urlopen(req) as f:
        print(f.read().decode('utf-8'))


def main():

    if len(sys.argv) < 2:
        print("[ERROR]: No token specified!")
        print("usage: ./mini-miner.py <token>")
        
        exit(-1)

    token = sys.argv[1]
    response = request_data('https://hackattic.com/challenges/mini_miner/problem', token)
    nonce = find_nonce(response)
    send_nonce(nonce, 'https://hackattic.com/challenges/mini_miner/solve', token)

    print(nonce)

if __name__ == '__main__':
    main()