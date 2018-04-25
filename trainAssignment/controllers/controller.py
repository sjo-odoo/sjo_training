import logging

from odoo import http

_logger = logging.getLogger(__name__)

class TrainC( http.Controller ):

   

    @http.route( '/hello', auth = 'public', website=True)
    def hello_world(self, **kwargs):
        train = http.request.env['route.route']
       # for i in range( len(train)) 
        #return str(train[0].from_station_id)+str(train[0].to_station_id)+str(train[0].arrival_time)+str(train[0].departure_time)+str(train[0].train_number)+str(train[0].distance)+str(train[0].fare)
        return http.request.render( 'trainAssignment.hello_world', { 'result' : train.search( [ ('from_station_id','=','SVDK') ] )} )

    # Odoo models map to database tables.

    @http.route( '/enquiry', auth = 'public', website = True)
    def enquiry(self, **kwargs):
        return http.request.render( 'trainAssignment.enquiry_page', {} )
    
    @http.route( '/result', auth = 'public', website = True)
    def result(self, **kwargs):
        temp_route = http.request.env['route.route']
        from_station = kwargs['source_station_name']
        to_station = kwargs['to_station_name']
        _logger.info("---------------------------------DATA----------------------"+str(from_station))
        _logger.info("---------------------------------DATA----------------------"+str(to_station))
        return http.request.render( 'trainAssignment.result_page', { 'result' : temp_route.search( [ ('from_station_id','=',from_station), ('to_station_id','=',to_station) ] ) })