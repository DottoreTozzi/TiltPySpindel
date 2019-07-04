# TILT Hydrometer "plug-in" for iSpindel Generic TCP Server
#### (tilt.py Version 0.1)

[German Version](README.md)

Still experimental:

Listens to Bluetooth LE 4.0 Beacons and looks for Data coming from a TILT Hydrometer.
Accumulates this Data over a configurable duration in seconds, averages it and sends it to iSpindle.py.
TILT sends data approximately every 1-2 seconds, so we are averaging it over this amount of time.
The Default is 5 minutes.

Usage is very simple, there is almost nothing to install.
Except:

* bluez
* python-bluez
* bluetooth

So we shall get these by entering on the console:

```sudo apt-get install bluez python-bluez bluetooth


In order to start this script as a service (and restart it on reboot):

```sudo cp tilt-srv.service /etc/systemd/system
```sudo systemctl daemon-reload
```sudo systemctl enable tilt-srv
```sudo systemctl start tilt-srv
```sudo mysql < CalibTilts.sql

There's nothing to configure. This will run out-of-the-box.

Of course, the data isn't 100% compatible, so we are using the following work-arounds:

* The name of the Tilt is "Tilt " and the corresponding color. For example: "Tilt Blue".
* The ID is 1-8, one for each available color.
* Right now, token is always "Test".

TILT only sends SG and Temp in F.
So, extract (P or %w/w) is being calculated.
Also, the "angle", which in this case does not represent the real tilt of the device but rather a range of angles that is easy to lateron translate back to extract concentration.

This code still has to be considered "alpha", but I am convinced it works in a productive environment.
But of course: Use at your own risk.

And take a look at tilt.py and send me your pull requests.

Have fun,
Stephan/Tozzi (stephan@sschreiber.de)