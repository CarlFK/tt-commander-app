import micropython, ttboard, uselect, sys, utime
from machine import UART

def little_term( tt, window_time=400*1000000):

    # don't halt on ^c (or any other char)
    micropython.kbd_intr(-1)

    # get ready to halt on 2 ^c in the window
    last_char,last_time = None,None

    uart = UART(0, baudrate=115200, tx=tt.pins.ui_in3.raw_pin, rx=tt.pins.uo_out4.raw_pin)

    poll = uselect.poll()
    poll.register(sys.stdin, uselect.POLLIN)

    while True:
        try:
            try:
                if poll.poll(0):

                    b = sys.stdin.buffer.read(1)

                    if b:

                        # if ^c
                        if b==b'\x03':
                            # if first time here, skip check for ^c^c.
                            if last_char is not None and \
                               last_char == b and \
                               utime.time_ns()-last_time < window_time:
                                   print("little_term exit.")
                                   print("import little_term; little_term.little_term(tt, window_time=400*1000000)")
                                   raise KeyboardInterrupt

                        last_char,last_time = b,utime.time_ns()

                        # send the char to uart
                        uart.write(b)

            except Exception as e:
                print(f"{e=}")
                pass

            d = uart.read()
            if d:
                sys.stdout.write(d)

            utime.sleep_ms(2)

        except Exception as e:
            print(f"{e=}")
            utime.sleep_ms(20)

def go():

    import main
    tt = main.DemoBoard.get()

    print("calling little_term(tt, window_time=400*1000000)")
    little_term(tt, window_time=400*1000000)


if __name__=="__main__":
    go()
else:
    print("little_term.go()")

    # little_term(tt, True) # NameError: name 'tt' isn't defined
    print("little_term.little_term(tt, window_time=400*1000000)")



