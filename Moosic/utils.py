import gi, string, sys, os, shutil
import NetworkManager
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from .settings import *

class Utils:
    def __init__(self):
        pass

    def list_header_func(self, row, before, user_data):
        if before and not row.get_header():
            row.set_header(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL))

    def slugify(self, s):
        valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        filename = ''.join(c for c in s if c in valid_chars)
        filename = filename.replace(' ','-')
        return filename

    def network_available(self):

        c = NetworkManager.const

        for dev in NetworkManager.NetworkManager.GetDevices():
            dev_type = c('device_type', dev.DeviceType)
            state = c('device_state', dev.State)

            self.debug(['network - device:', dev_type, 'state:', state, dev.State])

            if dev_type == 'Modem':
                # NM_DEVICE_TYPE_MODEM = 8
                self.debug(['Using GSM!!'])

            if dev.State == 100:
                #NM_DEVICE_STATE_UNKNOWN = 0
                #NM_DEVICE_STATE_UNMANAGED = 10
                #NM_DEVICE_STATE_UNAVAILABLE = 20
                #NM_DEVICE_STATE_DISCONNECTED = 30
                #NM_DEVICE_STATE_PREPARE = 40
                #NM_DEVICE_STATE_CONFIG = 50
                #NM_DEVICE_STATE_NEED_AUTH = 60
                #NM_DEVICE_STATE_IP_CONFIG = 70
                #NM_DEVICE_STATE_IP_CHECK = 80
                #NM_DEVICE_STATE_SECONDARIES = 90
                #NM_DEVICE_STATE_ACTIVATED = 100
                #NM_DEVICE_STATE_DEACTIVATING = 110
                self.debug(['connection available'])
                return True

        return False

    def debug(self, data):

        if Settings().get_debug():

            debugline = ''
            for debug in data:
                debugline = debugline + str(debug)

            frame = sys._getframe(1)
            #TODO: delete log file at startup
            debug_out = frame.f_code.co_filename + ' Line:' + str(frame.f_lineno) + ' Debug Data:' + debugline + '\n'
            log_file_path = Settings().get_log_file() + '/' + 'moozik.log'

            f = open(log_file_path, "a")
            print("Name of the file: ", f.name)
            f.write(debug_out)
            f.close()

    def create_log_file(self):
        xdg_cache_dir = os.environ.get('XDG_CACHE_HOME')
        log_dir = os.path.join(xdg_cache_dir, 'logs')

        try:
            #delete any old logfiles
            shutil.rmtree(log_dir)
            os.makedirs(log_dir, mode=0o755, exist_ok=True)
        except OSError as e:
            self.debug(["Error: %s - %s." % (e.filename, e.strerror)])
            return None
        else:
            Settings().set_log_file(log_dir)
            return log_dir
