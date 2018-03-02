#!/usr/bin/python

import os
import sys
import subprocess

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#Pseudocode
def getGreps(ip):
    y = []
    ip = str(ip)
    cidr = ip.split('/')
    snet = cidr[0]
    snet = snet.split('.')
    usableRange = 2**(32 - int(cidr[1]))
    for x in range(usableRange): #iterate grep over subnet range
        last = int(snet[3]) + x #prompt display is echo $USER$HOSTNAME$PWD'$'
        grepip = snet[0] + '.' + snet[1] + '.' + snet[2] + '.' + str(last)
        y.append("grep %s /tftpboot/autodl/*.cf" % (grepip))
    return y # y is list of grep commands to run per subnet

#execute greps
def execGreps(greps, output):
    grepout = output
    for command in greps:
        try:
            grepout = grepout + "\n" + command + "\n" + bcolors.WARNING + subprocess.check_output(command, shell=True) + bcolors.ENDC
        except:
            grepout = grepout + command + "\n"
    return grepout

#login to public edge and perform sh ip route and sh ip bgp
def ipRoute(ip):
    ip = ip.split('/')
    os.system('echo "show ip route %s" >> commands;echo "show ip bgp %s/22 longer-prefixes" >>commands' % (ip[0],ip[0]))

def __init__():
    greps = ''
    for arg in sys.argv:
        if arg == sys.argv[0]:
            print " "
        else:
            greps = execGreps(getGreps(str(arg)), greps)
            ipRoute(str(arg))
        #display output
    print greps
    os.system('echo exit >> commands;cat commands | ssh $USER@jfk-edge-19 >> output')
    os.system('cat output')
    #cleanup
    os.system('rm commands; rm output')

__init__()
