from django.http import HttpResponse
from django.shortcuts import render
import http.client, urllib.request, urllib.parse, urllib.error, base64
import json

def homepage(request):
    return render(request, 'homepage.html')

def price(request):
    depart = request.GET['depart']
    arrive = request.GET['arrive']

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


    my_data = json.loads(data)

    # grab the peaktime/offpeaktime/seniordisabled fare

    railfare = my_data['StationToStationInfos'][0]['RailFare']

    peaktime = railfare.get('PeakTime')
    offpeaktime = railfare.get('OffPeakTime')
    seniordisabled = railfare.get('SeniorDisabled')

    return render(request, 'price.html', {'peaktime': peaktime, 'offpeaktime': offpeaktime, 'seniordisabled': seniordisabled})
