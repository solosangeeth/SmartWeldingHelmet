import urequests
import thingspeakconfig

class ThingSpeakApi:
    def __init__(self):
        self.server = thingspeakconfig.server
        self.apikey = thingspeakconfig.apikey
        
    def WriteSingleField(self, fieldvalue):    
        url = f"{self.server}/update?api_key={self.apikey}&field1={fieldvalue}"
        request = urequests.post(url)
        request.close()
    
    def WriteMultipleFields(self, field_data):    
        url = f"{self.server}/update?api_key={self.apikey}"
        i = 1
        for field_value in field_data: 
            url = url + f"&field{i}={field_value}"
            i = i + 1
    
        request = urequests.post(url)
        request.close()