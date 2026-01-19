
import machine

from ttcontrol import read_rom, dump_state, set_clock_hz

import little_term

def main(tt):

    read_rom()
    dump_state()

    tt.shuttle.tt_um_kianV_rv32ima_uLinux_SoC.enable()
    set_clock_hz(30000000, max_rp2040_freq=200_000_000)

    pin = machine.Pin(1, machine.Pin.OUT)
    pin.value(0)
    pin.value(1)

    little_term.little_term(tt, window_time=400*1000000)
