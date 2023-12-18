import json
import collections
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class Connection:
    ''' Connection '''
    @staticmethod
    def start(method, url, payload=None, api_key=None, debug=False):
        ''' start '''
        req = None
        headers = {"Content-Type": "application/json", "Idelium-Key": api_key}
        if method == "POST":
            req = requests.post(url,
                              headers=headers,
                              data=json.dumps(payload),
                              verify=False)
        elif method == "PUT":
            req = requests.put(url,
                             headers=headers,
                             data=json.dumps(payload),
                             verify=False)
        elif method == "GET":
            req = requests.get(url, headers=headers, verify=False)
        if debug is True:
            print("Response: " + req.text)
            print("Headers: " + json.dumps(headers))
            print("Payload: " + json.dumps(payload))
            print(str(req.status_code) + " " + method + " " + url)
        return json.loads(req.text, object_pairs_hook=collections.OrderedDict)
