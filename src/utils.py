import requests
import json

def query(endpoint = '', parameters = {} ):
  """
  HTTP Return Codes

  HTTP 4XX return codes are used for malformed requests; the issue is on the sender's side.
  HTTP 403 return code is used when the WAF Limit (Web Application Firewall) has been violated.
  HTTP 429 return code is used when breaking a request rate limit.
  HTTP 418 return code is used when an IP has been auto-banned for continuing to send requests after receiving 429 codes.
  HTTP 5XX return codes are used for internal errors; the issue is on Binance's side. It is important to NOT treat this as a failure operation; the execution status is UNKNOWN and could have been a success.

  """
  header={
    'Accepts': 'application/json',
  }

  response = requests.get(url=endpoint,headers=header,params=parameters)

  if response.status_code == 200:
    return response
  else:
    print("HTTP Return Codes\n\n\
          HTTP 4XX return codes are used for malformed requests; the issue is on the sender's side.\n\
          HTTP 403 return code is used when the WAF Limit (Web Application Firewall) has been violated.\n\
          HTTP 429 return code is used when breaking a request rate limit.\n\
          HTTP 418 return code is used when an IP has been auto-banned for continuing to send requests after receiving 429 codes.\n\
          HTTP 5XX return codes are used for internal errors; the issue is on Binance's side. It is important to NOT treat this as a failure operation; the execution status is UNKNOWN and could have been a success."
          )
    print (f'error: {response.status_code}')
    exit()

def writeResponses(self,response,fileName='test'):
  with open(f'binance/responsesJson/{fileName}.json','w') as f:
    json.dump(response.json(),f,indent=2)