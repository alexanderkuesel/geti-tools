## Alexander Kuesel
## Contains functions I have written to help parse through Geti outputs, be it prediction results or others.
## To get the dictionary from Geti, use the following commands:
##    labels = prediction.get_labels() ##get labels only
##    label_dict = prediction.to_dict() #create a dictionary

import numpy as np
from geti_sdk.deployment import Deployment
from geti_sdk.utils import show_image_with_annotation_scene

class GetiParse:
    """
    This class contains functions that take the labels dictionary as an input and return relevant results
    """
    def __init__(self, label_dict):
        self.label_dict = label_dict
    
    def get_shapes(self):
        """
        Takes label_dict as input and returns shapes with basic properties
        Returns dict with {"Label Name ":"Shape Type"}
        """
        out_dict = {}
        for annotation in self.label_dict['annotations']:
            for label in annotation['labels']:
                # Create new entry where key = name and value = shape type
                out_dict[label['name']] = annotation['shape']['type']
                
        return out_dict
    
    def get_rectangle(self):
        """
        Get coordinates of rectangle such that:
        (x1,y2)---(x2,y2)
        |               |
        |               |
        (x1, y1)---(x2,y1)
        
        Can specify ['x1'] at end to just get that if wanted.  
        Only accepts 1 rectangle for label (at the moment)
        
        """
        out_dict = {}
        for annotation in self.label_dict['annotations']:
            for label in annotation['labels']:
                # iterate to make a unique id for each instance
                if annotation['shape']['type'] == 'RECTANGLE':
                    # create a new entry for each rectangle annotation and get shape dimensions
                    label = label['name']
                    left_x = annotation['shape']['x']
                    bot_y = annotation['shape']['y']
                    right_x = left_x + annotation['shape']['width'] #actual rightmost x value
                    top_y = bot_y + annotation['shape']['height'] #actual highest y value
                    
                    # Create label entry (there should only be one label per object)
                    if label not in out_dict:
                        out_dict[label] = {}

                    out_dict[label]['x1'] = left_x
                    out_dict[label]['y1'] = bot_y
                    out_dict[label]['x2'] = right_x
                    out_dict[label]['y2'] = top_y
                  
        return out_dict
    
    def get_polygons(self):
        """
        Get coordinates of polygon by just getting max, average and slope. 
        Currently just interested in max        
        """
        out_dict = {}
        for annotation in self.label_dict['annotations']:
            for label in annotation['labels']:

                if annotation['shape']['type'] == 'POLYGON':
                    # create a new entry for each rectangle annotation and get shape dimensions
                    label = label['name']
                    # get amount of coordinate pairs to determine largest annotation area
                    #annot_size = len(annotation['shape']['points'])
                    
                    # Create label entry
                    if label not in out_dict:
                        out_dict[label] = {}                    
                    out_dict[label] = annotation['shape']['points']
                    
                    
        return out_dict
                    
                    
                    
                
