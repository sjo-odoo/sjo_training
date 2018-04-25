import requests
import json

from odoo import models,fields,api,exceptions

class TrainRoute(models.Model):
    _name = "route.route"
    from_station_id = fields.Char(string = "Source station" )
    to_station_id = fields.Char(string = "Destination station" )
    arrival_time = fields.Char( string = "Arrival Time")
    departure_time = fields.Char( string = "Departure Time")
    train_number = fields.Char( string = "Train  Number" )
    train_name = fields.Char( string = "Train Name")
    distance = fields.Float()
    fare = fields.Float( string = "Route fare")
    #fare = fields.Float( compute = 'find_fare')

class Station(models.Model):
    _name = "station.station"
    name = fields.Char(string = "Station name" , required = True)
    code = fields.Char(string = "Station number" , required = True)

class TrainClass(models.Model):
    _name = "train.class"
    train_number = fields.Char( string = "Train Number")
    train_name = fields.Char( string = "Train Name")
    c_3A = fields.Char( string = "Third AC")
    c_2A = fields.Char( string = "Second AC")
    c_1A = fields.Char( string = "First AC")
    c_Sleeper = fields.Char( string = "Sleeper")
    c_2S = fields.Char( string = "2S")
    c_CC = fields.Char( string = "CC")
    c_3E = fields.Char( string = "3E")
    c_FC = fields.Char( string = "FC")

class Days(models.Model):
    _name = "train.days"
    code = fields.Char(string = "Train Number")
    train_name = fields.Char( string = "Train Name")
    monday = fields.Char()
    tuesday = fields.Char()
    wednesday = fields.Char()
    thursday = fields.Char()
    friday = fields.Char()
    saturday = fields.Char()
    sunday = fields.Char()

    def fetch_days(self):
        api_key = "7fcafusbpw"
        request_string = "https://api.railwayapi.com/v2/route/train/"+self.code+"/apikey/"+api_key
        json_response = json.loads(requests.get(request_string).content.decode('utf-8'))

        self.write({
            'monday':json_response['train']['days'][0]['runs'] , 
            'tuesday':json_response['train']['days'][1]['runs'] , 
            'wednesday':json_response['train']['days'][2]['runs'] , 
            'thursday':json_response['train']['days'][3]['runs'] , 
            'friday':json_response['train']['days'][4]['runs'] , 
            'saturday':json_response['train']['days'][5]['runs'] , 
            'sunday':json_response['train']['days'][6]['runs']
        })
class Train(models.Model):
    _name = "train.train"
    _inherit = ["route.route", "train.days", "train.class"]
    name = fields.Char(string = "Train Name")
    code = fields.Char(string = "Train number", required = True)
    _sql_constraints =[
        ('Train_code', 'unique(code)', 'unique train number')
    ]


    @api.one
    def fetch_details(self):
        api_key = "qbwkfe5yx8"
        request_string = "https://api.railwayapi.com/v2/route/train/"+self.code+"/apikey/"+api_key
        json_response = json.loads(requests.get(request_string).content.decode('utf-8'))

        if json_response['response_code']==200 and len(json_response['train'])>0:
            self.write({
                'name' : json_response['train']['name'],
                'from_station_id' : json_response['route'][0]['station']['code'],
                'to_station_id' : json_response['route'][len(json_response['route'])-1]['station']['code'],
                'arrival_time' : json_response['route'][len(json_response['route'])-1]['scharr'],
                'departure_time' : json_response['route'][0]['schdep'],
                'train_number' : str(self.code),
                'train_name' : json_response['train']['name'],
                'distance' : float(json_response['route'][len(json_response['route'])-1]['distance']),
                'fare' : 122.09,
                'c_3A' :  json_response['train']['classes'][0]['available'],
                'c_Sleeper' : json_response['train']['classes'][1]['available'],
                'c_1A' : json_response['train']['classes'][2]['available'],
                'c_2S' : json_response['train']['classes'][3]['available'],
                'c_FC' : json_response['train']['classes'][4]['available'],
                'c_2A' : json_response['train']['classes'][5]['available'],
                'c_CC' : json_response['train']['classes'][6]['available'],
                'c_3E' : json_response['train']['classes'][7]['available'],
                'monday' : json_response['train']['days'][0]['runs'],
                'tuesday' : json_response['train']['days'][1]['runs'],
                'wednesday' : json_response['train']['days'][2]['runs'],
                'thursday' : json_response['train']['days'][3]['runs'],
                'friday' : json_response['train']['days'][4]['runs'],
                'saturday' : json_response['train']['days'][5]['runs'],
                'sunday' : json_response['train']['days'][6]['runs']  
            })

            temp_train=self.env['train.days']
            temp_train.create({
                'code' : self.code,
                'train_name' : json_response['train']['name'],
                'monday' : json_response['train']['days'][0]['runs'],
                'tuesday' : json_response['train']['days'][1]['runs'],
                'wednesday' : json_response['train']['days'][2]['runs'],
                'thursday' : json_response['train']['days'][3]['runs'],
                'friday' : json_response['train']['days'][4]['runs'],
                'saturday' : json_response['train']['days'][5]['runs'],
                'sunday' : json_response['train']['days'][6]['runs']
            })

            temp_station=self.env['station.station']
            for i in range(len(json_response['route'])):
                temp_station.create({
                    'name' : json_response['route'][i]['station']['name'],
                    'code' : json_response['route'][i]['station']['code']  
                })

            temp_class = self.env['train.class']
            temp_class.create({
                    'train_name' : json_response['train']['name'],
                    'train_number' : self.code,
                    'c_3A' :  json_response['train']['classes'][0]['available'],
                    'c_Sleeper' : json_response['train']['classes'][1]['available'],
                    'c_1A' : json_response['train']['classes'][2]['available'],
                    'c_2S' : json_response['train']['classes'][3]['available'],
                    'c_FC' : json_response['train']['classes'][4]['available'],
                    'c_2A' : json_response['train']['classes'][5]['available'],
                    'c_CC' : json_response['train']['classes'][6]['available'],
                    'c_3E' : json_response['train']['classes'][7]['available']
            })

            temp_route = self.env['route.route']
            temp_route.create({
                'from_station_id' : json_response['route'][0]['station']['code'],
                'to_station_id' : json_response['route'][len(json_response['route'])-1]['station']['code'],
                'arrival_time' : json_response['route'][len(json_response['route'])-1]['scharr'],
                'departure_time' : json_response['route'][0]['schdep'],
                'train_number' : str(self.code),
                'train_name' : json_response['train']['name'],
                'distance' : float(json_response['route'][len(json_response['route'])-1]['distance']),
                'fare' : 122.09
            })
        else:
            raise exceptions.ValidationError( "Not a Valid Train Number")



  

