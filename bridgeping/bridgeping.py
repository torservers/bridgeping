#!/usr/bin/python3

from stem.control import Controller
from stem import process
from stem.util import term
from sys import argv, exit
from re import match

HELPTEXT="""
Determines wheter a TOR bridge is functional or not
USAGE: %s <IP> <Port>

Prints result on STDOUT
Returns 0 to shell if functional
Returns 1 to shell if not
"""%argv[0]

CONTROL_PORT = 9052

if len(argv) != 3:
    print(HELPTEXT)
    exit(255)

try:
    port = int(argv[2])
    if port < 0 or port > 65535:
        raise ValueError()
except ValueError:
    print (term.format("\nPort needs to be an Integer 0..65535\n", term.Color.RED))
    exit(255)

if not match(r'\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b',argv[1]):    
    print (term.format("\n'%s' does not seem to be a valid IP\n"%argv[1], term.Color.RED))
    exit(255)

path = ["%s:%d"%(argv[1],port)]
try:
    process = process.launch_tor_with_config(config={
            'ControlPort':str(CONTROL_PORT),
            'HashedControlPassword':'16:6EE09FA1A8F1A9FF60356B69F33C5896EE547319832ABC7410C87FF4C4',
            'UseBridges':'1',
            'bridge':"%s:%d"%(argv[1],port)
        }, 
        #init_msg_handler=lambda x: print(x), 
        timeout=10, 
        take_ownership=True)

    controller = Controller.from_port(port=CONTROL_PORT)
    controller.authenticate("test")
except OSError:
    print (term.format("\nThis %s:%d does not seem to be a functional bridge!\n"%
           (argv[1],port),
           term.Color.RED))
else:
    print (term.format("\n%s:%d is a valid bridge.\n"%
           (argv[1],port),
           term.Color.GREEN))
    process.kill()

