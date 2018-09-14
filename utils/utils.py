from datetime import datetime, timezone, timedelta

from config import Path
from system_manager import SystemManager

sys_manager = SystemManager.get_instance()


def write_time_frame(data, label, timestamp):
    file_path = '{}_{}'.format(Path.recording_buffer, sys_manager.session.id)

    with open(file_path, "a") as outfile:
        data_str = " ".join([str(x) for x in data])
        label_str = str(label)
        line = '{}; {}; {}; {}\n'.format(data_str, label_str, str(timestamp), sys_manager.session.id)
        outfile.write(line)


def date_str(timestamp):
    return datetime.fromtimestamp(timestamp, tz=timezone(offset=timedelta(hours=2)))
