#!/usr/bin/python

""" 
Provide GoPro incremental backup
"""

from goprocam import GoProCamera, constants
from gpbackup import DiskSpace
from gpbackup import DiskUsage
import sys
import os
import time
import datetime
import logging
import filecmp
import re

class GPBackup:
    def prepareDir(self, dir):
        if not os.path.exists(dir):
            os.makedirs(dir)

    def __init__(self, options = {}):
        self.now = datetime.datetime.now()
        self.isoNumeric = '%Y%m%d%H%M%S'
        self.isStarted = False

        self.summary = {
            'gpFiles': 0,
            'copied': 0,
            'alreadyExists': 0
        }

        self.defaultOptions = {
            'mediaDir': os.path.join('.', 'data', 'media'),
            'tmpDir': os.path.join('.', 'data', 'tmp'),
            'logDir': os.path.join('.', 'data', 'log'),
            'notifyOnStart' : True,
            'notifyOnFinish' : True,
            'powerOffWifiFinish' : True,
            'powerOffCamFinish': True
        }

        self.options = self.defaultOptions
        self.options.update(options)

        pattern = re.compile(r"[a-z0-9]+Dir$")

        for key, value in self.options.items():
            if pattern.match(key):
                self.prepareDir(value)

    def versionFile(self, filePath):
        nameParts = filePath.split('.')
        i = 0;

        while True:
            i += 1;

            if len(nameParts) > 1:
                suggestName = '.'.join(nameParts[:-1])
                suggestName += '-%d.%s' % (i, nameParts[-1])
            else:
                suggestName = '%s-%d' % (filePath, i)

            if not os.path.exists(suggestName):
                return suggestName

    def log(self):
        if not hasattr(self, 'logger'):
            logFormatter = logging.Formatter("%(asctime)s: %(message)s")

            self.logger = logging.getLogger('gp-backup')
            self.logger.setLevel(logging.DEBUG)

            fileName = "gp-backup-%s.log" % self.now.strftime(self.isoNumeric)
            pathLogFile = os.path.join(self.options['logDir'], fileName)

            consoleHandler = logging.StreamHandler()
            consoleHandler.setFormatter(logFormatter)

            fileHandler = logging.FileHandler(pathLogFile)
            fileHandler.setFormatter(logFormatter)

            self.logger.addHandler(consoleHandler)
            self.logger.addHandler(fileHandler)

        return self.logger

    def syncMedia(self):
        self.isStarted = True

        try:
            medias = self.gopro().listMedia(True, True)
        except:
            self.log().info('Cannot list media')
            self.log().info(sys.exc_info()[0])
            sys.exit()

        for media in medias:
            dirName = media[0]

            pathOutputDir = os.path.join(self.options['mediaDir'], dirName)

            self.prepareDir(pathOutputDir)

            fileName = media[1]
            self.summary['gpFiles'] += 1

            pathTmpFile = os.path.join(self.options['tmpDir'], fileName)

            pathOutputFile = os.path.join(pathOutputDir, fileName)

            if os.path.exists(pathTmpFile):
                os.remove(pathTmpFile)

            try:
                self.log().info('Downloading %s/%s' % (dirName, fileName))
                self.gopro().downloadMedia(dirName, fileName, pathTmpFile)
            except:
                self.log().info('Cannot download file %s/%s' % (dirName, fileName))
                self.log().info(sys.exc_info()[0])
                sys.exit()

            if os.path.isfile(pathOutputFile):
                if filecmp.cmp(pathTmpFile, pathOutputFile):
                    os.remove(pathTmpFile)
                    self.summary['alreadyExists'] += 1
                    continue
                else:
                    self.log().info('File %s/%s was exits, creating new version..' % (dirName, fileName))
                    pathOutputFile = self.versionFile(pathOutputFile)

            os.rename(pathTmpFile, pathOutputFile)
            self.summary['copied'] += 1

    def gopro(self):
        if not hasattr(self, 'goPro'):
            self.goprocam = GoProCamera.GoPro()

        return self.goprocam

    def notifyGopro(self, seconds = 2):
        try:
            self.gopro().locate(constants.Locate.Start)
            time.sleep(seconds)
            self.gopro().locate(constants.Locate.Stop)
        except:
            self.log('Cannot possible notify camera')
            sys.exit()

    def isSync(self):
        return (self.isStarted
                and (self.summary['copied'] + self.summary['alreadyExists']) == self.summary['gpFiles'])

    def turnOffWifi(self):
        try:
            self.gopro().gpControlSet(constants.Setup.WIFI, constants.Setup.Wifi.OFF)
        except:
            self.log().info('Cannot possible turn off wifi')
            sys.exit()

    def turnOff(self):
        try:
            self.gopro().power_off()
        except:
            self.log('Cannot possible turn off camera')
            sys.exit()

    def logkDiskUsage(self):
        diskUsage = DiskUsage.DiskUsage();

        size = diskUsage.disk_usage(self.options['mediaDir'])
        sizeFormatted = diskUsage.format_size(size)

        self.log().info('Size of media directory: %s' % (sizeFormatted))

    def run(self):
        self.log().info('Start backup now')

        if (self.options['notifyOnStart']):
            self.notifyGopro(2)

        self.syncMedia()

        self.log().info('GoPro end process')
        self.log().info('Files in Gopro: %d' % self.summary['gpFiles'])
        self.log().info('Files alredy exists in backup: %d' % self.summary['alreadyExists'])
        self.log().info('Files copied: %d' % self.summary['copied'])
        self.log().info('Gopro is syncronized: %s' % ('yes' if self.isSync() else 'no'))
        self.logkDiskUsage()

        if (self.options['notifyOnStart']):
            self.notifyGopro(10)

        if (self.options['powerOffWifiFinish']):
            self.turnOffWifi()

        if (self.options['powerOffCamFinish']):
            self.turnOff()
