from datetime import datetime, timezone, timedelta

import numpy as np

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


def fetch_highscore():
    file_path = Path.high_score_list
    line_count = sum(1 for _ in open(file_path))

    names = []
    scores = []
    with open(file_path) as infile:
        for i, line in enumerate(infile):
            tokens = [t.strip() for t in line.split(";")]
            name, score = tokens
            print(name, score)
            names.append(name)
            scores.append(score)

    order = np.flip(np.argsort(scores))
    print(order)
    scores = np.array(scores)[order]
    names = np.array(names)[order]

    res = []

    for i in range(len(scores)):
        res.append("{}: {} - {}".format(i + 1, scores[i], names[i]))

    return res
