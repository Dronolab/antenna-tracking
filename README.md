# Antenna Tracking
A tool to manage Dronolab's Antenna Tracking system.

## Install

Install [RTIMULib2](https://github.com/richardstechnotes/RTIMULib2)

## USC Student Competition Setup

PREPARATION
Aller dans antenna.py et changer la déclinaison magnétique pour celle de l'aéroport d'Alma

```python
# Hardcoded magnetic declination
MAGNETIC_DECLINATION = -14.46667

# Alma airport magnetic declination
# `AGNETIC_DECLINATION = -16.41667
```

ON-SITE 
1. Démarrer le GPS (je ne sais pas pourquoi mais sur la PI le deamon ne fonctionne pas en background)
```$ ssh pi@192.168.1.81```
```$ sudo gpsd -b -N -D 3 -F /var/run/gpsd.sock /dev/ttyAMA0```

2. Ouvrir MAVProxy. Sur l'ordinateur de groundstation officiel il y a un script de startup, 
normalement dans C:\Users\Drono\AppData\Local\MAVProxy\mavinit.scr. Le fichier doit avoir la ligne:
`module load interop`. Tout devrait se charger automatiquement.

3. DANS UNE NOUVELLE SESSION SSH
```$ ssh pi@192.168.1.81```
```$ cd antenna-tracking```
```$ python main.py```

Si tout va bien on devrait voir la télémétrie du drone ainsi que toutes les données de calcul de l'antenne

4. Brancher les servos
L'antenne devrait traquer le drone. 

Si une erreur survient, le programme de l'antenna va output un message d'erreur avec une description donnant
un indice sur la source du problème.

F.A.Q.

L'erreur "UAV connection failed to initialize. Please check MAVProxy or your network connection" survient et 
tout semble correct malgré tout: Redémarrer la Raspberry Pi

## License

MIT License

Copyright (c) 2016 dronolab

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
