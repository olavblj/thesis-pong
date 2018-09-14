import os
import threading

import requests
from tqdm import tqdm

from config import Path, batch_size, URL, ch_names
from models.time_frame import TimeFrame
from system_manager import SystemManager
from utils.prints import Print, print_section

sys_manager = SystemManager.get_instance()


class Uploader(threading.Thread):
    def __init__(self, session_id, keep_buffer=False):
        super().__init__()
        self.session_id = session_id
        self.keep_buffer = keep_buffer
        self.buffer_path = '{}_{}'.format(Path.recording_buffer, self.session_id)

    @print_section
    def run(self):
        is_successful = self.upload_recording_buffer()

        if is_successful:
            if not self.keep_buffer:
                os.remove(self.buffer_path)
        else:
            Print.failure("Failed to upload recording buffer")

    def upload_recording_buffer(self):
        all_successful = True
        time_frames = list()
        line_count = sum(1 for _ in open(self.buffer_path))

        ch_count = len(ch_names)

        with open(self.buffer_path) as infile:
            for i, line in enumerate(tqdm(infile, total=line_count)):
                new_time_frame = TimeFrame.from_line(line)

                if not len(new_time_frame.sensor_data) == ch_count:
                    Print.warning("Skipped TimeFrame with {} data points".format(len(new_time_frame.sensor_data)))
                    Print.data(new_time_frame.sensor_data)
                    continue

                time_frames.append(new_time_frame.to_json())

                if (i + 1) % batch_size == 0:
                    if not self.upload_batch(time_frames):
                        Print.failure("Failed to upload batch")
                        all_successful = False
                    time_frames = list()

            self.upload_batch(time_frames)

        return all_successful

    @staticmethod
    def upload_batch(time_frames):
        url = URL.timeframes

        r = requests.post(url, json=time_frames)
        if r.status_code != 201:
            Print.failure("Failed to upload batch")
            return False
        return True
