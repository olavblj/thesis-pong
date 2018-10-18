from datetime import datetime, timezone, timedelta

import numpy as np

from config import Path
from system_manager import SystemManager

sys_manager = SystemManager.get_instance()


def date_str(timestamp):
    return datetime.fromtimestamp(timestamp, tz=timezone(offset=timedelta(hours=2)))


def fetch_highscore():
    file_path = Path.high_score_list

    names = []
    scores = []
    with open(file_path) as infile:
        for i, line in enumerate(infile):
            tokens = [t.strip() for t in line.split(";")]
            name, score = tokens
            names.append(name)
            scores.append(int(score))

    order = np.flip(np.argsort(scores))
    scores = np.array(scores)[order]
    names = np.array(names)[order]

    res = []

    for i in range(len(scores)):
        res.append("{}: {} - {}".format(i + 1, scores[i], names[i]))

    return res
