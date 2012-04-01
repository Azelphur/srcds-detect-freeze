#!/usr/bin/python

from SourceLib import SourceRcon
import os, time

servers = {
          'Server 1' :
            { 
              'address' : 'Server1.Azelphur.com',
              'port' : 27015,
              'pass' : 'secret',
              'start' : './srcds_run -game tf +maxplayers 32 +map ctf_2fort',
              'stop' : 'screen -S server1 -X quit'
            },
          'Server 2' :
            { 
              'address' : 'Server2.Azelphur.com',
              'port' : 27015,
              'pass' : 'secret',
              'start' : './srcds_run -game tf +maxplayers 32 +map ctf_2fort',
              'stop' : 'screen -S server2 -X quit'
            },
          }

RETRIES = 3
TIME_BETWEEN_RETRIES = 5
USE_TWISTEDCAT = True
TEST_SOURCEMOD = True

def stop(server):
	os.system(servers[server]['stop'])

def start(server):
	os.system(servers[server]['start'])

for server in servers:
	for retry in range(1, RETRIES+1):
		try:
			rcon = SourceRcon.SourceRcon(servers[server]['address'], servers[server]['port'], servers[server]['pass'])
			if TEST_SOURCEMOD and USE_TWISTEDCAT and 'SourceMod Version Information' not in reply:
				reply = rcon.rcon("sm version")
				os.system('echo "%s server failed SourceMod Unit test" | twistedcat' % (server))
			else:
				reply = rcon.rcon("status")
			break
		except:
			if retry == RETRIES:
				if USE_TWISTEDCAT:
					os.system('echo "%s server has stopped responding, restarting it." | twistedcat' % (server))
				stop(server)
				time.sleep(1)
				start(server)
		time.sleep(TIME_BETWEEN_RETRIES)
