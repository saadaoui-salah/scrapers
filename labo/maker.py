import glob
import json

def read_json(path):
    with open(path,'r') as file:
        data = json.loads(file.read())
        return data

file_pattern = "./*.json"

file_list = glob.glob(file_pattern)

#for file in file_list:
#    data = read_json(file)
#    for user in data[0]['data']['view']['people']['nodes']:
#        if user['userInfo']['id'] == 'VXNlcl84OTAzMzA2':
#            print(user['userInfo']['hasSentRequest'])
#        if not user['userInfo']['hasSentRequest'] and not user['userInfo']['isConnected']:
#            needed_users += [user['userId']]
#
#print(needed_users)
#

import requests
import time


url = "https://connections.arabhealthonline.com/api/graphql"

headers = {
    "accept": "*/*",
    "accept-language": "fr-FR,fr;q=0.9,ar-DZ;q=0.8,ar;q=0.7,en-US;q=0.6,en;q=0.5",
    "authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb3JlQXBpVXNlcklkIjoiVlhObGNsOHlNalEwT0RreU1nPT0iLCJwZXJtaXNzaW9ucyI6WyJhcHBsaWNhdGlvbjpRWEJ3YkdsallYUnBiMjVmTlRJeCIsInNjaGVtYTp1c2VyIl0sInNlc3Npb25JZCI6IjY3YTYwNjU1NTg0ZjFiYTgxMzNhNWI1NyIsInR5cGUiOiJhY2Nlc3MtdG9rZW4iLCJ1c2VySWQiOiI2NzQ5YmIwYTczMWY2OWUwZjc4M2NlZmMiLCJlbWFpbFZlcmlmaWVkIjp0cnVlLCJpYXQiOjE3NDAxMjg5ODYsImV4cCI6MTc0MDIxNTM4NiwiaXNzIjoiYXV0aC1hcGkifQ.pQYxvGjcx-jSbTSEXdnz3tZdSgDK7fl40cKj2G6RjWyzs9QfvjVMBOEattoHOg8bjGy4at5v-rl2NEHpeWrQNzPg2rBJ2MlVpIwFJQNPYoIPN1ySf8uOM93wrQXHiCDGWQZ8pQiIZI8_k1QhpHcOxMQ6e-d3a4j32E6725Skqw6yLXmzOnTSQxooUKOvlVLru5ptYTgCxWJRMXtSPLjjESevcTajdgBupvWngf_2rN2jf1_lBPxfAzHRvmwmy1U098khC_JvXKQ4N-GsdZ45krubIjue00jHxuw7ZtDBStKDvMhv2cnydOKnOAANLKvMlO6lhr49Rb6eFvr8h60PUyF_nIZNHRE56k6BBNWqHKxF_aCDX1_hC7wEw3i2NHuO1f7Qy2NLIxPTRXIDyEGX6hJ3hK9jQ4HpUVLfvkwfe5Tw5Sr1xsQ9Eh-7f7SbUQ4PB-B-G2PinFEXX-G1XzFRW1qyr1XxlmdiZGN3Xmw3ROLZEul-LoI794BPOQvfIHg10tHwqAu1HGRVDtqSzhWIrLCiyspPSPrBu50ZJK8hqph9IfpbkgQwviMJ3OfN_KfRWt3R3WWRLF6f-jy6eI4I-u90eeT4EfbxIqAdLpuHYCVxN5FbagqEvBPB7hG2cZqF_rwV0mLG4xiUmo11ifxcy3F2UJYvbxU5XFRQ3LiMDSo",
    "cache-control": "no-cache",
    "content-type": "application/json",
    "dnt": "1",
    "origin": "https://connections.arabhealthonline.com",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://connections.arabhealthonline.com/",
    "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "x-client-origin": "connections.arabhealthonline.com",
    "x-client-platform": "Event App",
    "x-client-version": "2.309.108",
    "x-feature-flags": "fixBackwardPaginationOrder"
}

USERS = {'VXNlcl8yMjc5NzY1OA==', 'VXNlcl8yMjQ5ODIwOA==', 'VXNlcl8yMjc5NzY1OQ==', 'VXNlcl8yMjYzOTI4NA==', 'VXNlcl8xODAxOTA2MQ==', 'VXNlcl8yMjk5NTQ0Nw==', 'VXNlcl83MDE0NDA0', 'VXNlcl8yMDg2NTEwOQ==', 'VXNlcl8xNzk1MTY1NA==', 'VXNlcl8xNzYyNDUyMQ==', 'VXNlcl81NTg4MTE1', 'VXNlcl8xNzk5Njg5MQ==', 'VXNlcl8xMjUzNTMyOQ==', 'VXNlcl8yMjUyMzAyNQ==', 'VXNlcl8xMzg3NDgyNg==', 'VXNlcl8xODAxNzM4MQ==', 'VXNlcl81OTM4Njgw', 'VXNlcl8xNzYyODgxNQ==', 'VXNlcl8yMjYyOTI3Nw==', 'VXNlcl8xMzA4NDQ4OQ==', 'VXNlcl85MDM2MDI3', 'VXNlcl81ODc5NTUx', 'VXNlcl84Nzg3MDU4', 'VXNlcl83ODU5OTYw', 'VXNlcl8yMjk4Njg1OQ==', 'VXNlcl84OTMwNzg5', 'VXNlcl8yMzAzMTI3OA==', 'VXNlcl8yMjY4OTcxNQ==', 'VXNlcl8xNzk3MDA0NQ==', 'VXNlcl8xMjk3MDc4MA==', 'VXNlcl8yMjg3MTcyMw==', 'VXNlcl8xNzk4NDM5MA==', 'VXNlcl8xNzk4MzkxMA==', 'VXNlcl8xMzA4NTA2OA==', 'VXNlcl8yMzA2NTM1NA==', 'VXNlcl8yMjU5MDAyMw==', 'VXNlcl84OTE5MzAy', 'VXNlcl8xMjYwOTE0NQ==', 'VXNlcl84NzYwMjg0', 'VXNlcl8yMjk2NTkwNQ==', 'VXNlcl8xMTI0NzM2', 'VXNlcl8yMjgxNjM1Mg==', 'VXNlcl81ODY4Mzg2', 'VXNlcl81OTY2MzY4', 'VXNlcl8yMjUyMTM1Mw==', 'VXNlcl84MzMwMzE3', 'VXNlcl81ODk1NzQ0', 'VXNlcl8zODUzMTA0', 'VXNlcl8yMjY2NjkwNA==', 'VXNlcl84ODk3MjYz', 'VXNlcl8xMjE1Nzc5MQ==', 'VXNlcl8yMjUxNzU0Mg==', 'VXNlcl8yMjQ3MTIyNg==', 'VXNlcl8yMzAyNDY2Mg==', 'VXNlcl8xMzAzNTM0Mw==', 'VXNlcl81NTg5Mjcw', 'VXNlcl84NzYyMjIy', 'VXNlcl8xODAyNzQyNw==', 'VXNlcl8xNzczNzE1Mg==', 'VXNlcl8xMjQ4Mzcz', 'VXNlcl8yMjY4ODQ1OQ==', 'VXNlcl83Nzk1MjMx', 'VXNlcl8xNzg2NTAwMw==', 'VXNlcl8xMjc2MTAxOA==', 'VXNlcl8yMjM2MTM0OA==', 'VXNlcl84OTg5NTUz', 'VXNlcl8xODAwMDExNg==', 'VXNlcl8xNzU0NTM0Nw==', 'VXNlcl8xMjkwMTIwMg==', 'VXNlcl8xODA2ODAwNA==', 'VXNlcl8yMzA1OTcxMw==', 'VXNlcl8yMjcwNDAyOA==', 'VXNlcl81MjUwMjAy', 'VXNlcl8yMzAxOTI5MA==', 'VXNlcl8xMjk1NDYzOA==', 'VXNlcl81OTA2Mjcx', 'VXNlcl8xMjk3Mzc4MA==', 'VXNlcl8yMjI2MDQ3OQ==', 'VXNlcl83MTI0NjU2', 'VXNlcl8yMzA2MTMzOA==', 'VXNlcl8yMjUzNjg5NA==', 'VXNlcl81Njg0NTI2', 'VXNlcl8xMjUyODI0Mw==', 'VXNlcl8yMjk3NjE2MQ==', 'VXNlcl8xMzAwNjM3OA==', 'VXNlcl8yMzA0NjE2Mg==', 'VXNlcl8xMjQ0OTAyMg==', 'VXNlcl8yMjUwNjMwMg==', 'VXNlcl8xNzAyNDg5OQ==', 'VXNlcl8xNzg1MTUxNQ==', 'VXNlcl84OTY3OTM4', 'VXNlcl8xMzA0MzYzMA==', 'VXNlcl85MDI1MzY4', 'VXNlcl8xMjk2NDI4NQ==', 'VXNlcl8xNzQwNTQwMw==', 'VXNlcl8xMjQ2NjQzMg==', 'VXNlcl8xMjU0Njg1NQ==', 'VXNlcl84MjYxODU5', 'VXNlcl8yMzA0NDY0MQ==', 'VXNlcl8yMjU5Njg4NQ==', 'VXNlcl8yMzA2MDUyOQ==', 'VXNlcl8yMjYxNTQ5Nw==', 'VXNlcl84OTAzMTI2', 'VXNlcl84ODk3NTcy', 'VXNlcl8yMjkxMTU0MA==', 'VXNlcl8yMjMyNjMxNw==', 'VXNlcl8yMzAzMTE2OA==', 'VXNlcl8xNzE3MDEzNg==', 'VXNlcl8xNzQ4Mzk5Ng==', 'VXNlcl8yMzAzMTQ4Mw==', 'VXNlcl8xNzgwMTE4MA==', 'VXNlcl8xMjc1MTk1MA==', 'VXNlcl8yMjQ2MTEwNw==', 'VXNlcl8yMjYzMDk5Nw==', 'VXNlcl8xODAzMDQyNA==', 'VXNlcl8xODAwMzI4NA==', 'VXNlcl8yMjY5MDc0Mg==', 'VXNlcl8yMjU1OTAzOA==', 'VXNlcl8yMjUyMTgyMg==', 'VXNlcl8yMjg2ODczMw==', 'VXNlcl8yMjY3ODcwMA==', 'VXNlcl8xNzc1NDYwMw==', 'VXNlcl8yMzA1MTMwNw==', 'VXNlcl8xMTcxMTM5', 'VXNlcl8yMzA0MzA4Nw==', 'VXNlcl8yMjYwODgxNw==', 'VXNlcl81NzM2MDUw', 'VXNlcl8xMjYzMTQ4MA==', 'VXNlcl8xMjcwODg0OA==', 'VXNlcl81ODA1MDMz', 'VXNlcl8xNzc4MzY4Nw==', 'VXNlcl8xMjQ3MzA2OA==', 'VXNlcl8yMzAxOTAxNQ==', 'VXNlcl8yMjUzNjY5Ng==', 'VXNlcl8yMjMyNjEwMg==', 'VXNlcl84ODM5NDUz', 'VXNlcl8xMjk0NTY2NA==', 'VXNlcl8xMjcwNzY5NQ==', 'VXNlcl8xODAwMDU1Ng==', 'VXNlcl8xNzk5MDA2Mg==', 'VXNlcl8xODAwMjAyNA==', 'VXNlcl8xNzQ4NDI5MQ==', 'VXNlcl81ODk5NTEw', 'VXNlcl8xMTQ2Njc4OA==', 'VXNlcl8xNzQ5NjU0NQ==', 'VXNlcl8xMjkwNTM2NA==', 'VXNlcl8yMzAzMjE4OA==', 'VXNlcl81ODk2MjQy', 'VXNlcl8zNDYzODkx', 'VXNlcl80NTg0NzU1', 'VXNlcl8xNzU5Mzg3NQ==', 'VXNlcl84NzI2OTM2', 'VXNlcl8yMjUxNzc2Ng==', 'VXNlcl8yMzAzMTQ5NQ==', 'VXNlcl8yMzAxOTEwNQ==', 'VXNlcl8yMjQ0ODkyMg==', 'VXNlcl85MzIzODc5', 'VXNlcl8yMjY5NDIwMA==', 'VXNlcl8xNzc4NDkwNQ==', 'VXNlcl8yMjQ3NDcyNA==', 'VXNlcl8yMjUxODgxMQ==', 'VXNlcl8xMjcwMDYzNA==', 'VXNlcl8yMjUzODg1OA==', 'VXNlcl8yMjQ5OTY0NQ==', 'VXNlcl8xNzY4MTY1Nw==', 'VXNlcl8xODA0NTk4Mw==', 'VXNlcl8xMjc1MzIwMQ==', 'VXNlcl8xNzU1NTc2Mg==', 'VXNlcl8yMzA2Mzc3MA==', 'VXNlcl8xMjY1NTQyNw==', 'VXNlcl8yMjY0Mjk4Mw==', 'VXNlcl84Nzk5MzE1', 'VXNlcl8xNzQwNTExNg==', 'VXNlcl8xNzkyOTIwNA==', 'VXNlcl8yMjI2MDQ0NQ==', 'VXNlcl84ODQyNjkx', 'VXNlcl8yMzAyMjQ2MQ==', 'VXNlcl8xNjUwMDM3Ng==', 'VXNlcl84ODk3NzM0', 'VXNlcl8yMjU2NjcxMA==', 'VXNlcl8yMzAzMjE4Nw==', 'VXNlcl8yMjg2NTg1Nw==', 'VXNlcl8yMzA0NTQyOQ=='}

def sendRequest():
    sent =[]
    u = set(USERS) - set(sent)
    for user in u:
        payload = [
            {
                "operationName": "PersonConnectMutation",
                "variables": {
                    "message": "Great meeting at Arab Health! Let’s connect on eQMS and Orcanos’ value.",
                    "userId": user,
                    "eventId": "RXZlbnRfMjE0ODk4OA=="
                },
                "extensions": {
                    "persistedQuery": {
                        "version": 1,
                        "sha256Hash": "69747f113503a61fc97acdad1aa50ec1647403e2ca8cd4469bf55e0c6e2c20d9"
                    }
                }
            }
        ]
        response = requests.post(url, headers=headers, json=payload)
        print("######################")
        print(response.status_code)
        print(response.json())
        if user in sent:
            continue

        if not response.json()[0].get('errors'):
            sent += [user]
            print(set(USERS) - set(sent))
            print(len(set(USERS) - set(sent)))
        else:
            if 'A request has already been sent to thi' in response.json()[0]['errors'][0]['message']:
                sent += [user]
                print(set(USERS) - set(sent))
                print(user)
                print(len(set(USERS) - set(sent)))
                continue
            print(user)
            time.sleep(7*60)
        print("######################")

#  'Operation', 'Regulatory'
keywords = ['Quality']
class D:
    users = []

d = D()

def get_users(end_cursor=None):

    for keyword in keywords:
        url = "https://connections.arabhealthonline.com/api/graphql"

        payload = [
            {
                "operationName": "EventPeopleListViewConnectionQuery",
                "variables": {
                    "viewId": "RXZlbnRWaWV3Xzk2MDU5OQ==",
                    "search": keyword,
                },
                "extensions": {
                    "persistedQuery": {
                        "version": 1,
                        "sha256Hash": "7f6aeac87634ef772c93d5b0b2e89c9e7ed810a19868180507be401b9ab18214"
                    }
                }
            }
        ]


        if end_cursor:
            payload[0]['variables']["endCursor"] = end_cursor
        response = requests.post(url, headers=headers, json=payload)

        print(response.status_code)
        data = response.json()[0]['data']['view']['people']
        for user in data['nodes']:
            if not user['userInfo']['hasSentRequest'] and not user['userInfo']['isConnected'] and user['userId'] not in d.users:
                print(len(d.users))
                d.users += [user['userId']]
        if data['pageInfo']['hasNextPage']:
            get_users(data['pageInfo']['endCursor'])

sendRequest()
#get_users()
#print(d.users)