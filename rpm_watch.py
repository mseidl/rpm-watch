#!/usr/bin/env python

import rpm
import pyinotify
from time import sleep

#We pick one file to watch or else we get _lots_ of notices
RPMDB = '/var/lib/rpm/Packages'

def print_diff(one, two, message='Difference'):
    """Prints out the difference of two sets with started by message"""
    #print "len one: %s // len two: %s" % (len(one), len(two))
    pkgs = one.viewkeys() - two.viewkeys()
    if pkgs:
        print '%s: %s' % (message, ', '.join(map(str,pkgs)))    

def update_installed_rpms(rpm_list):
        """Connects to the default rpmdb and queries for installed packages"""
        ts = rpm.TransactionSet()
        mi = ts.dbMatch()
        rpm_list.clear()
        for r in mi:
            rpm_list[r['name']] = [( r['version'], r['release']),  r['sha1header']]


def updated_rpms(new_rpms, old_rpms):
    """Outputs upgraded or downgraded rpms if versions change"""
    #Loop through all keys from installed packages
    for k in new_rpms:
        #if the package was previously installed
        if k in old_rpms:
            #compare (version, release) of each state
            if old_rpms[k][0] >  new_rpms[k][0]:
                print 'package %s downgraded' % k
            elif old_rpms[k][0] < new_rpms[k][0]:
                print 'package %s upgraded' % k

class RPMWatch(pyinotify.ProcessEvent):
    def __init__(self):
        """Initializer, creates empty dicts and updates them from the rpmdb"""
        self.installed_rpms = {}
        self.known_rpms = {}
        update_installed_rpms(self.installed_rpms)
        self.known_rpms = self.installed_rpms.copy()
    
    def process_IN_CLOSE_WRITE(self, event):
        """Gets called when RPMDB is modified and compares changes to determine what's new and gone"""
        print "DB modified"
        sleep(5)
        update_installed_rpms(self.installed_rpms)
        print_diff(self.installed_rpms, self.known_rpms, 'Installed ')
        print_diff(self.known_rpms, self.installed_rpms, 'Removed ')
        updated_rpms(self.installed_rpms, self.known_rpms)
        self.known_rpms = self.installed_rpms.copy()


if __name__ == '__main__':
    try:
        wm = pyinotify.WatchManager()
        handler = RPMWatch()
        notifier = pyinotify.Notifier(wm, handler)
        wdd = wm.add_watch(RPMDB, pyinotify.IN_CLOSE_WRITE)
        notifier.loop()
    finally:
        print 'done'
