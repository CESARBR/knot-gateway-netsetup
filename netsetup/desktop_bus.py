#!/usr/bin/env python
#
# Copyright (c) 2019, CESAR. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0

import os
import sys
import logging
import struct
import dbus
from dbus.service import method as dbus_method

logging.basicConfig(format='[%(levelname)s] %(funcName)s: %(message)s\n',
                    stream=sys.stderr, level=logging.INFO)

OPENTHREAD_IFACE = 'br.org.cesar.knot.netsetup.Openthread'


class FailedException(dbus.exceptions.DBusException):
    _dbus_error_name = 'br.org.cesar.knot.netsetup.Openthread.Error.Failed'


class NotSupportedException(dbus.exceptions.DBusException):
    _dbus_error_name = 'br.org.cesar.knot.netsetup.Openthread.Error.NotSupported'


class OpenthreadBus(dbus.service.Object):
    """
    br.org.cesar.knot.netsetup.Openthread interface implementation
    """

    def __init__(self, bus, wpan):
        self.wpan = wpan
        self.path = '/br/org/cesar/knot/netsetup/openthread'
        dbus.service.Object.__init__(self, bus, self.path)

    def __fmt_to_bytes(self, fmt, arg):
        """
            Convert the values in fmt to bytes.
            The formats strings can be found in
            https://docs.python.org/2/library/struct.html#format-strings
        """
        return struct.pack(fmt, arg)

    def __bytes_to_dbus_byte_array(self, arg):
        """
            Convert python Bytes in dbus bytes array
        """
        return dbus.Array(dbus.Byte(i) for i in arg)

    @dbus_method(dbus.PROPERTIES_IFACE,
                 in_signature='ss', out_signature='v')
    def Get(self, interface_name, property_name):
        """
            Get property method
        """
        return self.GetAll(interface_name)[property_name]

    @dbus_method(dbus.PROPERTIES_IFACE,
                 in_signature='s', out_signature='a{sv}')
    def GetAll(self, interface_name):
        """
            Get all properties method
        """
        if self.wpan is not None:
            return {
                OPENTHREAD_IFACE: {
                    'network_name': self.__bytes_to_dbus_byte_array(
                                bytes(self.wpan.network_name)),
                    'pan_id': self.__bytes_to_dbus_byte_array(
                                self.__fmt_to_bytes(">H", self.wpan.pan_id)),
                    'channel': self.__bytes_to_dbus_byte_array(
                                self.__fmt_to_bytes(">l", self.wpan.channel)),
                    'xpan_id': self.__bytes_to_dbus_byte_array(
                                self.__fmt_to_bytes(">Q", self.wpan.xpan_id)),
                    'mesh_ipv6': self.__bytes_to_dbus_byte_array(
                                bytes(self.wpan.mesh_ipv6)),
                    'masterkey': self.__bytes_to_dbus_byte_array(
                                bytes(self.wpan.masterkey))
                }
            }
        else:
            raise FailedException()

    @dbus_method(dbus.PROPERTIES_IFACE, in_signature='ssv')
    def Set(self, interface_name, property_name, new_value):
        """
            Set property method
            Not Supported
        """
        raise NotSupportedException()

    @dbus.service.signal(dbus.PROPERTIES_IFACE, signature='sa{sv}as')
    def PropertiesChanged(self, interface_name, changed_properties,
                          invalidated_properties):
        """
            Properties changed signal
            Not Supported
        """
        raise NotSupportedException()


class DbusService(dbus.service.Object):
    """
    netsetup dbus implementation
    """

    bus = None
    openthread_iface = None

    def __init__(self, wpan):

        self.bus = dbus.SystemBus()

        self._bus_name = dbus.service.BusName(
            'br.org.cesar.knot.netsetup', dbus.SystemBus())

        self.openthread_iface = OpenthreadBus(self.bus, wpan)
