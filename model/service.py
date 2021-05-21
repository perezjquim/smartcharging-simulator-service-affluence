from nameko.events import EventDispatcher
from nameko.rpc import rpc

from model.exceptions import NotFound

import json

import tensorflow as tf

class ModelService:

    AFFLUENCE_CONFIG = { # average influx of passengers
        0 : 0,      #0h00 - 0h59
        1 : 0,      #1h00 - 1h59
        2 : 0,      #2h00 - 2h59        
        3 : 0,      #3h00 - 3h59
        4 : 0,      #4h00 - 4h59
        5 : 0,      #5h00 - 5h59
        6 : 0,      #6h00 - 6h59
        7 : 30.1369863013699,      #7h00 - 7h59
        8 : 14.5205479452055,    #8h00 - 8h59
        9 : 6.57534246575342,    #9h00 - 9h59
        10 : 38.9041095890411,  #10h00 - 10h59                                                                
        11 : 2.19178082191781,  #11h00 - 11h59
        12 : 7.3972602739726,    #12h00 - 12h59
        13 : 5.2054794520548,    #13h00 - 13h59
        14 : 4.10958904109589,    #14h00 - 14h59                                
        15 : 1.36986301369863,  #15h00 - 15h59
        16 : 3.56164383561644,  #16h00 - 16h59
        17 : 2.46575342465753,    #17h00 - 17h59
        18 : 0.821917808219178,    #18h00 - 18h59
        19 : 75.6164383561644,    #19h00 - 19h59
        20 : 34.7945205479452,    #20h00 - 20h59
        21 : 31.2328767123288,    #21h00 - 21h59
        22 : 0,    #22h00 - 22h59
        23 : 0,    #23h00 - 23h59
    }     

    AFFLUENCE_STDDEV = 17.8753449996882
                                                                                

    name = 'model_energysim_travel_affluence'

    event_dispatcher = EventDispatcher( )

    @rpc
    def get_affluence( self, hour_of_day ):
        hour_of_day_int = int( hour_of_day )
        affluence = self.generate_affluence( hour_of_day_int )
        response = json.dumps( { 'affluence': affluence } )

        return response

    def generate_affluence( self, hour_of_day ):
        average_affluence = ModelService.AFFLUENCE_CONFIG.get( hour_of_day )
        # if average_affluence==0:
        #     return 0

        shape = [ 1,1 ]
        min_affluence = max(0,average_affluence - ModelService.AFFLUENCE_STDDEV) 
        max_affluence = average_affluence + ModelService.AFFLUENCE_STDDEV

        tf_random = tf.random_uniform(
                shape=shape,
                minval=min_affluence,
                maxval=max_affluence,
                dtype=tf.float32,
                seed=None,
                name=None
        )
        tf_var = tf.Variable( tf_random )

        tf_init = tf.global_variables_initializer( )
        tf_session = tf.Session( )
        tf_session.run( tf_init )

        tf_return = tf_session.run( tf_var )
        affluence = float( tf_return[ 0 ][ 0 ] )

        return affluence