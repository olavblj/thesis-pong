from config import Path
from system_manager import SystemManager

sys_manager = SystemManager.get_instance()


class TimeFrame:
    def __init__(self, sensor_data, label, timestamp, session_id):
        self.sensor_data = sensor_data
        self.label = label
        self.timestamp = timestamp
        self.session_id = session_id

    @classmethod
    def from_line(cls, line):
        tokens = [t.strip() for t in line.split(';')]

        params = dict(
            sensor_data=[float(x) for x in tokens[0].split()],
            label=tokens[1],
            timestamp=float(tokens[2]),
            session_id=tokens[3]
        )

        return cls(**params)

    def to_json(self):
        return dict(
            sensor_data=self.sensor_data,
            label=self.label,
            timestamp=self.timestamp,
            session=self.session_id
        )

    @staticmethod
    def write_to_buffer(data, label, timestamp):
        file_path = '{}_{}'.format(Path.recording_buffer, sys_manager.session.id)

        with open(file_path, "a") as outfile:
            data_str = " ".join([str(x) for x in data])
            label_str = str(label)
            line = '{}; {}; {}; {}\n'.format(data_str, label_str, str(timestamp), sys_manager.session.id)
            outfile.write(line)
