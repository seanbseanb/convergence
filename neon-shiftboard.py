# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import requests, json, pprint

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

heads={'userSessionId': userSessionId, 'Content-Type': 'application/json' }

#
# Let's get attendees
#
# https://api.neoncrm.com/neonws/services/api/event/retrieveEventAttendees?&userSessionId=' + userSessionId + '&eventId=157
#

payload = {
 'userSessionId': userSessionId,
 'eventId': '157',
 'page.pageSize': '100'
}
foo = _url('/event/retrieveEventAttendees')

resp = requests.get(foo, payload)
print(resp.url)
#resp = requests.post(_url('/dcaportal/api/bsmsearch/mySecurityGroups'),headers=heads)


if resp.status_code != 200:
    # This means something went wrong.
    raise ApiError('GET /event/retrieveEventAttendees {}'.format(resp.status_code))

j = resp.json()

pageData = j['retrieveEventAttendees']['page']
pprint.pprint(pageData)

attendees = j['retrieveEventAttendees']['eventAttendeesResults']['eventAttendeesResult']

# {"errorCode":null,"taskId":"42"}

#if j['errorCode'] != 'None':
#    # This means something went wrong.
#    #raise ApiError('GET /tasks/ {}'.format(resp.text))
#    print('Something went wrong: ')
#    print(j['errorCode'])
#    exit()

exit()