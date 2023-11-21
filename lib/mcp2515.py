#!/usr/bin/env python
# -*- coding: utf-8 -*-
# mcp2515.py

from machine import Pin, SPI

# MCP2515 SPI Instruction Set
RESET = 0xC0

READ = 0x03
READ_RXB0SIDH = 0x90
READ_RXB0D0 = 0x92
READ_RXB1SIDH = 0x94
READ_RXB1D0 = 0x96

WRITE = 0x02
LOAD_TXB0SIDH = 0x40  # TX0 ID location
LOAD_TXB0D0 = 0x41    # TX0 Data location
LOAD_TXB1SIDH = 0x42  # TX1 ID location
LOAD_TXB1D0 = 0x43    # TX1 Data location
LOAD_TXB2SIDH = 0x44  # TX2 ID location
LOAD_TXB2D0 = 0x45    # TX2 Data location

RTS_TX0 = 0x81
RTS_TX1 = 0x82
RTS_TX2 = 0x84
RTS_ALL = 0x87
READ_STATUS = 0xA0
RX_STATUS = 0xB0
BIT_MOD = 0x05

# MCP25152515 Register Adresses
RXF0SIDH = 0x00
RXF0SIDL = 0x01
RXF0EID8 = 0x02
RXF0EID0 = 0x03
RXF1SIDH = 0x04
RXF1SIDL = 0x05
RXF1EID8 = 0x06
RXF1EID0 = 0x07
RXF2SIDH = 0x08
RXF2SIDL = 0x09
RXF2EID8 = 0x0A
RXF2EID0 = 0x0B
CANSTAT = 0x0E
CANCTRL = 0x0F

RXF3SIDH = 0x10
RXF3SIDL = 0x11
RXF3EID8 = 0x12
RXF3EID0 = 0x13
RXF4SIDH = 0x14
RXF4SIDL = 0x15
RXF4EID8 = 0x16
RXF4EID0 = 0x17
RXF5SIDH = 0x18
RXF5SIDL = 0x19
RXF5EID8 = 0x1A
RXF5EID0 = 0x1B
TEC = 0x1C
REC = 0x1D

RXM0SIDH = 0x20
RXM0SIDL = 0x21
RXM0EID8 = 0x22
RXM0EID0 = 0x23
RXM1SIDH = 0x24
RXM1SIDL = 0x25
RXM1EID8 = 0x26
RXM1EID0 = 0x27
CNF3 = 0x28
CNF2 = 0x29
CNF1 = 0x2A
CANINTE = 0x2B
CANINTF = 0x2C
EFLG = 0x2D

TXB0CTRL = 0x30
TXB1CTRL = 0x40
TXB2CTRL = 0x50
RXB0CTRL = 0x60
RXB0SIDH = 0x61
RXB1CTRL = 0x70
RXB1SIDH = 0x71

class MCP2515:
    def __init__(self):
        self.spi = SPI(0, 10_000_000, polarity=0, phase=0, sck=Pin(6), mosi=Pin(7), miso=Pin(4))
        self.cs = Pin(5, Pin.OUT)

    def verify_mode_transition(self, mode):
        loop = 10
        for i in range(loop):
            if (self.ReadByte(CANSTAT) & 0xE0) == mode:
                return True
            loop = loop - 1
        return False

    def set_config_mode(self):
        # Set CANCTRL Register to Configuration mode.
        self.write_byte(CANCTRL, 0x80)
        return self.verify_mode_transition(0x80)

    def set_normal_mode(self):
        # Set CANCTRL Register to Normal mode.
        self.write_byte(CANCTRL, 0x00)
        return self.verify_mode_transition(0x00)

    def set_sleep_mode(self):
        # Set CANCTRL Register to Sleep mode.
        self.write_byte(CANCTRL, 0x20)
        return self.verify_mode_transition(0x20)

    def reset(self):
        # Reset the MCP2515.
        self.cs(0)
        self.spi.write(bytearray([RESET]))
        self.cs(1)

    def read_byte(self, addr):
        # Read a byte from the specified address.
        self.cs(0)
        self.spi.write(bytearray([READ, addr]))
        res = self.spi.read(1)
        self.cs(1)
        return res

    def read_rx_sequence(self, instruction, length):
        # Read a sequence of bytes from an instruction and specified length.
        self.cs(0)
        self.spi.write(bytearray([instruction]))
        res = self.spi.read(length)
        self.cs(1)
        return res

    def write_byte(self, addr, data):
        # Write a byte to the specified address.
        self.cs(0)
        self.spi.write(bytearray([WRITE, addr, data]))
        self.cs(1)

    def write_byte_sequence(self, addr, buf: bytearray):
        # Write a sequence of bytes starting from the specified address.
        self.cs(0)
        self.spi.write(bytearray([WRITE, addr]) + buf)
        self.cs(1)

    def load_tx_sequence(self, instruction, id_reg: bytearray, dlc, buf: bytearray):
        # Load a sequence to transmit in a TX buffer.
        self.cs(0)
        self.spi.write(bytearray([instruction]) + id_reg + bytearray([dlc]) + buf)
        self.cs(1)

    def load_tx_data(self, instruction, data):
        # Load data for transmission into a TX buffer.
        self.cs(0)
        self.spi.write(bytearray([instruction, data]))
        self.cs(1)

    def request_to_send(self, instruction):
        # Send a request to transmit data.
        self.cs(0)
        self.spi.write(bytearray([instruction]))
        self.cs(1)

    def read_status(self):
        # Read the status of the MCP2515.
        self.cs(0)
        self.spi.write(bytearray([READ_STATUS]))
        res = self.spi.read(1)
        self.cs(1)
        return res

    def get_rx_status(self):
        # Get the receive status.
        self.cs(0)
        self.spi.write(bytearray([RX_STATUS]))
        res = self.spi.read(1)
        self.cs(1)
        return res

    def bit_modify(self, address, mask, data):
        self.cs(0)
        self.spi.write(bytearray([BIT_MOD, address, mask, data]))
        self.cs(1)
