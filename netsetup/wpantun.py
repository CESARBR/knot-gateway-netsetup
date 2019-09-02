#!/usr/bin/env python
#
# Copyright (c) 2019, CESAR. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0

import os
import sys
import logging
import dbus
import dbus.mainloop.glib
import gobject as GObject

logging.basicConfig(format='[%(levelname)s] %(funcName)s: %(message)s\n',
                    stream=sys.stderr, level=logging.INFO)

INTERFACE_SERVICE_DBUS = "com.nestlabs.WPANTunnelDriver"
INTERFACE_DBUS = "org.wpantund.v1"
INTERFACE_DBUS_PATH = "/org/wpantund/wpan0"


class Singleton(type):
    """
    Singleton class to guarantee that a single instance will be used for
    its inhereted classes
    """
    __instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            cls.__instances[cls] = super(Singleton,
                                         cls).__call__(*args, **kwargs)
        return cls.__instances[cls]


class WpanClient(object):
    __metaclass__ = Singleton

    bus = None

    def __init__(self):
        self.bus = dbus.SystemBus()
        self.iface = None
        self.iface_state = None
        self.signal_match = None
        self.state = ""
        self.node_type = ""
        self.network_name = ""
        self.pan_id = 0
        self.channel = 0
        self.xpan_id = ""
        self.mesh_ipv6 = ""
        self.masterkey = ""

    def start(self):
        self.bus.watch_name_owner(
            INTERFACE_SERVICE_DBUS, self._on_name_owner_changed)

    def _on_name_owner_changed(self, newOwner):
        if not newOwner:
            logging.info("wpantund is down")
            self._stop_monitor_properties_changes()
        else:
            logging.info("wpantund is up")
            self._start_monitor_properties_changes()

    def _stop_monitor_properties_changes(self):
        if self.signal_match:
            self.signal_match.remove()
        self.iface = None
        self.iface_state = None
        self.state = ""

    def _start_monitor_properties_changes(self):
        self.iface = self.bus.get_object(
            INTERFACE_SERVICE_DBUS,
            INTERFACE_DBUS_PATH)

        self.iface_state = self.bus.get_object(
            INTERFACE_SERVICE_DBUS,
            "/com/nestlabs/WPANTunnelDriver/wpan0/Properties/NCP/State")

        self.refresh_values()
        self.signal_match = self.iface_state.connect_to_signal(
            "PropertyChanged", self.refresh_values())

    def is_associated(self):
        return self.state == "associated"

    def refresh_values(self):
        # FIXME: Wait to interface 'wpan0' be added
        status = self.iface.Status(dbus_interface=INTERFACE_DBUS)

        self.state = status.get("NCP:State")

        if self.state == "associated":
            self.node_type = status.get("Network:NodeType")
            self.network_name = status.get("Network:Name")
            self.pan_id = status.get("Network:PANID")
            self.channel = status.get("NCP:Channel")
            self.xpan_id = status.get("Network:XPANID")
            self.mesh_ipv6 = status.get("IPv6:MeshLocalAddress")

            mkey = self.iface.PropGet(
                "Network:Key", dbus_interface=INTERFACE_DBUS)[1]

            self.masterkey = ":".join(['%02x' % item for item in mkey])
