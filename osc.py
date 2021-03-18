# Import needed modules from osc4py3
from osc4py3.as_eventloop import *
from osc4py3 import oscbuildparse
import time

# Start the system.
osc_startup()

# Make client channels to send packets.
osc_udp_client("192.168.1.133", 10000, "touchdesigner")

# Build a simple message and send it.
msg = oscbuildparse.OSCMessage("/test/me", ",sif", ["text", 672, 8.871])
osc_send(msg, "touchdesigner")

# Build a message with autodetection of data types, and send it.
msg = oscbuildparse.OSCMessage("/test/me", None, ["text", 672, 8.871])
osc_send(msg, "touchdesigner")

# Buils a complete bundle, and postpone its executions by 10 sec.
exectime = time.time() + 30   # execute in 10 seconds
msg1 = oscbuildparse.OSCMessage("/sound/levels", None, [1, 5, 3])
msg2 = oscbuildparse.OSCMessage("/sound/bits", None, [32])
msg3 = oscbuildparse.OSCMessage("/sound/freq", None, [42000])
bun = oscbuildparse.OSCBundle(oscbuildparse.OSC_IMMEDIATELY ,
                    [msg1, msg2, msg3])
osc_send(bun, "touchdesigner")

# Periodically call osc4py3 processing method in your event loop.
finished = False
while not finished:
    # You can send OSC messages from your event loop too…
    # …
    osc_process()
    msg1 = oscbuildparse.OSCMessage("/sound/levels", None, [1, 5, 3])
    msg2 = oscbuildparse.OSCMessage("/sound/bits", None, [32])
    msg3 = oscbuildparse.OSCMessage("/sound/freq", None, [time.time()*.002])
    bun = oscbuildparse.OSCBundle(oscbuildparse.OSC_IMMEDIATELY ,
                        [msg1, msg2, msg3])
    osc_send(bun, "touchdesigner")
    # …

# Properly close the system.
osc_terminate()