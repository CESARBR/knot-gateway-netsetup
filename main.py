#!/usr/bin/env python
#
# Copyright (c) 2019, CESAR. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0

import os
import sys
import signal
import lockfile
import functools
import logging
import dbus
import dbus.service
import dbus.mainloop.glib
import gobject as GObject

import daemon

mainloop = None

logging.basicConfig(format='[%(levelname)s] %(funcName)s: %(message)s\n',
                    stream=sys.stderr, level=logging.INFO)


def quit_cb(signal_number, stack_frame):
    logging.info("Terminate with signal %d" % signal_number)
    mainloop.quit()


context = daemon.DaemonContext(
    working_directory='/usr/local/bin',
    umask=0o002,
    detach_process=False,
    pidfile=lockfile.FileLock('/tmp/netsetup'),
    signal_map={signal.SIGTERM: quit_cb, signal.SIGINT: quit_cb},
    stdout=sys.stdout,
    stderr=sys.stderr,
)


with context:
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    mainloop = GObject.MainLoop()

    mainloop.run()