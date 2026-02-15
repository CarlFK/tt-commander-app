Linux on KianV RISC-V SOC / Tiny Tapeout 6
CLI Style.  No browser needed, maybe.

code version of https://docs.google.com/document/d/1xsKXSyzRcITReSPcTtEUlEqfY_uygV3ntWclOUEb7FA

Step 1 use https://tinytapeout.github.io/tinytapeout-flasher/
(python version of flash spi will be done later)

Step 2: don't use https://commander.tinytapeout.com

```
ttydev=/dev/serial/by-id/usb-MicroPython_Board_in_FS_mode_de640cb1d3975a26-if00
tio ${ttydev} # leave it running.

# in a 2nd shell:
ttydev=/dev/serial/by-id/usb-MicroPython_Board_in_FS_mode_de640cb1d3975a26-if00
python bl.py --throttle 1 --debug --serial-port ${ttydev}
```
bl.py does the following:
reset the rp2040
send ../ttcontrol.py
selets 910: kianV_rv32ima_uLinux_SoC
sets clock to 30 MHz
bounces reset
sends little_term.py - route uPy's stdio to the uart

Now we have:
your ssh client -network- Pi -usb serial- RP2040 -uart serial- TT06 / 910 (KianV Linux)
The Pi is running sshd/tio - this routes your ssh client IO to the RP2040
The RP2040 is runing uP (Micro Python), which is running little_term.py, which routes IO from USB serial to uart serial.

When you hit ^c, that char should get sent from your ssh client all the way to KianV Linux.
by default, ^c will cause uP to raise a KeyboardInterrupt exception.
So this is disabled with micropython.kbd_intr(-1)

little_term.py now breaks on 2 ^c's but the first ^c gets passed on, possibely halting a long running demo.
We all know how to fix this, PR please.
