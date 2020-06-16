# raspberrypi_temperature
Personal project for temperature measurement and visualization using Raspberry Pi

## Launch

For data acquisition and graph generation processes:

```
python background_processing.py
```

For web server:

```
sudo FLASK_APP=app.py flask run --host=0.0.0.0 --port=80
```

Includes code done by [Bradley Gillap](https://github.com/bradgillap/I2C-LCD-Display), used under Apache License.