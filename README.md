# raspberrypi_temperature
Personal project for temperature measurement and visualization using Raspberry Pi

## Setup

1. Enable I2C: https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c
2. Install python packages **globally**: `sudo pip3 install -r requirements.txt`
3. Install some extra packages: `sudo apt install libatlas-base-dev libopenjp2-7 libtiff5`
4. Enable I2C and 1-Wire using `raspi-config`

## Launch

For data acquisition and graph generation processes:

```
python3 temp_retrieval_processing.py
```

For web server:

```
sudo FLASK_APP=app.py flask run --host=0.0.0.0 --port=80
```

Includes code done by [Bradley Gillap](https://github.com/bradgillap/I2C-LCD-Display), used under Apache License.
