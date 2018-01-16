#!/user/bin/python

import sys
import urllib.request
import json
import base64
import struct


def request_data(url: str, token: str):

    response: object

    with urllib.request.urlopen(f'{url}?access_token={token}') as f:
        response = json.loads(f.read().decode())

    return response


def process_bytes(data_bytes: str):

    data = {}

    numbers = struct.unpack('iIhfd', base64.b64decode(data_bytes)[:-8])
    big_endian_number = struct.unpack('d', base64.b64decode(data_bytes)[-8:][::-1])

    data['int'] = numbers[0]
    data['uint'] = numbers[1]
    data['short'] = numbers[2]
    data['float'] = numbers[3]
    data['double'] = numbers[4]
    data['big_endian_double'] = big_endian_number[0]

    return data


def send_numbers(data: object, url: str, token: str):

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
    response = request_data('https://hackattic.com/challenges/help_me_unpack/problem', token)
    data = process_bytes(response['bytes'])
    send_numbers(data, 'https://hackattic.com/challenges/help_me_unpack/solve', token)


if __name__ == '__main__':
    main()