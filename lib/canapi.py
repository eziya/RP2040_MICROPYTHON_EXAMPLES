#!/usr/bin/env python
# -*- coding: utf-8 -*-
# canapi.py

import mcp2515
import time

# Constants for CAN message ID types
STANDARD_CAN_MSG_ID_2_0B = 1
EXTENDED_CAN_MSG_ID_2_0B = 2

class CANAPI:
    def __init__(self):
        # Initialize the MCP2515 instance
        self.mcp2515 = mcp2515.MCP2515()
        self.mcp2515.reset()
        time.sleep(0.1)

        # Set MCP2515 to Configuration mode
        if not self.mcp2515.set_config_mode():
            print("mcp2515.set_config_mode() failed.\n")

        # Initialize RX mask filters
        self.init_rx_mask_filters()

        # Initialize RX message filters
        self.init_rx_message_filters()

        # Configure RXB0 and RXB1 to accept specific message types
        self.mcp2515.write_byte(mcp2515.RXB0CTRL, 0x04)  # Accept All (Standard + Extended ID)
        self.mcp2515.write_byte(mcp2515.RXB1CTRL, 0x01)  # Accept only Extended ID

        # Configure the baud rate
        self.configure_baud_rate()

        # Set MCP2515 to Normal mode
        if not self.mcp2515.set_normal_mode():
            print("mcp2515.set_normal_mode() failed.\n")

    def init_rx_mask_filters(self):
        # Configure RXM0 and RXM1 mask filters
        self.mcp2515.write_byte(mcp2515.RXM0SIDH, 0x00)
        self.mcp2515.write_byte(mcp2515.RXM0SIDL, 0x00)
        self.mcp2515.write_byte(mcp2515.RXM0EID8, 0x00)
        self.mcp2515.write_byte(mcp2515.RXM0EID0, 0x00)

        self.mcp2515.write_byte(mcp2515.RXM1SIDH, 0x00)
        self.mcp2515.write_byte(mcp2515.RXM1SIDL, 0x08)
        self.mcp2515.write_byte(mcp2515.RXM1EID8, 0x00)
        self.mcp2515.write_byte(mcp2515.RXM1EID0, 0x00)

    def init_rx_message_filters(self):
        filter0_2 = [
            (0, 0x00, 0x00, 0x00, 0x00),  # Accept Standard ID
            (1, 0x00, 0x08, 0x00, 0x00),  # Accept Extended ID
            (2, 0x00, 0x00, 0x00, 0x00),  # Accept Standard ID
        ]

        filter3_5 = [
            (0, 0x00, 0x08, 0x00, 0x00),  # Accept Extended ID
            (1, 0x00, 0x00, 0x00, 0x00),  # Accept Standard ID
            (2, 0x00, 0x08, 0x00, 0x00),  # Accept Extended ID
        ]

        for index, sidh, sidl, eid8, eid0 in filter0_2:
            # Configure RX message filters
            self.mcp2515.write_byte(mcp2515.RXF0SIDH + 4 * index, sidh)
            self.mcp2515.write_byte(mcp2515.RXF0SIDL + 4 * index, sidl)
            self.mcp2515.write_byte(mcp2515.RXF0EID8 + 4 * index, eid8)
            self.mcp2515.write_byte(mcp2515.RXF0EID0 + 4 * index, eid0)

        for index, sidh, sidl, eid8, eid0 in filter3_5:
            # Configure RX message filters
            self.mcp2515.write_byte(mcp2515.RXF3SIDH + 4 * index, sidh)
            self.mcp2515.write_byte(mcp2515.RXF3SIDL + 4 * index, sidl)
            self.mcp2515.write_byte(mcp2515.RXF3EID8 + 4 * index, eid8)
            self.mcp2515.write_byte(mcp2515.RXF3EID0 + 4 * index, eid0)

    def configure_baud_rate(self):
        # Configure CAN bus baud rate settings
        # tq = 2 * (brp(0) + 1) / 16000000 = 0.125us
        # 1tq(SYN) + 5tq(PROP) + 7tq(PS1) + 3tq(PS2) = 16tq = 2us = 500kbps
        # SJW: 3tq
        self.mcp2515.write_byte(mcp2515.CNF1, 0x80)
        self.mcp2515.write_byte(mcp2515.CNF2, 0xE6)
        self.mcp2515.write_byte(mcp2515.CNF3, 0x82)

    def sleep(self):
        # Set MCP2515 to Sleep mode
        self.mcp2515.bit_modify(mcp2515.CANINTF, 0x40, 0x00)
        self.mcp2515.bit_modify(mcp2515.CANINTE, 0x40, 0x40)
        self.mcp2515.set_sleep_mode()

    def transmit(self, can_id, id_type, dlc, msg):
        # Transmit a CAN message
        status = self.mcp2515.read_status()
        regs = self.convert_can_id_to_reg(can_id, id_type)

        if (status & 0x04) == 0:
            self.transmit_message(regs, dlc, msg, mcp2515.LOAD_TXB0SIDH, mcp2515.RTS_TX0)
        elif (status & 0x10) == 0:
            self.transmit_message(regs, dlc, msg, mcp2515.LOAD_TXB1SIDH, mcp2515.RTS_TX1)
        elif (status & 0x40) == 0:
            self.transmit_message(regs, dlc, msg, mcp2515.LOAD_TXB2SIDH, mcp2515.RTS_TX2)

    def transmit_message(self, regs, dlc, msg, instruction, rts_flag):
        # Transmit a CAN message using the specified TX buffer
        self.mcp2515.load_tx_sequence(instruction, regs, dlc, msg)
        self.mcp2515.request_to_send(rts_flag)

    def receive(self):
        # Receive and decode a CAN message
        id_type, can_id, dlc, data0, data1, data2, data3, data4, data5, data6, data7 = self.decode_received_message()
        return [id_type, can_id, dlc, data0, data1, data2, data3, data4, data5, data6, data7]

    def decode_received_message(self):
        # Decode a received CAN message
        rx_status = self.mcp2515.get_rx_status()
        regs = []

        if (rx_status & 0xC0) == 0x40 or (rx_status & 0xC0) == 0xC0:
            # Message in RXB0 or both(RXB0, RXB1)
            regs = self.mcp2515.read_rx_sequence(mcp2515.RXB0SIDH, 13)
        elif (rx_status & 0xC0) == 0x80:
            # Message in RXB1
            regs = self.mcp2515.read_rx_sequence(mcp2515.RXB1SIDH, 13)

        id_type, can_id, dlc, data0, data1, data2, data3, data4, data5, data6, data7 = self.decode_can_id_registers(regs)
        return id_type, can_id, dlc, data0, data1, data2, data3, data4, data5, data6, data7

    def decode_can_id_registers(self, regs):
        # Decode message registers into ID type, CAN ID, DLC, and data
        id_type, can_id, dlc, data0, data1, data2, data3, data4, data5, data6, data7 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

        if (regs[4] & 0x10) == 0x0:
            id_type = STANDARD_CAN_MSG_ID_2_0B
            can_id = self.convert_reg_to_standard_can_id(regs[0], regs[1])
        elif (regs[4] & 0x10) == 0x10:
            id_type = EXTENDED_CAN_MSG_ID_2_0B
            can_id = self.convert_reg_to_extended_can_id(regs[2], regs[3], regs[0], regs[1])

        dlc = regs[4]
        data0, data1, data2, data3, data4, data5, data6, data7 = regs[5], regs[6], regs[7], regs[8], regs[9], regs[10], regs[11], regs[12]

        return id_type, can_id, dlc, data0, data1, data2, data3, data4, data5, data6, data7

    def get_message_in_buffer(self):
        # Get the number of messages in the receive buffer
        status = self.mcp2515.read_status()
        message_count = (status & 0x03)
        return message_count

    def is_bus_off(self):
        # Check if the CAN bus is off
        err_status = self.mcp2515.read_byte(mcp2515.EFLG)
        return (err_status & 0x20) != 0

    def is_rx_error_passive(self):
        # Check if the CAN controller is in RX error passive state
        err_status = self.mcp2515.read_byte(mcp2515.EFLG)
        return (err_status & 0x08) != 0

    def is_tx_error_passive(self):
        # Check if the CAN controller is in TX error passive state
        err_status = self.mcp2515.read_byte(mcp2515.EFLG)
        return (err_status & 0x10) != 0

    def convert_can_id_to_reg(self, can_id, id_type):
        # Convert CAN ID and ID type to register values
        temp_sidl = temp_sidh = temp_eid0 = temp_eid8 = 0

        if id_type == EXTENDED_CAN_MSG_ID_2_0B:
            temp_eid0 = 0xFF & can_id
            can_id = can_id >> 8
            temp_eid8 = 0xFF & can_id
            can_id = can_id >> 8
            temp_sidl = 0x03 & can_id
            can_id = can_id << 3
            temp_sidl = (0xE0 & can_id) + temp_sidl
            temp_sidl = temp_sidl + 0x08
            temp_sidl = 0xEB & temp_sidl
            can_id = can_id >> 8
            temp_sidh = 0xFF & can_id
        else:
            temp_eid8 = 0
            temp_eid0 = 0
            can_id = can_id << 5
            temp_sidl = 0xFF & can_id
            can_id = can_id >> 8
            temp_sidh = 0xFF & can_id

        return bytearray([temp_sidh, temp_sidl, temp_eid8, temp_eid0])

    def convert_reg_to_standard_can_id(self, sidh, sidl):
        # Convert register values to a standard CAN ID
        return (sidh << 3) + (sidl >> 5)

    def convert_reg_to_extended_can_id(self, eid8, eid0, sidh, sidl):
        # Convert register values to an extended CAN ID
        can_standard_id_lo_2_bits = (sidl & 0x03)
        can_standard_id_hi_3_bits = (sidl >> 5)
        converted_id = (sidh << 3)
        converted_id = converted_id + can_standard_id_hi_3_bits
        converted_id = (converted_id << 2)
        converted_id = converted_id + can_standard_id_lo_2_bits
        converted_id = (converted_id << 8)
        converted_id = converted_id + eid8
        converted_id = (converted_id << 8)
        converted_id = converted_id + eid0

        return converted_id
