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
        tokens = line.split(';')

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
