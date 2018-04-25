from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import requests

class SimpleServer(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text-html')
        self.end_headers()
        #self.wfile.write(self.path.encode("utf-8"))
        if self.path=="/":
            directory='/home/shubhamj/Desktop/Simple_HTTP_Server/' 
            f=open(directory+"index.html")
            self.wfile.write(f.read().encode("utf-8"))
            f.close()
            
        elif self.path=="/calculate":
            self.wfile.write(b'calculating fare')
        
        else:
            self.wfile.write(b'Invalid URL')


    def do_POST(self):
        api_key="qbwkfe5yx8"
        journey_date='05-07-2018'
        passenger_age=21

        self.send_response(200)
        self.send_header('Content-type','text-html')
        self.end_headers()
        content_length=int(self.headers['Content-Length'])
        #self.wfile.write(str(content_length).encode("utf-8"))
        data=self.rfile.read(content_length)
        
        #self.wfile.write(bytes(str(data),"utf-8"))

        source_station=bytes(str(data).split('&')[0].split('=')[1],"utf-8")
        destination_station=bytes(str(data).split('&')[1].split('=')[1],"utf-8")
       # journey_date=bytes(str(data).split('&')[2].split('=')[1],"utf-8")
        #self.wfile.write(source_station)
        #self.wfile.write(destination_station)
       # self.wfile.write(journey_date)


        self.wfile.write('''
<html>
    <head>
        <title>Train Fare</title>
        <link href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    </head>
    <body>
       <div class="container">
           <div class="jumbotron">'''.encode("utf-8"))
        self.wfile.write("<h2>Source Station is".encode("utf-8"))
        self.wfile.write(source_station)
        self.wfile.write("</h2><br><h2>Destination Station is".encode("utf-8"))
        self.wfile.write(destination_station)
       

        request_string="https://api.railwayapi.com/v2/between/source/"+source_station.decode("utf-8") +"/dest/"+destination_station.decode("utf-8") +"/date/"+journey_date+"/apikey/"+api_key
        #self.wfile.write(bytes(request_string,"utf-8"))
        json_response=json.loads(requests.get(request_string).content.decode('utf-8'))

        total_train=json_response['total']
        self.wfile.write("<br>Trains Available are ".encode("utf-8"))
        self.wfile.write(str(total_train).encode("utf-8"))
        #print(str(total_train)+" trains between "+source_station+" and "+destination_station+" on "+journey_date+"\n")

        shortest_distance=100000
        shortest_distance_train=''

        self.wfile.write('''
               </h2> <table class="table">
                    <thead>
                        <th>Train No.</th>
                        <th>Train Name</th>
                        <th>Fare</th>
                        <th>Distance</th>
                    </thead>
                    <tbody>'''.encode("utf-8"))

        for i in range(total_train):
            fare_request_string="https://api.railwayapi.com/v2/fare/train/"+json_response['trains'][i]['number']+"/source/"+source_station.decode("utf-8")+"/dest/"+destination_station.decode("utf-8")+"/age/"+str(passenger_age)+"/pref/SL/quota/GN/date/"+journey_date+"/apikey/"+api_key
            fare_response=json.loads(requests.get(fare_request_string).content.decode('utf-8'))
            distance=0

            request_string2="https://api.railwayapi.com/v2/route/train/"+json_response['trains'][i]['number']+"/apikey/"+api_key
            
            response=json.loads(requests.get(request_string2).content.decode("utf-8"))
            #self.wfile.write(str(len(response['route'])).encode("utf-8"))
            for j in range(len(response['route'])):
                #self.wfile.write(str(response['route'][j]['distance']).encode("utf-8"))
                #self.wfile.write('''<br>'''.encode("utf-8"))
                if response['route'][j]['station']['code']==source_station.decode("utf-8"):
                    distance-=response['route'][j]['distance']
                    
                elif response['route'][j]['station']['code']==destination_station.decode("utf-8"):
                    distance+=response['route'][j]['distance']
      
            if distance<shortest_distance:
                shortest_distance=distance
                shortest_distance_train=json_response['trains'][i]['number']
  
            self.wfile.write('''<tr>
                            <td>'''.encode("utf-8"))
            self.wfile.write(bytes(json_response['trains'][i]['number'],"utf-8"))
            self.wfile.write('''</td>
                            <td>'''.encode("utf-8"))
            self.wfile.write(bytes(json_response['trains'][i]['name'],"utf-8"))
            self.wfile.write('''</td>
                            <td>'''.encode("utf-8"))
            self.wfile.write(bytes(str(fare_response['fare']),"utf-8"))
            self.wfile.write('''</td>
                            <td>'''.encode("utf-8"))
            self.wfile.write(bytes(str(distance),"utf-8"))
            self.wfile.write('''</td></td>'''.encode("utf=8"))
            #  printing the result in a tabular form
            #print('%-12s%-26s%-12s%-12s' %(json_response['trains'][i]['number'],json_response['trains'][i]['name'],fare_response['fare'],distance))
    
       
        #print("\nShortest distance between %s and %s is by train number %s" %(source_station,destination_station,shortest_distance_train))        
              
        self.wfile.write('''
                    </tbody>
                </table>'''.encode("utf-8"))
        self.wfile.write("<br>Shortest path is  ".encode("utf-8"))
        self.wfile.write(bytes(str(shortest_distance)+" by train no ","utf-8"))
        self.wfile.write(shortest_distance_train.encode("utf-8"))
        self.wfile.write('''
            </div>
        </div>
    </body>
</html>'''.encode("utf-8"))     
    
httpd=HTTPServer(('0.0.0.0',8001),SimpleServer)
httpd.serve_forever()


