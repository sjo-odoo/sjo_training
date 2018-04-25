from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
import json


class HTTPRequest(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type","text/html")
        self.end_headers()
        self.wfile.write('''<html>\
    <head> \
        <title>Train Fare</title> \
        <link href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">\
    </head>\
    <body>'''.encode("utf-8"))
        self.wfile.write(b'Hello vbWorld')


    # API KEY
        api_key="jwq1ybnyjb"


        #source_station=input(" Enter the source station\n")
        source_station="BRC"


        #destination_station=input(" Enter the destination station\n")
        destination_station="UMB"

        #journey_date=input(" Enter journey date in DD-MM-YYYY format\n")
        journey_date="05-07-2018"


        passenger_age=21

        request_string="https://api.railwayapi.com/v2/between/source/"+source_station+"/dest/"+destination_station+"/date/"+journey_date+"/apikey/"+api_key

        json_response=json.loads(requests.get(request_string).content)

        total_train=json_response['total']
        print(str(total_train)+" trains between "+source_station+" and "+destination_station+" on "+journey_date+"\n")

        shortest_distance=100000
        shortest_distance_train=''

        print("%-12s%-26s%-12s%-12s" %("Train No.","Train Name","Fare","Distance"))
        print("_______________________________________________________")
        for i in range(total_train):
            fare_request_string="https://api.railwayapi.com/v2/fare/train/"+json_response['trains'][i]['number']+"/source/"+source_station+"/dest/"+destination_station+"/age/"+str(passenger_age)+"/pref/SL/quota/GN/date/"+journey_date+"/apikey/"+api_key
            fare_response=json.loads(requests.get(fare_request_string).content)
            
            
            
            distance=0
            train_number=12449

            request_string="https://api.railwayapi.com/v2/route/train/"+json_response['trains'][i]['number']+"/apikey/"+api_key

            response=json.loads(requests.get(request_string).content)
            for j in range(len(response['route'])):
                if response['route'][j]['station']['code']==source_station:
                    distance-=response['route'][j]['distance']
                elif response['route'][j]['station']['code']==destination_station:
                    distance+=response['route'][j]['distance']
            
            if distance<shortest_distance:
                shortest_distance=distance
                shortest_distance_train=json_response['trains'][i]['number']
        

            #  printing the result in a tabular form
            print('%-12s%-26s%-12s%-12s' %(json_response['trains'][i]['number'].encode("utf-8"),json_response['trains'][i]['name'],fare_response['fare'],distance))
            
        
        print("\nShortest distance between %s and %s is by train number %s" %(source_station,destination_station,shortest_distance_train))
        
                

    def do_POST(self):
        #content_length=int(self.headers['Content-Length'])
       # body=self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        #self.wfile.write(response.getvalue())
        self.wfile.write(b'POST REQUEST')

httpd=HTTPServer(('0.0.0.0',8021),HTTPRequest)

httpd.serve_forever()