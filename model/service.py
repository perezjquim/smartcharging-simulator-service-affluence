from nameko.events import EventDispatcher
from nameko.rpc import rpc

from model.exceptions import NotFound

import json

class ModelService:

    AFFLUENCE_CONFIG = {
        0 : 0,      #0h00 - 0h59
        1 : 0,      #1h00 - 1h59
        2 : 0,      #2h00 - 2h59        
        3 : 0,      #3h00 - 3h59
        4 : 0,      #4h00 - 4h59
        5 : 0,      #5h00 - 5h59
        6 : 0,      #6h00 - 6h59
        7 : 0,      #7h00 - 7h59
        8 : 10,    #8h00 - 8h59
        9 : 20,    #9h00 - 9h59
        10 : 17,  #10h00 - 10h59                                                                
        11 : 17,  #11h00 - 11h59
        12 : 8,    #12h00 - 12h59
        13 : 9,    #13h00 - 13h59
        14 : 7,    #14h00 - 14h59                                
        15 : 11,  #15h00 - 15h59
        16 : 10,  #16h00 - 16h59
        17 : 7,    #0h00 - 0h59
        18 : 3,    #0h00 - 0h59
        19 : 3,    #0h00 - 0h59
        20 : 3,    #0h00 - 0h59
        21 : 0,    #0h00 - 0h59
        22 : 1,    #0h00 - 0h59
        23 : 1,    #0h00 - 0h59
    }                                                                                        

    name = 'model_affluence'

    event_dispatcher = EventDispatcher()

    @rpc
    def get_affluence(self, hour_of_day):
        affluence = self.generate_affluence(hour_of_day)

        response = json.dumps({'affluence': affluence})
        return response

    def generate_affluence(self, hour_of_day):
        affluence = self.AFFLUENCE_CONFIG.get(hour_of_day)

        return affluence
