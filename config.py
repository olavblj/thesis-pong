from PyQt5.QtCore import Qt

# <--- SIZES --->

# Base size
base_size = 1.5

# Initial ball velocity
init_ball_vel = 3 * base_size

# Increase in ball velocity when it hits a paddle
ball_vel_inc = 0.5 * base_size

# Radius of ball
ball_radius = 16 * base_size

# Window size
window_size = (700 * base_size, 400 * base_size)

# Paddle shape
paddle_shape = (10 * base_size, 100 * base_size)

# Paddle velocity
paddle_vel = 5 * base_size

scene_margin = 2 * base_size

mid_text_size = 40 * base_size

# <--- KEYS --->

left_up = Qt.Key_W
left_down = Qt.Key_S
right_up = Qt.Key_Up
right_down = Qt.Key_Down

solo_up = right_up
solo_down = right_down

# <--- TIME --->

# Timer refresh rate
timer_rate = 30
timer_delay = int(1000 // timer_rate)


class PaddleColor:
    moving = Qt.green
    done_moving = Qt.gray
    inactive = Qt.white
