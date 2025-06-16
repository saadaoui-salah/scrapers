import urllib.request
import json


def fetch_token():
    surl = "https://www.upwork.com/nx/top-nav-ssi/visitor-gql-token"
    headers = {
        "accept": "*/*",
        "accept-language": "fr-FR,fr;q=0.9,ar-DZ;q=0.8,ar;q=0.7,en-US;q=0.6,en;q=0.5",
        "cache-control": "no-cache",
        "content-length": "0",
        "dnt": "1",
        "origin": "https://www.upwork.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://www.upwork.com/nx/search/jobs/?nbs=1&q=seo&page=2",
        "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        "sec-ch-ua-arch": '"x86"',
        "sec-ch-ua-bitness": '"64"',
        "sec-ch-ua-full-version": '"129.0.6668.58"',
        "sec-ch-ua-full-version-list": '"Google Chrome";v="129.0.6668.58", "Not=A?Brand";v="8.0.0.0", "Chromium";v="129.0.6668.58"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-model": '""',
        "sec-ch-ua-platform": '"Linux"',
        "sec-ch-ua-platform-version": '"6.8.11"',
        "sec-ch-viewport-width": "1131",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "vnd-eo-parent-span-id": "1c46164f-92ff-424b-9567-c662b5ec5b13",
        "vnd-eo-span-id": "14109f9d-daab-42c4-a7b7-c21b321cae16",
        "vnd-eo-trace-id": "94702327cbbb1c68-PDX",
    }

    data = b""  # empty POST body

    req = urllib.request.Request(surl, data=data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req) as response:
            result = response.read().decode("utf-8")
            print(result)
            return result
    except Exception as e:
        print("Error:", e)

url = 'https://www.upwork.com/api/graphql/v1?alias=visitorJobSearch'
token = fetch_token()
headers = {
    'accept': '*/*',
    'accept-language': 'fr-FR,fr;q=0.9,ar-DZ;q=0.8,ar;q=0.7,en-US;q=0.6,en;q=0.5',
    'authorization': f'Bearer {token}',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'dnt': '1',
    'origin': 'https://www.upwork.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.upwork.com/nx/search/jobs/?nbs=1&q=seo&page=2',
    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-bitness': '"64"',
    'sec-ch-ua-full-version': '"129.0.6668.58"',
    'sec-ch-ua-full-version-list': '"Google Chrome";v="129.0.6668.58", "Not=A?Brand";v="8.0.0.0", "Chromium";v="129.0.6668.58"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Linux"',
    'sec-ch-ua-platform-version': '"6.8.11"',
    'sec-ch-viewport-width': '1131',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'vnd-eo-parent-span-id': '46a60745-ea43-4c94-8587-196919298ab1',
    'vnd-eo-span-id': '4af2d342-2dcf-499b-85b5-6aea55e2cb47',
    'vnd-eo-trace-id': '946f6f9f9ded4e20-SEA',
    'vnd-eo-visitorid': '105.235.137.54.1748452166124000',
    'x-upwork-accept-language': 'en-US',
}



payload = {
    "query": """
      query VisitorJobSearch($requestVariables: VisitorJobSearchV1Request!) {
        search {
          universalSearchNuxt {
            visitorJobSearchV1(request: $requestVariables) {
              paging {
                total
                offset
                count
              }
              facets {
                jobType { key value }
                workload { key value }
                clientHires { key value }
                durationV3 { key value }
                amount { key value }
                contractorTier { key value }
                contractToHire { key value }
              }
              results {
                id
                title
                description
                relevanceEncoded
                ontologySkills {
                  uid
                  parentSkillUid
                  prefLabel
                  prettyName: prefLabel
                  freeText
                  highlighted
                }
                jobTile {
                  job {
                    id
                    ciphertext: cipherText
                    jobType
                    weeklyRetainerBudget
                    hourlyBudgetMax
                    hourlyBudgetMin
                    hourlyEngagementType
                    contractorTier
                    sourcingTimestamp
                    createTime
                    publishTime
                    hourlyEngagementDuration {
                      rid
                      label
                      weeks
                      mtime
                      ctime
                    }
                    fixedPriceAmount {
                      isoCurrencyCode
                      amount
                    }
                    fixedPriceEngagementDuration {
                      id
                      rid
                      label
                      weeks
                      ctime
                      mtime
                    }
                  }
                }
              }
            }
          }
        }
      }
    """,
    "variables": {
        "requestVariables": {
            "userQuery": "seo",
            "sort": "recency",
            "highlight": True,
            "paging": {
                "offset": 10,
                "count": 10
            }
        }
    }
}

# Convert the payload to JSON and then encode it
data = json.dumps(payload).encode('utf-8')

# Create the request object
req = urllib.request.Request(url, data=data, headers=headers)

# Send the request and get the response
try:
    with urllib.request.urlopen(req) as response:
        result = response.read().decode()
        print(result)
except urllib.error.HTTPError as e:
    print(f'HTTP Error: {e.code} - {e.reason}')
    print(e.read().decode())
except urllib.error.URLError as e:
    print(f'URL Error: {e.reason}')
