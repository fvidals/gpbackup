#!/usr/bin/python

class DiskSpace(object):
    """
    Disk Usage for Unix like
    Source: https://gist.github.com/igniteflow/3782116

    Example usage:

    disk_space = DiskSpace()
    disk_space.max_usage = '90%'
    disk_space.is_low()
    """

    max_usage = '70%'

    def __init__(self, args='h', is_test=False):
        """
        Get output of df and transform it to a tuple of list representing the table
        format the UNIX command prints in the console
        """
        if not is_test:
            raw_output = self.get_raw_df_output(args)
            self.disk_space = self.transform_raw_output(raw_output)

    def get_raw_df_output(self, args='h'):
        return commands.getoutput('df -%s' % args)

    def transform_raw_output(self, raw_output):
        output = raw_output.split('\n')
        output[0] = output[0].replace('Mounted on', 'Mounted_on')
        headers, rest = output[0].split(), output[1:]

        disk_space =  [headers]
        for line in rest:
            disk_space.append(line.split())
        return disk_space

    def headers(self):
        """ Returns a list """
        return self.disk_space[0]

    def rows(self):
        """ Returns a list of lists """
        return self.disk_space[1:]

    def get_column_index(self, title):
        """ Returns an integer """
        return self.headers().index(title)

    def get_row(self, filesystem):
        """ Returns a list """
        for row in self.rows():
            if row[0] == filesystem:
                return row

    def get_value(self, filesystem, column_title):
        """
        :param filesystem: string
        :param column_title: string
        :returns string
        """
        row = self.get_row(filesystem)
        return row[self.get_column_index(column_title)]

    def get_use_as_percentage(self, partition=None):
        """Returns string eg. 70%
        """
        if not partition:
            partition = settings.PARTITION # django settings eg. '/dev/sda7'
        return self.get_value(partition, 'Use%')

    def usage_greater_than_max(self, usage, _max):
        """
        :param usage: string. eg. '70%'
        :param _max: string. eg. '80%'
        :returns boolean.  True is disk space is low
        """
        avail = int(usage.replace('%', ''))
        _max = int(_max.replace('%', ''))
        return True if avail > _max else False

    def is_low(self):
        usage = self.get_use_as_percentage()
        if self.usage_greater_than_max(usage, self.max_usage):
            return usage
        else:
            return
