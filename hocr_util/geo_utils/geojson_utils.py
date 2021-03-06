""" 
Utility functions to help with serialization to geojson via the geojson package. 
Django indendepent 
"""

import geojson

def get_geojson_feature(id, raw_bbox_string, properties_dict):
    """ Return a single geojson feature from a raw bbox string"""
    coords = raw_bbox_string.split()
    
    # Tesseract uses ints, but allow floats
    for i, val in enumerate(coords):
        coords[i] = float(val)
    # bbox order = # x0 y0 x1 y1
    
    bbox_json_obj = geojson.Polygon([[
        (coords[0], coords[1]), 
        (coords[0], coords[3]), 
        (coords[2], coords[3]), 
        (coords[2], coords[1]),
        (coords[0], coords[1])
    ]])
    return geojson.Feature(id, bbox_json_obj, properties=properties_dict)



def get_feature_collection(page):
    """ Return a geojson feature collection from the 'words' attribute of the page given. 
        NOTE: The word_num is used as the id. These are sometimes non-sequential. 
    """
    #print page['words']
    feature_array = []
    for i,word in enumerate(page['words']):
        # should line_num be required here? It's not supported by -bbox output... 
        word_properties = {'text':word['text'], 'line_num':word['line_num']}
        # should we instead rely on the the word number for the id? 
        feature_array.append(get_geojson_feature(i, word['bbox'], word_properties))
        
    featurecollection = geojson.FeatureCollection(feature_array)
    # todo: add page dimensions
    return geojson.dumps(featurecollection)