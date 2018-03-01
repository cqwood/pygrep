

import os
import sys
import subprocess

#Pseudocode
def getGreps(ip):
        y = []
        ip = str(ip)
        cidr = ip.split('/')
        snet = cidr[0]
        snet = snet.split('.')
        usableRange = 2**(32 - int(cidr[1]))
        for x in range(usableRange): #iterate grep over subnet range
                last = int(snet[3]) + x
                #prompt display is echo $USER$HOSTNAME$PWD'$'
                grepip = snet[0] + '.' + snet[1] + '.' + snet[2] + '.' + str(last)
                y.append("grep %s /tftpboot/autodl/*.cf" % (grepip))
        return y # y is list of grep commands to run per subnet

#execute greps
def execGreps(greps):
        for command in greps:
                grepout = command + "\n" + os.system(command) + '\n'
        return grepout

#login to public edge and perform sh ip route and sh ip bgp
def ipRoute(ip):
       ip = ip.split('/')
       os.system('echo "show ip route %s" >> commands;echo "show ip bgp %s/22 longer-prefixes" >>commands' % (ip[0],ip[0]))

def __init__():
        for arg in sys.argv:
                if arg == sys.argv[0]:
                        print " "
                else:
                        greps = execGreps(getGreps(str(arg)))
                        ipRoute(str(arg))
        #display output
        print greps
        os.system('echo exit >> commands;cat commands | ssh $USER@jfk-edge-19 >> output')
        os.system('cat output')
        #cleanup
        os.system('rm grepout; rm commands; rm output')

__init__()
