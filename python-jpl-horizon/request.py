#!/usr/bin/python

# python-jpl-horizon
#
# Written by: Siddarth Kalra (@siddarthkalra)

import json
import cgi, cgitb
#from jpl_horizon_connector.horizon import Horizon

def get_query_json(params):
    if params is None:
        return None
    elif not params["query"]:
        return None
    
    try:
        return json.loads(params["query"].value)
    except:
        return None

def is_json_obj_valid(json_obj):
    required_keys = ("version", "response_type", "query_type", "filters")
    query_types = ("id", "name")
    body_types = ("mb", "sb")
    response_types = ("json")
        
    result = {"success": False, "message": "Failed to validate request."}
    
    if not "horizons-api" in json_obj:
        result["message"] = "Failed. First level key 'horizons-api' missing."
        return result
        
    for r_key in required_keys:
        if not r_key in json_obj["horizons-api"]:
            result["message"] = "Failed. Second level key '%s' missing." % r_key
            return result
    
    result["success"] = True
    result["message"] = "Success"
    return result
       

if __name__ == "__main__":    
    
    params = cgi.FieldStorage()
    json = get_query_json(params)
    
    if json is None:
        print "Invalid json structure."
        sys.exit()

    json_validation = is_json_obj_valid(json)
    
    if not json_validation["success"]:
        print '''HTTP/1.1 501 Not Implemented
        Content-type: text/html
        
        '''
        sys.exit()
    
    #load json into 
    print('Content-type: application/json\r\n\r')
    print "Start Horizon<br/>"
    #horizon_data = Horizon()
    #print horizon.version()