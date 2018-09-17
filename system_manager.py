import sys
import time

from utils.prints import Print, print_init, print_section


class SystemManager:
    __instance = None

    @staticmethod
    def get_instance():
        if SystemManager.__instance is None:
            SystemManager()
        return SystemManager.__instance

    @print_init
    def __init__(self):
        if SystemManager.__instance is not None:
            raise Exception("This class is a singleton!")

        SystemManager.__instance = self

        # -- THREADS --
        self.game_window = None
        self.streamhandler = None

        # -- SYSTEM OBJECTS --
        self.session = None
        self.person = None
        self.current_action = None

        # -- STATUS FLAGS --
        self.receiving_samples = False
        self.is_real_data = False

    # <--- RECORDING CONTROL --->

    @print_section
    def start_recording(self):
        self.streamhandler.start_recording()

    @print_section
    def stop_recording(self):
        self.current_action = None
        self.streamhandler.stop_recording()

    # <--- SYSTEM FLOW FUNCTIONS --->

    @print_section
    def exit_system(self):

        self.streamhandler.stop()
        time.sleep(1)
        Print.success("Successfully exited program.")
        sys.exit()

    # <--- HELPER METHODS --->
    def set_receiving_samples(self, receiving_samples):
        if self.receiving_samples != receiving_samples:
            self.game_window.update_status_indicator(receiving_samples)
        self.receiving_samples = True
