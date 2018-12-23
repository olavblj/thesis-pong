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
3. Navigate to the project directory in your terminal.
4. Run `python -m main`

If you want to upload the recorded data to the EEG API, you will need to make sure that the API is running as well.