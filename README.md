# TILT Hydrometer "plug-in" for iSpindel Generic TCP Server
#### (tilt.py Version 0.1)

[English Version](README_en.md)

Noch experimentell:

Nimmt die Daten vom Raspi per Bluetooth 4.0 LE "hörbarer" TILT Hydrometer entgegen.
Diese werden dann über einen konfigurieren Zeitraum hinweg akkumuliert.
Nach Ablauf des Intervalls werden sie gemittelt und zum iSpindle.py Skript weitergeleitet.
Das TILT sendet fast sekündlich neue Daten, diese werden also geglättet.
Das Default ist 5 Minuten.

Vorab:
Ihr braucht nichts zu installieren.

Also OK, gelogen, 'fast nichts.'
Außer den folgenden Paketen:

* bluez
* python-bluez
* bluetooth

Diese werden also nachinstalliert mit:
```sudo apt-get install bluez python-bluez bluetooth

Um das Skript als Service zu starten (Autostart):
```sudo cp tilt-srv.service /etc/systemd/system
```sudo systemctl daemon-reload
```sudo systemctl enable tilt-srv
```sudo systemctl start tilt-srv
```sudo mysql < CalibTilts.sql

Es gibt erst mal nichts zu konfigurieren, das sollte out-of-the box laufen!

Die Übernahme der Daten klappt natürlich nicht völlig 1:1.

Der Name der "iSpindel" ist "TILT" und die Farbe (z.B. "BLUE").
Der Winkel wird mit einer kruden Formel aus der Gravity Messung des TILT berechnet.
Um das zu "kalbrieren" muss die Tabelle "Calibration" in der Datenbank angepasst werden.
Das kann man z.B. mit Hilfe der Datei "CalibTilts.sql" tun, wie oben bereits gemacht.

Hintergrund:
Das TILT sendet "nur" den gemessenen und berechneten Wert der SG und die Temperatur in F.
Gewicht % des Extrakts (%w/w), scheinbar (aka ˚P) und die Temperatur in Celsius müssen also berechnet werden.
Ebenso der Winkel. Dieser entspricht natürlich in keiner Weise dem tatsächlichen Winkel des TILT.
Vielmehr habe ich hier eine Formel eingebaut, die nachher in den Diagrammen wieder einfach aufzulösen ist:

``` angle: 25 + (gravP * 1.6)

Damit wird auch ziemlich genau der erlaubte bzw. empfohlene Messbereich abgebildet.


Das ist alles noch unfertig und wird vielleicht noch nicht immer zu 100% funktionieren.
Manches ist noch quick & dirty, aber immerhin läuft es!

Schaut Euch das tilt.py Script mal an und teilt Eure Ideen mit mir, bitte.


Viel Spaß
Stephan/Tozzi (stephan@sschreiber.de)
