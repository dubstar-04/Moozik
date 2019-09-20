import gi, string
import NetworkManager
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

def list_header_func(row, before, user_data):
    if before and not row.get_header():
        row.set_header(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL))

def slugify(s):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    filename = filename.replace(' ','-')
    return filename

def network_available():

    c = NetworkManager.const

    for dev in NetworkManager.NetworkManager.GetDevices():
        dev_type = c('device_type', dev.DeviceType)
        state = c('device_state', dev.State)

        print('network - device:', dev_type, 'state:', state, dev.State)

        if dev_type == 'Modem':
            # NM_DEVICE_TYPE_MODEM = 8
            print('Using GSM!!')

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
            print('connection available')
            return True

    return False
