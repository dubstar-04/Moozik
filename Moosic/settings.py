
from gi.repository import Gio

class Settings:
    def __init__(self):
        self.settings = Gio.Settings('org.gnome.Moosic')
        #TODO
        #Add a drop down for Audio Quality
    '''
    def set_username(self, username):
        print('set_username:',username )
        self.settings.set_string('username', username)
        
    def get_username(self):
        username = self.settings.get_string('username')
        return username
    
    def set_password(self, password):
        self.settings.set_string('password', password)
        
    def get_password(self):
        password = self.settings.get_string('password')
        return password
    '''
    
    def set_device_id(self, device_id):
        self.settings.set_string('device-id', device_id)

    def get_device_id(self):
        device_id = self.settings.get_string('device-id')
        return device_id

    def get_settings_obj(self):
        return self.settings
        
