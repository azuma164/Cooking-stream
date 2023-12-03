from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

class Control:
    @staticmethod
    def mute_microphone():
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None
        ).QueryInterface(IAudioEndpointVolume)
        interface.SetMute(True, None)

    @staticmethod
    def unmute_microphone():
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None
        ).QueryInterface(IAudioEndpointVolume)
        interface.SetMute(False, None)