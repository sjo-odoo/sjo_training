import requests
import json

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
  print('%-12s%-26s%-12s%-12s' %(json_response['trains'][i]['number'],json_response['trains'][i]['name'],fare_response['fare'],distance))
  
  
print("\nShortest distance between %s and %s is by train number %s" %(source_station,destination_station,shortest_distance_train))
  