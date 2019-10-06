
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

    def set_show_welcome(self, show_welcome):
        self.settings.set_string('show-welcome', show_welcome)

    def show_welcome(self):
        show_welcome = self.settings.get_string('show-welcome')
        return show_welcome

    def set_debug(self, sender, debug):
        self.settings.set_boolean('debug', debug)

    def get_debug(self):
        debug = self.settings.get_boolean('debug')
        return debug

    def set_log_file(self, log_file):
        self.settings.set_string('log-file', log_file)

    def get_log_file(self):
        log_file = self.settings.get_string('log-file')
        return log_file

    def get_settings_obj(self):
        return self.settings
        
