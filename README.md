## Gopro Backup

This is a incremental backup, that copy the Gopro media content

The initial idea was run this application on Raspberry Pi, for use in my travels, without having to take a laptop always in my bag, safing space and being carefree

## How's work
Install this application in one device

Enable Wireless conection on Gopro

Connect in Gopro wireless network using the device which will run this application and execute `backup.py`

## Install
This application requires Python 3 and [`goprocam`](https://github.com/KonradIT/gopro-py-api) library

On Linux / Mac
```
$ sudo pip3 install goprocam
```

On Windows run Prompt Command as administrator and type
```
python -m pip install goprocam
```

Download or clone this project
```
git clone https://github.com/fvidals/gpbackup.git
```

Run `backup.py`

### Settings

You can customize some options

```python
from gpbackup import GPBackup

myOptions = {
    'mediaDir': '/home/developer/media', # directory for storage pictures, videos etc
    'tmpDir': '/tmp/gpcache', # directory for temp download media
    'logDir': '/var/log/gpbackup', # directory for storage log files
    'notifyOnStart' : True, # this quickly plays a sound locate of camera when start backup files
    'notifyOnFinish' : True, #this quickly plays a sound locate of camera after backup
    'powerOffWifiFinish' : True, #turn off the wifi camera after backup
    'powerOffCamFinish': True #turn off the camera after backup 
}

GPBackup.GPBackup(myOptions).run()

```
