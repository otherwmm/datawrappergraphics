import requests
import json
import os
import sys
import pandas as pd
import geopandas
import datetime
import logging
import urllib.error
import numpy
from geojson import Feature
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
from datawrappergraphics.icons import dw_icons


# There are two opens when creating a new DatawrapperGraphic object:
    # 
    #   1. You can create a brand new chart by specifying no chart_id and no copy_id. This is not recommended but can be used to create a large number of charts en-mass,
    #   and then save their info into a csv or something.
    # 
    #   2. You can specify a copy_id, and a new chart will be created by copying that chart. This is also not recommended but can be used for various purposes.
    #
    #   3. You can specify a chart that is already made that you want to update. This is the easiest way - copy another chart in the Datawrapper app and then
    #   use that chart_id.

class DatawrapperGraphic:
    
    # The CHART_ID is a unique ID that can be taken from the URL of datawrappers. It's required to use the DW api.
    global CHART_ID
    
    # Holds the chart's metadata when the graphic is instantiated.
    global metadata
    
    # Represents the data that is uploaded or will be uploaded to the graphic.
    global dataset
    
    # What OS is the script running on? This effects timestamping as unix uses UTC.
    global os_name
    
    # Token to authenticate to Datawrapper's API.
    global DW_AUTH_TOKEN
    
    # Path that the script is running from using this module.
    global path
    
    # Name of the script currently running using this module.
    global script_name
    
    def __init__(self, chart_id: str = None, copy_id: str = None, auth_token: str = None, folder_id: str = None):
        
        # Set OS name (see global DatawrapperGraphic variables)
        self.os_name = os.name
        
        self.script_name = os.path.basename(sys.argv[0]).replace(".py", "").replace("script-", "")
        
        self.path = os.path.dirname(sys.argv[0]) 
        
        self.auth(token=auth_token)
        
        
        
        # Define common headers for all the below options for instantiating Datawrapper graphics.
        headers = {
                "Accept": "*/*",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.DW_AUTH_TOKEN}"
            }
        
        # If no chart ID is passed, and no copy id is passed, we create a new chart from scratch.
        if chart_id == None and copy_id == None:
            
            print(f"No chart specified. Creating new chart...")
            
            # If a folder is specified in which to create the chart, handle that here.
            if folder_id:
                payload = {"folderId": folder_id}
                
            # Otherwise, just send an empty payload.    
            else:
                payload = {}
            
            response = requests.post(f"https://api.datawrapper.de/v3/charts/", json=payload, headers=headers)
            chart_id = response.json()["publicId"]

            print(f"New chart created with id {chart_id}")
            
            self.CHART_ID = chart_id
        
        # If we want to make a copy of a graphic to create the new graphic.    
        elif chart_id == None and copy_id != None:
            
            print(f"No chart specified. Copying chart with ID: {copy_id}...")
            
            response = requests.post(f"https://api.datawrapper.de/v3/charts/{copy_id}/copy", headers=headers)
            chart_id = response.json()["publicId"]
            
            print(f"New chart ({chart_id}) created as a copy of {copy_id}.")
            
            self.CHART_ID = chart_id
            
        # If we specify a chart id and no copy id, then there is a chart already made that we're altering.    
        elif chart_id != None and copy_id == None:
            
            self.CHART_ID = chart_id
        
        # Throw exception if both copy id and chart id are input.
        elif chart_id != None and copy_id != None:
            raise Exception(f"Please specify either a chart_id or a copy_id, but not both.")
        
        self.metadata = self.get_metadata()

    
    
    
    
    
    def get_metadata(self):
        
        headers = {
            "Accept": "*/*",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.DW_AUTH_TOKEN}"
        }
        
        r = requests.get(f"https://api.datawrapper.de/v3/charts/{self.CHART_ID}", headers=headers)
        
        metadata = r.json()
        
        if r.ok: return metadata
        else: raise Exception(f"Couldn't update metadata. Response: {r.reason}")
        
        
    
    
    
    
    
    
    def set_metadata(self, metadata: dict = None):
        
        if metadata is None:
            metadata = self.metadata
        
        headers = {
            "Accept": "*/*",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.DW_AUTH_TOKEN}"
        }
        
        template = {'thumbnails': {
                'full': '//img.datawrapper.de/nSHo0/b31913d1ae7339725e20821d825ef7f5/full.png',
                'plain': '//img.datawrapper.de/nSHo0/b31913d1ae7339725e20821d825ef7f5/plain.png'},
               'publicId': 'nSHo0',
               'language': 'en-US',
               'theme': 'cbc',
               'authorId': 282719,
               'createdAt':'2022-05-30T17:04:21.000Z',
               'externalData': None,
               'forkable': False,
               'forkedFrom': '83uUC',
               'id': 'nSHo0',
               'isFork': False,
               'lastEditStep': 5,
               'lastModifiedAt': '2022-06-05T14:16:31.000Z',
               'metadata': {
                   'data': {
                       'transpose': False,
                       'vertical-header': True,
                       'horizontal-header': True,
                       'json': True
                       },
                   'describe': {
                       'source-name': 'U.S. National Hurricane Center',
                       'source-url': '',
                       'intro': 'Windspeed is currently measured at <b>96 km/h</b>.',
                       'byline': 'Dexter McMillan',
                       'aria-description': '',
                       'number-format': '-',
                       'number-divisor': 0,
                       'number-append': '',
                       'number-prepend': ''
                       },
                   'visualize': {
                       'highlighted-series': [],
                       'highlighted-values': [],
                       'view': {
                           'fit': {
                               'top': [-67.98585335442425, 50.960484198569304],
                               'left': [-102.04827196201292, 32.34364955620653],
                               'right': [-33.923434746835596, 32.34364955620653],
                               'bottom': [-67.98585335442425, 8.97056056217815]
                               },
                           'zoom': 3.5,
                           'pitch': 0,
                           'center': [-67.98585335442522, 32.34364955620599],
                           'height': 74, 'bearing': 0
                           },
                       'scale': False,
                       'style': 'dw-light',
                       'locked': False,
                       'upload': {
                           'maxSize': 2000000, 'maxMarkers': 100
                           },
                       'x-grid': 'on',
                       'compass': False,
                       'markers': None,
                       'sharing': {
                           'auto': True, 'enabled': False
                           },
                       'mapLabel': True,
                       '_last_tab': 'markers',
                       'addRegion': False,
                       'scaleUnit': 'metric',
                       'publish': {
                           'embed-width': 1096,
                           'embed-height': 998,
                            'embed-codes': {
                                'embed-method-iframe': '<iframe title="TEST: Tracking tropical storm Alex" aria-label="Locator maps" id="datawrapper-chart-nSHo0" src="https://datawrapper.dwcdn.net/nSHo0/284/" scrolling="no" frameborder="0" style="border: none;" width="1096" height="998"></iframe>',
                                'embed-method-responsive': '<iframe title="TEST: Tracking tropical storm Alex" aria-label="Locator maps" id="datawrapper-chart-nSHo0" src="https://datawrapper.dwcdn.net/nSHo0/284/" scrolling="no" frameborder="0" style="width: 0; min-width: 100% !important; border: none;" height="998"></iframe><script type="text/javascript">!function(){"use strict";window.addEventListener("message",(function(e){if(void 0!==e.data["datawrapper-height"]){var t=document.querySelectorAll("iframe");for(var a in e.data["datawrapper-height"])for(var r=0;r<t.length;r++){if(t[r].contentWindow===e.source)t[r].style.height=e.data["datawrapper-height"][a]+"px"}}}))}();\n</script>'
                                }
                            },
                       'annotate': {
                           'notes': 'Last updated on June 5, 2022 at 10:16 a.m.'
                           },
                       'custom': {},
                       'json_error': None},
                   'organizationId': 'cbc',
                   'publicUrl': 'https://datawrapper.dwcdn.net/nSHo0/284/',
                   'publicVersion': 284,
                   'publishedAt': '2022-06-05T14:16:31.000Z',
                   'title':
                       'TEST: Tracking tropical storm Alex',
                       'type': 'locator-map',
                       'customFields': {},
                       'folderId': 105625,
                       'author': {
                           'name': 'Dexter McMillan',
                           'email': 'dexter.mcmillan@cbc.ca'
                           },
                       'url': '/v3/charts/nSHo0'
                       }
        }

        r = requests.patch(f"https://api.datawrapper.de/v3/charts/{self.CHART_ID}", headers=headers, data=json.dumps(metadata))
        
        self.metadata = r.json()
        
        if r.ok: print(f"SUCCESS: Metadata updated.")
        else: raise Exception(f"Couldn't update metadata. Response: {r.reason}")
        
        return self
    
    
    
    
    
    
    # Add the chart's headline.
    def head(self, string: str):
    
        # Define headers for headline upload.
        headers = {
            "Accept": "*/*",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.DW_AUTH_TOKEN}"
        }
        
        # Take the string input as a parameter and put it into a payload object. Then convert to JSON string.
        data = {"title": string}
        data = json.dumps(data)
        
        r = requests.patch(f"https://api.datawrapper.de/v3/charts/{self.CHART_ID}", headers=headers, data=data)
        
        if r.ok: print(f"SUCCESS: Chart head added.")
        else: raise Exception(f"ERROR: Chart head was not added. Response: {r.text}")
        
        return self
    
    
    
    
    
    
    

    
    def deck(self, deck: str):
        
        headers = {
            "Accept": "*/*", 
            "Authorization": f"Bearer {self.DW_AUTH_TOKEN}"
            }
        
        payload =  {
            "metadata": {
                "describe": {
                    "intro": deck,
                },
            }
        }
        
        r = requests.patch(f"https://api.datawrapper.de/v3/charts/{self.CHART_ID}", headers=headers, data=json.dumps(payload))
        
        if r.ok: print(f"SUCCESS: Chart deck added.")
        else: raise Exception(f"ERROR: Chart deck was not added. Response: {r.text}")
        
        # Update the object's metadat representation.
        self.metadata = r.json()
        
        return self
    
    
    
    
    
    
    
    
    
    ## Adds a timestamp to the "notes" section of your chart. Also allows for an additional note string that will be added before the timestamp.
    
    def footer(self, source: str = None, byline:str = "Dexter McMillan", note: str = "", timestamp: bool = True):
        
        today = datetime.datetime.today()
        
        if self.os_name == "posix":
            today = today - datetime.timedelta(hours=4)
        
        # Get day and time strings for use in the footer timestamp.
        time = today.strftime('%I:%M') + " " + ".".join(list(today.strftime('%p'))).lower() + "."
        day = today.strftime('%B %d, %Y')
        
        # Use day and time values and create the string we put into the footer as a timestamp.
        timestamp_string = f"Last updated on {day} at {time}".replace(" 0", " ")
        
        headers = {
            "Accept": "*/*",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.DW_AUTH_TOKEN}"
        }
        
        # This is a template object for the structure of the patch payload that Datawrapper API accepts.
        data =  {
            "metadata": {
                "describe": {
                    "source-name": source,
                    "byline": byline,
                },
                "annotate": {
                    "notes": f"{note} {timestamp_string if timestamp else ''}".strip(),
                },
            }
        }

        # Make the HTTP request to update metadata.
        r = requests.patch(f"https://api.datawrapper.de/v3/charts/{self.CHART_ID}", headers=headers, data=json.dumps(data))
        
        if r.ok: print(f"SUCCESS: Chart footer (byline, notes, and source) built and added.")
        else: raise Exception(f"ERROR: Couldn't build chart footer. Response: {r.reason}")
        
        # Update the object's metadat representation.
        self.metadata = r.json()
        
        return self
    
    
    
    
    
    
    
    
    
    def publish(self):

        headers = {
            "Accept": "*/*", 
            "Authorization": f"Bearer {self.DW_AUTH_TOKEN}"
            }

        r = requests.post(f"https://api.datawrapper.de/v3/charts/{self.CHART_ID}/publish", headers=headers)
        
        if r.ok: print(f"SUCCESS: Chart published!")
        else: raise Exception(f"ERROR: Chart couldn't be published. Response: {r.reason}")
        
        return self
    
    
    
    
    
    
    # This method authenticates to Datawrapper and returns the token for accessing the DW api.
    def auth(self, token: str = None):
        
        if token != None:
            DW_AUTH_TOKEN = token
        else:
            # On a local machine, it will read the auth.txt file for the token.
            try:
                with open('./auth.txt', 'r') as f:
                    DW_AUTH_TOKEN = f.read().strip()
            # If this is run using Github actions, it will take a secret from the repo instead.
            except FileNotFoundError:
                try: DW_AUTH_TOKEN = os.environ['DW_AUTH_TOKEN']
                except: raise Exception(f"No auth.txt file found, and no environment variable specified for DW_AUTH_TOKEN. Please add one of the two to authenticate to Datawrapper's API.")
        
        self.DW_AUTH_TOKEN = DW_AUTH_TOKEN    
        return self 
    

    
    
    
    
    # Moves your chart to a particular folder ID.
    def move(self, folder_id: str):
        
        headers = {
            "Accept": "*/*", 
            "Authorization": f"Bearer {self.DW_AUTH_TOKEN}"
            }
        
        payload = {
            "ids": [self.CHART_ID],
            "patch": {"folderId": folder_id}
            }

        r = requests.patch(f"https://api.datawrapper.de/v3/charts", json=payload, headers=headers)
        
        if r.ok: print(f"SUCCESS: Chart moved to folder ID {folder_id}!")
        else: raise Exception(f"ERROR: Chart couldn't be moved. Response: {r.reason}")
        
        return self
    
    
    
    
    
    
    def delete(self):
        
        logging.warning(f"Deleting chart with ID {self.CHART_ID}!")
        
        headers = {
            "Accept": "*/*", 
            "Authorization": f"Bearer {self.DW_AUTH_TOKEN}"
            }

        r = requests.delete(f"https://api.datawrapper.de/v3/charts/{self.CHART_ID}", headers=headers)
        
        if r.ok: print(f"SUCCESS: Chart published!")
        else: raise Exception(f"ERROR: Chart couldn't be deleted. Response: {r.reason}")
        
        return self
    
    
    
    
    def export(self, format: str = "png", filename: str = "export.png"):
        
        file_path = self.path + filename
        
        headers = {
            "Accept": "image/png", 
            "Authorization": f"Bearer {self.DW_AUTH_TOKEN}"
            }

        export_chart_response = requests.get(f"https://api.datawrapper.de/v3/charts/{self.CHART_ID}/export/{format}?unit=px&mode=rgb&plain=false&scale=1&zoom=2&download=true&fullVector=false&ligatures=true&transparent=false&logo=auto&dark=false", headers=headers)
            
        
        if export_chart_response.ok:
            print(f"SUCCESS: Chart with ID {self.CHART_ID} exported and saved!")
            
            with open(file_path, "wb") as response:
                response.write(export_chart_response.content)
                
        else: raise Exception(f"ERROR: Chart couldn't be exported as {format}. Response: {export_chart_response.reason}")
        
        return self

# The Chart class defines methods and variables for uploading data to datawrapper charts (scatter plots, tables etc).
# Use this class to create a new, copy, or to manage a currently existing Datawrapper chart (ie. not a map!).
class Chart(DatawrapperGraphic):
    
    script_name = os.path.basename(sys.argv[0]).replace(".py", "").replace("script-", "")
    
    def __init__(self, *args, **kwargs):
        
        super(Chart, self).__init__(*args, **kwargs)
    
    def data(self, data: pd.DataFrame):
        
        headers = {
            "Accept": "*/*",
            "Content-Type": "text/csv",
            "Authorization": f"Bearer {self.DW_AUTH_TOKEN}"
        }

        payload = data.to_csv()
        
        r = requests.put(f"https://api.datawrapper.de/v3/charts/{self.CHART_ID}/data", headers=headers, data=payload)

        if r.ok: print(f"SUCCESS: Data added to chart.")
        else: raise Exception(f"Chart data couldn't be added. Response: {r.reason}")
        
        return self
    




# This class defines methods and variables for Datawrapper locator maps.
# It is also extended by the hurricane map class below.
class Map(DatawrapperGraphic):
    
    # Script_name variable is used to pull the right icon templates from the assets folder, and is set on init.
    global script_name
    global icon_list
    
    def __init__(self, *args, **kwargs):
        super(Map, self).__init__(*args, **kwargs)
        
        self.icon_list = dw_icons
     
     
     
     
     
     
    # This method handles the majority of the heavy lifting for map data.
    # In essence, it converts either a pd.DataFrame or a geopandas.GeoDataFrame to a GEOJson object, then
    # replaces values in a template with custom values specified in the dataframe.
    def data(self, input_data: pd.DataFrame | geopandas.GeoDataFrame, append: str = None):
        
        # Define a list of marker types that are allowed.
        allowed_marker_type_list = ["point", "area"]
        
        # Define a list of icon types that are allowed (ie those that are defined in the icons.py file.)
        allowed_icon_list = [key for key, value in self.icon_list.items()]
        
        # Append "area" to this list. These icons are handled a bit differently so there is no icon defined for them.
        allowed_icon_list.append("area")
        
        # New list for storing the altered geojson.
        new_features = []
        
        if isinstance(input_data, geopandas.GeoDataFrame):
            input_data = input_data.to_crs("EPSG:4326")
        
        for i, feature in input_data.iterrows():
            
            # Check if a marker type is specified. If it's not, we'll try to infer the type based on the presence of lat/lng columns or geometry columns (area columns have geometry
            # point columns have lat/lng.
            marker_type = feature["type"]
            
            # Check to make sure the marker type we specified is in the list of allowed marker types.
            if marker_type not in allowed_marker_type_list:
                raise Exception(f"It looks like you haven't provided a valid marker type. Please ensure the value is one of: {', '.join(allowed_marker_type_list)}.")
            
            # Load the template feature object depending on the type of each marker (area or point). Throw an error if the file can't be found.
            if marker_type == "point":
                new_feature = {
                "type": "point",
                "title": feature["title"] if "title" in input_data and feature["title"] is not numpy.nan else "",
                "icon": self.icon_list[feature["icon"]] if "icon" in input_data and feature["icon"] is not numpy.nan else self.icon_list["circle"],
                "scale": feature["scale"] if "scale" in input_data and feature["scale"] is not numpy.nan else 1.1,
                "textPosition": True,
                "markerColor": feature["markerColor"] if "markerColor" in input_data and feature["markerColor"] is not numpy.nan else "#C42127",
                "markerSymbol": feature["markerSymbol"] if "markerSymbol" in input_data and feature["markerSymbol"] is not numpy.nan else "",
                "markerTextColor": "#333333",
                "anchor": feature["anchor"] if "anchor" in input_data and feature["anchor"] is not numpy.nan else "middle-left",
                "offsetY": 0,
                "offsetX": 0,
                "labelStyle": "plain",
                "text": {
                    "bold": False,
                    "color": "#333333",
                    "fontSize": 14,
                    "halo": "#f2f3f0",
                    "italic": False,
                    "space": False,
                    "uppercase": False
                },
                "class": "",
                "rotate": 0,
                "visible": feature["visible"] if "visible" in input_data and feature["visible"] is not numpy.nan else True,
                "locked": False,
                "preset": "-",
                "visibility": {
                    "desktop": feature["visible"] if "visible" in input_data and feature["visible"] is not numpy.nan else True,
                    "mobile": feature["visible"] if "visible" in input_data and feature["visible"] is not numpy.nan else True,
                },
                "tooltip": {
                    "text": feature["tooltip"] if "tooltip" in input_data and feature["tooltip"] is not numpy.nan else ""
                },
                "connectorLine": {
                    "enabled": False,
                    "arrowHead": "lines",
                    "type": "curveRight",
                    "targetPadding": 3,
                    "stroke": 1,
                    "lineLength": 0
                },
                "coordinates": [feature["longitude"], feature["latitude"]]
                }
                
            
                
            elif marker_type == "area":
                
                new_feature = {
                    "type": "area",
                    "title": feature["title"] if "title" in input_data and feature["title"] is not numpy.nan else "",
                    "visible": feature["visible"] if "visible" in input_data and feature["visible"] is not numpy.nan else True,
                    "fill": feature["fill"] if "fill" in input_data and feature["fill"] is not numpy.nan and isinstance(feature["fill"], bool) else True,
                    "stroke": feature["stroke"] if "stroke" in input_data and feature["stroke"] is not numpy.nan and isinstance(feature["fill"], bool) else True,
                    "exactShape": False,
                    "highlight": False,
                    "markerColor": feature["markerColor"] if "markerColor" in input_data and feature["markerColor"] is not numpy.nan else "#C42127",
                    "properties": {
                        "fill": feature["fill"] if "fill" in input_data and feature["fill"] is not numpy.nan and isinstance(feature["fill"], str) else "#C42127",
                        "fill-opacity": feature["fill-opacity"] if "fill-opacity" in input_data and feature["fill-opacity"] is not numpy.nan else 1.0,
                        "stroke": feature["stroke"] if "stroke" in input_data and feature["stroke"] is not numpy.nan and isinstance(feature["fill"], str) else "#000000",
                        "stroke-width": 1,
                        "stroke-opacity": 1.0,
                        "stroke-dasharray": feature["stroke-dasharray"] if "stroke-dasharray" in input_data and feature["stroke-dasharray"] is not numpy.nan else "100000",
                        "pattern": "solid",
                        "pattern-line-width": 2,
                        "pattern-line-gap": 2
                    },
                    "icon": {"id": "area",
                        "path": "M225-132a33 33 0 0 0-10 1 38 38 0 0 0-27 28l-187 798a39 39 0 0 0 9 34 37 37 0 0 0 33 12l691-93 205 145a38 38 0 0 0 40 2 38 38 0 0 0 20-36l-54-653a38 38 0 0 0-17-28 38 38 0 0 0-32-5l-369 108-274-301a39 39 0 0 0-28-12z",
                        "horiz-adv-x": 1000,
                        "scale": 1.1,
                        "outline": "2px"},
                    "visibility": {
                        "desktop": feature["visible"] if "visible" in input_data and feature["visible"] is not numpy.nan else True,
                        "mobile": feature["visible"] if "visible" in input_data and feature["visible"] is not numpy.nan else True,
                    },
                    "feature": {
                        "type": "Feature",
                        "properties": {},
                        "geometry": Feature(geometry=feature["geometry"], properties={})["geometry"]
                        }
                }
            
            
            
            new_features.append(new_feature)

        
        # If there are other shapes to be added (ie. highlights of provinces, etc.) then this will use a naming convention to grab them from the shapes folder.
        # Check if there are any extra shapes to add.
        # TODO allow users to enter their own assets path.
        
        if append:
            
            # Open the shape file.
            with open(append, 'r') as f:
                extra_shapes = json.load(f)
                
                # If there is only one object and it's not in a list, make it a list.
                if type(extra_shapes) != list:
                    extra_shapes = [extra_shapes]
                    
                # Iterate through the list and add it to our markers list.
                for shape in extra_shapes:
                    new_features.append(shape)
        
        # Datawrapper uses a convention to ID features following m0, m1, m2 etc. Add these in once we have all the markers in a list so there are no duplicates.
        for i, feature in enumerate(new_features):
            feature["id"] = "m" + str(i)
            
        with open(f"./markers-{self.script_name}.json", 'w') as f:
                json.dump(new_features, f)
            
        # Change layout of the markers to match what Datawrapper likes to receive.    
        payload = {"markers": new_features}
        payload = json.dumps(payload)
        
        # Make the HTTP request to the Datawrapper API to upload the data.
        headers = {"Authorization": f"Bearer {self.DW_AUTH_TOKEN}"}
        r = requests.put(f"https://api.datawrapper.de/v3/charts/{self.CHART_ID}/data", headers=headers, data=payload)

        if r.ok: print(f"SUCCESS: Data added to chart.")
        else: raise Exception(f"ERROR: Chart data couldn't be added. Response: {r.reason}")
        
        return self
    
    
    
    
    
    
    
    
    
    # This method is mostly used for testing and debugging. It can be called to save the data that was just uploaded to a chart
    # so it can be easily inspected.
    def get_markers(self, save: bool = False):
        
        headers = {
            "Accept": "text/csv",
            "Authorization": f"Bearer {self.DW_AUTH_TOKEN}"
            }
        
        response = requests.get(f"https://api.datawrapper.de/v3/charts/{self.CHART_ID}/data", headers=headers)
        markers = response.json()["markers"]
        
        if save:
            with open(f"{self.path}/markers-{self.script_name}.json", 'w') as f:
                json.dump(markers, f)
                
        return markers
    
    



# The StormMap class is a special extension of the Map class that takes data from the NOAA and turns
# it into a hurricane map with standard formatting. It takes one input: the storm ID of the hurricane
# or tropical storm that can be taken from the NOAA's National Hurricane Center.

# The NOAA stores this data in at least two separate zipfiles that need to be pulled in and processed.
class StormMap(Map):
    
    # Some variables that we want to be able to access when the class is instantiated.
    global storm_id
    global windspeed
    global storm_name
    global storm_type
    
    # The url from which the data originates. An arg for creating a StormMap.
    global xml_url
    
    
    
    def __init__(self, storm_id: str, xml_url: str, chart_id: str = None, copy_id: str = None):
        
        # Set storm id from the input given to the class constructor.
        self.storm_id = storm_id
        self.xml_url = xml_url
        
        super().__init__(chart_id, copy_id)
    
    
    
    # This method gets the shapefile from the NOAA, which is in a zipfile.
    def __get_shapefile(self, filename, layer):
        filename = filename.lower()
        
        # Download and open the zipfile.
        try: resp = urlopen(filename)
        except urllib.error.HTTPError: raise Exception(f"Resource is forbidden. It's likely the shapefile for probable path is not publicly accessible.")
        
        # List out names of files in the zipfile.
        files = ZipFile(BytesIO(resp.read())).namelist()
        
        # Put it into a dataframe for easy iteration.
        files = pd.Series(files)

        file_name = files[files.str.contains(layer)].to_list()[0].replace(".shp", "")
        
        # Returns a geopandas df.
        return geopandas.read_file(filename, layer=file_name)
    
    
    
    
    # This function gets the total path of the hurricane, which is stored in a separate zip file entirely from the others.
    # TODO clean up this function ugh.
    def __total_path(self, storm_id):
        
        # Get the best track zipfile that contains the shapefile about the historical path of the storm.
        best_track_zip = f"https://www.nhc.noaa.gov/gis/best_track/{storm_id}_best_track.zip"
        
        # Pull the shapefile out of this zip file.
        points = self.__get_shapefile(best_track_zip, "pts.shp$")

        # points = points[points["STORMNAME"] == self.storm_name.upper()]
        points = points.rename(columns={"LAT": "latitude", "LON": "longitude"})

        points["longitude"] = points["geometry"].x.astype(float)
        points["latitude"] = points["geometry"].y.astype(float)
        points = points.drop(columns=["geometry"])
        
        for df in [points, line]:
            df["STORMTYPE"] = points["STORMTYPE"].replace({"TS": "S", "HU": "H", "TD": "D"})
            df = df[df["STORMTYPE"].isin(["D", "H", "S"])]
        
        points["type"] = "point"
        points["icon"] = "circle"
        points["markerSymbol"] = points["STORMTYPE"]
        points["markerSymbol"] = points["markerSymbol"].str.replace("M", "H")
        points.loc[~points["markerSymbol"].isin(["D", "S", "H"]), "markerSymbol"] = ""
        points["markerColor"] = points["markerSymbol"].replace({"H": "#e06618"})
        points.loc[points["markerColor"] != "H", "markerColor"] = "#567282"
        points["scale"] = 1.1
        
        line = self.__get_shapefile(best_track_zip, "lin.shp$")
        
        line["stroke"] = "#000000"
        line["type"] = "area"
        line["stroke-dasharray"] = "1,2.2"
        line["fill-opacity"] = 0.0
        
        # line = line[line["SS"] >= 1]
        
        line = line.dissolve(by='STORMNUM')
        
        return pd.concat([line])
    
    # This method is a custom version of Map's data() method, which is then called after calling this.
    def data(self):
        
        # Get storm metadata.
        metadata = pd.read_xml(self.xml_url, xpath="/rss/channel/item[1]/nhc:Cyclone", namespaces={"nhc":"https://www.nhc.noaa.gov"})
        
        # Split the marker for the center of the storm into latitude and longitude values.
        metadata["latitude"] = pd.Series(metadata.at[0, "center"].split(",")[0].strip()).astype(float)
        metadata["longitude"] = pd.Series(metadata.at[0, "center"].split(",")[1].strip()).astype(float)
        
        # Save windspeed in object variables.
        self.windspeed = metadata.at[0, "wind"].replace(" mph", "")
        self.windspeed = int(int(self.windspeed) * 1.60934)
        
        # Save name of storm in object variables.
        self.storm_name = metadata.at[0, "name"]
        
        # Save type of storm in object variables.
        self.storm_type = metadata.at[0, "type"]
        
        # Pull in data from NOAA five day forecast shapefile.
        five_day_latest_filename = f"https://www.nhc.noaa.gov/gis/forecast/archive/{self.storm_id}_5day_latest.zip"
        
        # Get points layer from five day forecast shapefile.
        points = self.__get_shapefile(five_day_latest_filename, "5day_pts.shp$")
        
        # Start by processing the points shapefile
        points["longitude"] = points["geometry"].x.astype(float)
        points["latitude"] = points["geometry"].y.astype(float)
        points = points.drop(columns=["geometry"])
        
        points["DATELBL"] = pd.to_datetime(points["DATELBL"]).apply(lambda x: x.tz_localize("America/Chicago"))
        points["DATELBL"] = points["DATELBL"].dt.tz_convert('US/Eastern')
        points["type"] = "point"
        points["icon"] = "circle"
        points["fill"] = "#C42127"
        points["title"] = points['DATELBL'].dt.strftime("%b %e") + "<br>" + points['DATELBL'].dt.strftime("%I:%M %p")
        points["title"] = points["title"].str.replace("<br>0", "<br>")
        points["scale"] = 1.1
        points["markerSymbol"] = points["DVLBL"]
        points["markerColor"] = points["markerSymbol"].replace({"D": "#567282", "S": "#567282", "H": "#e06618"})
        
        points.loc[points["DVLBL"] == "D", "storm_type"] = "Depression"
        points.loc[points["DVLBL"] == "H", "storm_type"] = "Hurricane"
        points.loc[points["DVLBL"] == "S", "storm_type"] = "Storm"
        
        points["tooltip"] = "On " + points['DATELBL'].dt.strftime("%b %e") + " at " + points['DATELBL'].dt.strftime("%I:%M %p").str.replace("$0", "", regex=True) + " EST, the storm is projected to be classified as a " + points["storm_type"].str.lower() + "."
        points["tooltip"] = points["tooltip"].str.replace(" 0", " ")
        
        # Get center line layer from five day forecast shapefile.
        centre_line = self.__get_shapefile(five_day_latest_filename, "5day_lin.shp$")
        
        # Define properties unique to centre line.
        centre_line["stroke"] = "#000000"
        centre_line["fill-opacity"] = 0.0
        centre_line["stroke-opacity"] = 0.5
        centre_line["type"] = "area"
        
        # Get probable path layer from five day forecast shapefile.
        probable_path = self.__get_shapefile(five_day_latest_filename, "5day_pgn.shp$")
        
        # Define properties unique to probable path shape.
        probable_path["fill"] = "#6a3d99"
        probable_path["stroke"] = "#6a3d99"
        probable_path["markerColor"] = "#6a3d99"
        probable_path["fill-opacity"] = 0.3
        probable_path["stroke-opacity"] = 0.0
        probable_path["title"] = "Probable path"
        
        # Define some common style points for the centre line and the probable path.
        for df in [centre_line, probable_path]:
        
            df["type"] = "area"
            df["icon"] = "area"
        
        # Call the method that returns our total path information. This holds historical info about where the hurricane has been.
        total_path = self.__total_path(storm_id=self.storm_id)
        
        # Concatenate all our dataframes into one large dataframe so we can upload it.
        all_shapes = pd.concat([centre_line, probable_path, points, total_path])
        
        # Filter out all the columsn we don't care about keeping.
        # TODO remove this, as the new data() method should be able to do this without specifying.
        all_shapes = all_shapes[["markerColor", "fill", "fill-opacity", "stroke", "stroke-opacity", "type", "icon", "latitude", "longitude", "geometry", "title", "tooltip", "scale", "markerSymbol", "stroke-dasharray"]]
        
        
        # Fill any null values in latitude and longitude columns.
        # TODO do we need these fillna lines?
        all_shapes["latitude"] = all_shapes["latitude"].fillna("")
        all_shapes["longitude"] = all_shapes["longitude"].fillna("")
          
        # I've commented the next line out because I don't think I need it with the new data() method structure.  
        # all_shapes["stroke-dasharray"] = all_shapes["stroke-dasharray"].fillna("100000")

        # Save as the object's dataset.
        self.dataset = all_shapes
        self.dataset.to_clipboard()
        
        # Pass the dataset we've just prepped into the super's data method.
        return super(self.__class__, self).data(self.dataset)