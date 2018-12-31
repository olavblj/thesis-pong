# EEG-Pong

## Setup

### OpenBCI LSL

This project depends on OpenBCI LSL. A modified version of this can be found [here](https://github.com/olavblj/thesis-openbci-lsl).

### Project Setup

Run these commands from your terminal (consider using a virtualenv)

```bash
git clone https://github.com/olavblj/thesis-pong.git
cd thesis-pong
pip install -r requirements.txt
```


## Usage
1. Plug in the dongle of your OpenBCI headset, and turn the Cyton board on.
2. Run OpenBCI LSL and make sure it is streaming data.
3. Make sure a foot pedal is connected to the computer.
4. Navigate to the project directory in your terminal.
5. Run `python -m main`

If you want to upload the recorded data to the EEG API, you will need to make sure that the API is running as well.

## Foot Pedal

The author has used [this foot pedal](https://www.amazon.com/dp/B0098PLPOI?ref_=pe_1196280_123950170) with this system. This pedal outputs the character `b` when it is pressed. If a foot pedal is used that outputs a different character, the `Key.solo_down` variable has to be updated in the `config.py` file.
