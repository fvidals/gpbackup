#! /bin/sh
### BEGIN INIT INFO
# Provides:          Backup gopro camera
# Required-Start:    $all
# Required-Stop:     
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Manage my cool stuff
### END INIT INFO

GOPRO_HOST=10.5.5.9
WORKDIR=/srv/apps/gpbackup/
BACKUP_SCRIPT=/srv/apps/gpbackup/backup.py

IS_RUNNING=$(ps aux | grep $BACKUP_SCRIPT | grep -v grep | awk '{print $2}')

case "$1" in
    start)
        if ! [ -z "$IS_RUNNING" ]; then
            message="gpbackup: A backup instance is running"
            logger $message
            echo $message

            exit 0
        fi

        message="gpbackup: Starting GoPro Backup"
        logger $message
        echo $message

        found=0

        for attemp in $(seq 1 12); do
            GATEWAY=$(ip route show | grep -i 'default via'| awk '{print $3 }')

            if [ "$GATEWAY" = "$GOPRO_HOST" ]; then
                found=1
                cd $WORKDIR
                python3 $BACKUP_SCRIPT
                exit 0
            fi

            sleep 10
        done

        if [ $found -eq 0 ]; then
            message="gpbackup: GoPro not found"
            logger $message
            echo $message
        fi

        exit 0
        ;;

    stop)
        for pid in "$IS_RUNNING"; do 
            echo "gpbackup: Stoping backup  PID: ${pid}"
            kill $pid;
        done

        exit 0
        ;;

    status)
        if ! [ -z "$IS_RUNNING" ]; then
            echo "gpbackup: GoPro backup is running"
        else
            echo "gpbackup: GoPro backup is NOT running"
        fi

        exit 0
        ;;

    *)
        echo "Usage: /etc/init.d/gpbackup {start|stop|status}"
        exit 1
        ;;
esac
