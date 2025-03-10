# bl.py - Boot Linux from tt-06

import argparse

import serial

from time import sleep


class uPy_com:
    """
    TT-MicroPython commander
    """

    def __init__(self, serial_port, throttle, debug):
        self.debug = debug
        self.throttle = throttle
        self.serial = serial.Serial(serial_port, timeout=0.1)

    def write(self, bytes_):
        if self.debug:
            print(bytes_)
        self.serial.write(bytes_)
        sleep(self.throttle)
        rx = self.serial.readline().decode(errors="replace").strip()
        print(rx)
        sleep(self.throttle)

    def send_file(self, file_name):
        ttCpy = open(file_name).read()
        self.write(ttCpy.encode())

    def sendCommand(self, command):
        self.write(str(command).encode() + b"\x04")

    def syncState(self):
        self.sendCommand("dump_state()")

    def btn_reset(self):
        self.write(b"\x03")
        self.sendCommand("pin = machine.Pin(1, machine.Pin.OUT)")
        self.sendCommand("pin.value(0)")
        self.sendCommand("pin.value(1)")
        sleep(4)

    def init_tt(self):

        # from ../TTBoardDevice.ts
        """
          // The following sequence tries to ensure clean reboot:
          // Send Ctrl+C twice to stop any running program,
          // followed by Ctrl+B to exit RAW REPL mode (if it was entered),
          // and finally Ctrl+D to soft reset the board.
          await this.writer.write('\x03\x03\x02');
          await this.writer.write('\x04');
        }
        await this.writer.write('\x01'); // Send Ctrl+A to enter RAW REPL mode.
        await this.writer.write(ttControl + '\x04'); // Send the ttcontrol.py script and execute it.
        await this.sendCommand('read_rom()');
        await this.syncState();
        """
        self.write(b"\x03\x03\x02")
        self.write(b"\x04")

        self.write(b"\x01")
        self.send_file("../ttcontrol.py")
        self.write(b"\x04")
        sleep(8)

        self.sendCommand("read_rom()")
        self.syncState()


def get_args():

    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument(
        "-c",
        "--serial-port",
        default="/dev/ttyACM4",
        dest="serial_port",
        help="the serial port",
    )

    parser.add_argument(
        "-t", "--throttle", default=0.1, type=float, help="delay between lines"
    )
    parser.add_argument("-d", "--debug", action="store_true")

    args = parser.parse_args()

    return args


def main():

    args = get_args()

    # open serial connection from host to RP2040
    upc = uPy_com(args.serial_port, args.throttle, args.debug)

    # Init the TT board
    upc.init_tt()

    # Selet the  KianV RISC-V SOC project:
    # Command from commander app:
    # upc.sendCommand("select_design(910, 0)")
    # same thing, nicer looking:
    upc.sendCommand("tt.shuttle.tt_um_kianV_rv32ima_uLinux_SoC.enable()")

    # set clock to 30 MHz
    upc.sendCommand("set_clock_hz(30000000, max_rp2040_freq=200_000_000)")

    # Press reset button
    upc.btn_reset()

    # route the rp2040's tx/rx to SoC tx/rx
    upc.write(b"\x02")
    upc.write(b"\x05")
    upc.send_file("little_term.py")
    upc.write(b"\x04")


if __name__ == "__main__":
    main()
