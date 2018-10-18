import enum
import threading
import time

from pylsl import StreamInlet, resolve_stream

from config import ch_names
from models.session import Session
from models.time_frame import TimeFrame
from system_manager import SystemManager
from utils.prints import Print, print_init, print_section
from utils.uploader import Uploader

sys_manager = SystemManager.get_instance()


class State(enum.Enum):
    IDLE = 0
    RECORDING = 1
    STOPPING = 2


class StreamHandler(threading.Thread):

    @print_init
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

        self.state = State.IDLE
        self.last_sample_time = time.time()

    @print_section
    def run(self):
        streams = resolve_stream('type', 'EEG')
        stream = StreamInlet(streams[0])

        while self.state != State.STOPPING:
            self.create_samples(stream)

    @print_section
    def stop(self):
        self.state = State.STOPPING

    def create_samples(self, stream):
        data, timestamp = stream.pull_sample(timeout=1.0)
        timestamp += stream.time_correction()

        if time.time() - self.last_sample_time < 1:
            sys_manager.set_receiving_samples(True)

        self.last_sample_time = time.time()

        if self.state == State.RECORDING:
            sensor_data = data[0:len(ch_names)]
            label = sys_manager.current_action
            TimeFrame.write_to_buffer(sensor_data, label, timestamp)

    @print_section
    def start_recording(self):
        if self.state == State.IDLE:
            sys_manager.session = Session.create()
            # create_path_if_not_existing('{}_{}'.format(Path.recording_buffer, sys_manager.session.id))

            self.state = State.RECORDING
        else:
            Print.warning("Is already recording.")

    @print_section
    def stop_recording(self):
        if self.state == State.RECORDING:
            self.state = State.IDLE

            uploader = Uploader(sys_manager.session.id)
            uploader.start()
        else:
            Print.warning("Cannot stop recording because it is not recording.")
