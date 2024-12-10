import requests
import random
import time
from concurrent.futures import ThreadPoolExecutor

username = input('Enter username: ')
times = int(input('How many times? '))

sents = 0
fails = 0

def pick(filename):
 with open(filename, 'r') as afile:
    line = next(afile)
    for num, aline in enumerate(afile, 2):
        if random.randrange(num):
            continue
        line = aline
    return line

MAX_RETRIES = 10

def send_request(_):
    headers = {
        'authority': 'ngl.link',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://ngl.link',
        'referer': 'https://ngl.link/' + username,
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
        'x-requested-with': 'XMLHttpRequest',
    }

    data = {
        'username': username,
        'question': pick('D:/PythonProjects/NGLSpammer/list.txt'),
        'deviceId': pick('D:/PythonProjects/NGLSpammer/uuids.txt')
    }

    s = requests.Session()
    global sents, fails
    for _ in range(MAX_RETRIES):
        try:
            r = s.post('https://ngl.link/api/submit', headers=headers, data=data, timeout=5)
            if r.status_code == 200:
                print('Sent as (' + data['deviceId'] + '): ' + data['question'])
                sents += 1
                return True
        except requests.exceptions.Timeout:
            print("The request timed out, retrying...")
        except Exception as e:
            print(f'Failed due to: {e}, retrying...')
        time.sleep(3)
    fails += 1
    return False

with ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(send_request, range(times)))

print('Sents:', sents)
print('Fails:', fails)

ok = input('Again? [Y/N]: ')

while ok.lower() == 'y':
    username = input('Enter username: ')
    times = int(input('How many times? '))

    sents = 0
    fails = 0

    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(send_request, range(times)))

    print('Sents:', sents)
    print('Fails:', fails)

    ok = input('Again? [Y/N]: ')