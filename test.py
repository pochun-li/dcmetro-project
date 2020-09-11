import http.client, urllib.request, urllib.parse, urllib.error, base64

depart = input('Enter your origin station code: ')
arrive = input('Enter your destination station code: ')

headers = {
    # Request headers
    'api_key': 'cff10c2c747945e49cdf5c657be1f4b3',
}

params = urllib.parse.urlencode({
    # Request parameters
    'FromStationCode': depart,
    'ToStationCode': arrive,
})

try:
    conn = http.client.HTTPSConnection('api.wmata.com')
    conn.request("GET", "/Rail.svc/json/jSrcStationToDstStationInfo?%s" % params, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

# transfer the data to dictionary type

import json
my_data = json.loads(data)

# grab the peaktime/offpeaktime/seniordisabled fare

railfare = my_data['StationToStationInfos'][0]['RailFare']

peaktime = railfare.get('PeakTime')
offpeaktime = railfare.get('OffPeakTime')
seniordisabled = railfare.get('SeniorDisabled')

print('The peak time fare from ' + str(depart) + ' to ' + str(arrive)+ ' is $' + str(peaktime) + '.')
print('The off peak time fare from ' + str(depart) + ' to ' + str(arrive)+ ' is $' + str(offpeaktime) + '.')
print('The senior or disabled fare from ' + str(depart) + ' to ' + str(arrive)+ ' is $' + str(seniordisabled) + '.')
