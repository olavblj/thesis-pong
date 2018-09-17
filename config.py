import os

from PyQt5.QtCore import Qt

# <=============== PONG GAME CONFIG ===============>


# <--- SIZES --->

# Base size
base_size = 1.5

# Initial ball velocity
init_ball_vel = 3 * base_size

# Increase in ball velocity when it hits a paddle
ball_vel_inc = 0.2 * base_size

# Radius of ball
ball_radius = 16 * base_size
ball_shape = (ball_radius, ball_radius)

# Window size
window_size = (700 * base_size, 400 * base_size)

# Paddle shape
paddle_shape = (10 * base_size, 70 * base_size)

# Paddle velocity
paddle_vel = 8 * base_size

scene_margin = 2 * base_size

mid_text_size = 40 * base_size
score_text_size = 20 * base_size


# <--- KEYS --->

class Key:
    left_up = Qt.Key_W
    left_down = Qt.Key_S
    right_up = Qt.Key_Up
    right_down = Qt.Key_Down

    solo_up = Qt.Key_Space
    solo_down = Qt.Key_B

    replay = Qt.Key_Space
    exit = Qt.Key_Escape


# <--- TIME --->

# Timer refresh rate
timer_rate = 30
timer_delay = int(1000 // timer_rate)

# <=============== RECORDING CONFIG ===============>


dev_mode = True
batch_size = 500
ch_names = ["C3", "C4", "P3", "P4"]


class URL:
    _base = "http://127.0.0.1:8000" if dev_mode else ""

    timeframes = "/".join([_base, "time-frames"])
    sessions = "/".join([_base, "sessions"])
    persons = "/".join([_base, "persons"])


class Path:
    _project_root = os.path.dirname(os.path.realpath(__file__))

    recording_buffer = "{}/data/recording_buffer".format(_project_root)
    high_score_list = "{}/data/high_score_list".format(_project_root)
