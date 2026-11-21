#Victor Ruest

class SensorData:
    def __init__(self, emergency_stop, emergency_release, teleop, obsticle_stop, autonomy):
        self.emergency_stop = emergency_stop
        self.emergency_release = emergency_release
        self.teleop = teleop
        self.obsticle_stop = obsticle_stop
        self.autonomy = autonomy