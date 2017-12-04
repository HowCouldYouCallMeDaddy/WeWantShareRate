from get_torrents import Torrents
from commend import Command
import time
t = Torrents()
c = Command()
times=0
print "Ready to add torrents to transmission-daemon server..."
while(True):
    path = t()
    if times%10==0:
        print "clear zero upload torrent ~~"
        c.clear_zeroUp_torrents()
    c.add_torrent(path)
    print "add {} torrent".format(times+1)
    times+=1
    time.sleep(60)
c.clear_zeroUp_torrents()
print "Adding all torrents done, see you tomorow!"