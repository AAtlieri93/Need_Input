#Victor Ruest

#add includes

#Base state class keeping for sure
class State:
    def __init__(self, name):
        self.name = name
    
    def on_enter(self, fsm):
        pass

    def on_exit(self, fsm):
        pass
        
    def update(self, fsm, sensor_data):
        pass