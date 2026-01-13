import micropython, ttboard, uselect, sys, utime
from machine import UART

micropython.kbd_intr(-1)

uart = UART(0, baudrate=115200, tx=tt.pins.ui_in3.raw_pin, rx=tt.pins.uo_out4.raw_pin)

poll = uselect.poll()
poll.register(sys.stdin, uselect.POLLIN)

while True:
    try:
        try:
            if poll.poll(0):
                b = sys.stdin.buffer.read(1)
                if b:
                    _ = uart.write(b)
        except Exception:
            pass

        d = uart.read()
        if d:
            _ = sys.stdout.write(d)

        utime.sleep_ms(2)

    except Exception:
        utime.sleep_ms(20)
