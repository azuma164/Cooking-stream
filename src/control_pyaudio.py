import sounddevice as sd

class Control:
    # Open the audio stream
    # Get the index of the default input device

    @staticmethod
    def mute_microphone():
        sd.default.device = sd.query_devices(kind='input')[0]
        sd.default.input_device_index = sd.default.device['index']
        sd.default.input_channels = sd.default.device['max_input_channels']
        sd.default.input_mute = True
    
    @staticmethod
    def unmute_microphone():
        sd.default.device = sd.query_devices(kind='input')[0]
        sd.default.input_device_index = sd.default.device['index']
        sd.default.input_channels = sd.default.device['max_input_channels']
        sd.default.input_mute = False