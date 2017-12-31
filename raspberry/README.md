# Setting GPBackup Raspberry

## Install
Install the depedencies
```
$ apt-get install python3-pip
```

```
$ pip3 install goprocam
```

Download this project and unzip

```
$ su
# mkdir /srv/apps/
# cd /srv/apps/
# wget https://github.com/fvidals/gpbackup/archive/master.zip
# unzip master.zip
# mv /srv/apps/gpbackup-master /srv/apps/gpbackup
# rm -f /srv/apps/master.zip
```

## Network Settings

Edit `wpa_supplicant.conf`
```
# nano /etc/wpa_supplicant/wpa_supplicant.conf
```

Set your Gopro wifi with highest priority
```
country=BR
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
    ssid="GOPRO-HERO"
    psk="beahero"
    priority=99
    id_str="gopro"
}

network={
    ssid="family"
    psk="mypassword"
    priority=1
    id_str="home"
}
```

## Add Service Backup

Copy [`gpbackup.sh`](gpbackup.sh) to init scripts directory
```
# cp /srv/apps/gpbackup/raspberry/gpbackup.sh /etc/init.d/gpbackup
```

Give execution permission
```
# chmod +x /etc/init.d/gpbackup
```

Enable run on boot
```
# update-rc.d gpbackup defaults 99
```


## Usage
- Power on the camera and turn on wifi
- Power on Raspberry
