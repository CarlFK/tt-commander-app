

code version of https://docs.google.com/document/d/1xsKXSyzRcITReSPcTtEUlEqfY_uygV3ntWclOUEb7FA

Step 1 use https://tinytapeout.github.io/tinytapeout-flasher/
(python version of flash spi will be done later)

Step 2: don't use https://commander.tinytapeout.com

```
tio /dev/ttyACM5 # leave it running.
# in a 2nd shell:
python bl.py --throttle 1 --debug --serial-port /dev/ttyACM5
```
Does the following:
reset
send ../ttcontrol.py
selets 910: kianV_rv32ima_uLinux_SoC
sets clock to 30 MHz
bounces reset
sends little_term.py - the code from the doc

