# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import requests, json, pprint, hmac, hashlib
from base64 import b64encode

def _url(path):
        return 'https://api.neoncrm.com/neonws/services/api' + path
# ?login.apiKey=198dad94c6cfcd55c66fb80f8dd8cb73&login.orgid=ce
#
# https://api.neoncrm.com/neonws/services/api/common/login?login.apiKey=198dad94c6cfcd55c66fb80f8dd8cb73&login.orgid=ce
#
#
# Let's get the GUID of the site.
#

class ApiError(Exception):
    """An API Error Exception"""

    def __init__(self, status):
        self.status = status

    def __str__(self):
        return "ApiError: status={}".format(self.status)


loginapiKey = '198dad94c6cfcd55c66fb80f8dd8cb73'
loginorg = 'ce'


foo = _url('/common/login' + '?' + 'login.apiKey=' + loginapiKey + '&login.orgid=' + loginorg)

resp = requests.get(foo)

if resp.status_code != 200:
    # This means something went wrong.
    raise ApiError('GET /common/login {}'.format(resp.status_code))

j = resp.json()

#
#{u'loginResponse': {u'operationResult': u'SUCCESS',
#                    u'responseDateTime': u'2017-05-22T00:51:34.762+0000',
#                    u'responseMessage': u'User logged in.',
#                    u'userSessionId': u'ba0cfec992a401d2652115db24001c29'}}
#

print('Login operationResult: ' + j['loginResponse']['operationResult'])
print('Login userSessionId: ' + j['loginResponse']['userSessionId'])
userSessionId = j['loginResponse']['userSessionId']

pprint.pprint(j)

if j['loginResponse']['operationResult'] == 'SUCCESS':
       print('successfully authenticated' + userSessionId) 

#
# Function to get attendees by page.
#
# https://api.neoncrm.com/neonws/services/api/event/retrieveEventAttendees?&userSessionId=' + userSessionId + '&eventId=157
#
def getEvent(userSessionId):
    str = "this"
    return str


def process_event_attendees(userSessionId, eventId, pageSize):
    "This calls out to NeonCRM and gets the page of attendees for the given event"
    pageNumber = 1
    totalPageNumber = 1
    while pageNumber <= totalPageNumber:
        print('Processing page: {0}'.format(pageNumber))
        payload = {
            'userSessionId': userSessionId,
            'eventId': eventId,
            'page.pageSize': pageSize,
            'page.currentPage': pageNumber
        }
        resp = requests.get(_url('/event/retrieveEventAttendees'), payload)
        print(resp.url)

        if resp.status_code != 200:
            # This means something went wrong.
            raise ApiError('GET /event/retrieveEventAttendees {}'.format(resp.status_code))

        j = resp.json()
        pageNumber += 1
        totalPageNumber = j['retrieveEventAttendees']['page']['totalPage']

        process_attendees(j['retrieveEventAttendees']['eventAttendeesResults']['eventAttendeesResult'])


shiftBoardSigKey = 'ehhqTHvEWdQSLeypElI/7ADQBL58b2GOXbqBYl78'
shiftBoardAccessKey = '74dd571c-cd5f-4342-8a48-a5f4345f1885'
shiftBoardDomain = 'https://api.shiftdata.com'

def update_sig(method, params):
    data = "method" + method + "params" + params
    shiftBoardSig = hmac.new(shiftBoardSigKey.encode('utf-8'), data.encode('utf-8'), hashlib.sha1)
    return b64encode(shiftBoardSig.digest())

def build_sb_payload(method, params):
    return {
        'id': '1',
        'jsonrpc': '2.0',
        'method': method,
        'params': b64encode(params.encode()),
        'signature': update_sig(method, params),
        'access_key_id': shiftBoardAccessKey
    }

def get_account(name):
    method = 'account.list'
    params = '{"select":{"search":"' + name + '"}}'

    resp = requests.get(shiftBoardDomain, build_sb_payload(method, params))

    if resp.status_code != 200:
        raise ApiError('GET {0} {1}'.format(resp.url, resp.status_code))

    j = resp.json()

    if 'error' in j:
        raise ApiError('GET {0} {1}'.format(resp.url, j['error']['data']['message']))

    if int(j['result']['count']) <= 0:
        return None
    return j['result']['accounts'][0]


def create_sb_account(attendee):
    method = 'account.create'
    data = {
        'external_id':attendee['attendeeId'],
        'last_name':attendee['attendeeLastName'],
        'first_name':attendee['attendeeFirstName']
    }
    params = json.dumps(data)



def process_attendees(attendees):
    for attendee in attendees:
        shiftBoardAccount = get_account(attendee['registrantName'])
        if shiftBoardAccount is None:
            # todo: Create a new Account in ShiftBoard using the attendee data.
            print("Not Found")
        else:
            # todo: edit shiftboard account if needed.
            pprint.pprint(shiftBoardAccount)

process_event_attendees(userSessionId, 152, 10)
exit()