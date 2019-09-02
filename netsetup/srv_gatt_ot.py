#!/usr/bin/env python
#
# Copyright (c) 2019, CESAR. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0

import logging
import dbus
import struct
from dbus.service import method as dbus_method

from ble_util.gatt_service import Service
from ble_util.characteristic import Characteristic


class OpenthreadService(Service):
    UUID = "a8a9e49c-aa9a-d441-9bec-817bb4900e30"

    def __init__(self, bus, index, wpantun):
        Service.__init__(self, bus, index, self.UUID, True)
        self.add_characteristic(OpenthreadChannelCharacteristic(bus, 0, self,
                                wpantun))
        self.add_characteristic(OpenthreadNameCharacteristic(bus, 1, self,
                                wpantun))
        self.add_characteristic(OpenthreadPanIDCharacteristic(bus, 2, self,
                                wpantun))
        self.add_characteristic(OpenthreadXPanIDCharacteristic(bus, 3, self,
                                wpantun))
        self.add_characteristic(OpenthreadMasterKeyCharacteristic(bus, 4, self,
                                wpantun))
        self.add_characteristic(OpenthreadStateCharacteristic(bus, 5, self,
                                wpantun))
        self.add_characteristic(OpenthreadMeshIPv6Characteristic(bus, 6, self,
                                wpantun))


class OpenthreadChannelCharacteristic(Characteristic):
    CHANNEL_CHRC_UUID = "a8a9e49c-aa9a-d441-9bec-817bb4900d31"

    def __init__(self, bus, index, service, wpantun):
        Characteristic.__init__(self, bus, index, self.CHANNEL_CHRC_UUID,
                                ["read"], service)
        if wpantun.is_associated():
            self.value = dbus.Array(
                dbus.Byte(i) for i in struct.pack(">l", wpantun.channel))
        else:
            self.value = []

    def ReadValue(self, options):
        logging.info('OpenthreadChannelCharacteristic Read: ' +
                     repr(self.value))
        return self.value


class OpenthreadNameCharacteristic(Characteristic):
    NAME_CHRC_UUID = "a8a9e49c-aa9a-d441-9bec-817bb4900d32"

    def __init__(self, bus, index, service, wpantun):
        Characteristic.__init__(self, bus, index, self.NAME_CHRC_UUID,
                                ["read"], service)
        if wpantun.is_associated():
            self.value = dbus.Array(
                dbus.Byte(i) for i in bytes(wpantun.network_name))
        else:
            self.value = []

    def ReadValue(self, options):
        logging.info('OpenthreadNameCharacteristic Read: ' + repr(self.value))
        return self.value


class OpenthreadPanIDCharacteristic(Characteristic):
    PANID_CHRC_UUID = "a8a9e49c-aa9a-d441-9bec-817bb4900d33"

    def __init__(self, bus, index, service, wpantun):
        Characteristic.__init__(self, bus, index, self.PANID_CHRC_UUID,
                                ["read"], service)
        if wpantun.is_associated():
            self.value = dbus.Array(
                dbus.Byte(i) for i in struct.pack(">H", wpantun.pan_id))
        else:
            self.value = []

    def ReadValue(self, options):
        logging.info('OpenthreadPanIDCharacteristic Read: ' + repr(self.value))
        return self.value


class OpenthreadXPanIDCharacteristic(Characteristic):
    XPANID_CHRC_UUID = "a8a9e49c-aa9a-d441-9bec-817bb4900d34"

    def __init__(self, bus, index, service, wpantun):
        Characteristic.__init__(self, bus, index, self.XPANID_CHRC_UUID,
                                ["read"], service)
        if wpantun.is_associated():
            self.value = dbus.Array(
                dbus.Byte(i) for i in struct.pack(">Q", wpantun.xpan_id))
        else:
            self.value = []

    def ReadValue(self, options):
        logging.info('OpenthreadXPanIDCharacteristic Read: ' +
                     repr(self.value))
        return self.value


class OpenthreadMasterKeyCharacteristic(Characteristic):
    MASTERKEY_CHRC_UUID = "a8a9e49c-aa9a-d441-9bec-817bb4900d35"

    def __init__(self, bus, index, service, wpantun):
        Characteristic.__init__(self, bus, index, self.MASTERKEY_CHRC_UUID,
                                ["read"], service)
        if wpantun.is_associated():
            self.value = dbus.Array(
                dbus.Byte(i) for i in bytes(wpantun.masterkey))
        else:
            self.value = []

    def ReadValue(self, options):
        logging.info('OpenthreadMasterKeyCharacteristic Read: ' +
                     repr(self.value))
        return self.value


class OpenthreadStateCharacteristic(Characteristic):
    STATE_CHRC_UUID = "a8a9e49c-aa9a-d441-9bec-817bb4900d36"

    def __init__(self, bus, index, service, wpantun):
        Characteristic.__init__(self, bus, index, self.STATE_CHRC_UUID,
                                ["read"], service)
        if wpantun.is_associated():
            self.value = dbus.Array(
                dbus.Byte(i) for i in bytes(wpantun.state))
        else:
            self.value = []

    def ReadValue(self, options):
        logging.info('OpenthreadStateCharacteristic Read: ' + repr(self.value))
        return self.value


class OpenthreadMeshIPv6Characteristic(Characteristic):
    MESHIPV6_CHRC_UUID = "a8a9e49c-aa9a-d441-9bec-817bb4900d37"

    def __init__(self, bus, index, service, wpantun):
        Characteristic.__init__(self, bus, index, self.MESHIPV6_CHRC_UUID,
                                ["read"], service)
        if wpantun.is_associated():
            self.value = dbus.Array(
                dbus.Byte(i) for i in bytes(wpantun.mesh_ipv6))
        else:
            self.value = []

    def ReadValue(self, options):
        logging.info('OpenthreadMeshIPv6Characteristic Read: ' +
                     repr(self.value))
        return self.value
