import commands
class Command(object):

    def add_torrent(self,torrentFilePath):
        commands.getstatusoutput("transmission-remote -n 'transmission:transmission' -a {}".format(torrentFilePath))


    def delete_zeroUp_torrent(self,torrent_id):
        def fo(value):
            if value=='None':
                return 0.
            if 'M' in value:
                value = float(value.split(' ')[0])*1000000
            elif 'G' in value:
                value = float(value.split(' ')[0])*1000000000
            elif 'k' in value or 'K' in value:
                value = float(value.split(' ')[0]) * 1000
            else:
                value=float(value.split(' ')[0])
            return value

        output = commands.getstatusoutput("transmission-remote -n 'transmission:transmission' -t {} -i".format(torrent_id))[1]
        status={}
        for s in output.split('\n'):
            if ':' in s:
                status[s.split(':')[0].strip()]=s.split(':')[1].strip()

        status['Downloaded']=fo(status['Downloaded'])
        status['Uploaded']=fo(status['Uploaded'])
        status['ShareRate']= status['Uploaded']/float(status['Downloaded']) or 0
        if status['Uploaded']==0:
            commands.getstatusoutput("transmission-remote -n 'transmission:transmission' -t {} --remove-and-delete".format(torrent_id))

    def get_torrent_id(self):
        ts = commands.getstatusoutput(
            "transmission-remote -n 'transmission:transmission' -l")[1]
        if ts=='':
            return
        ts = ts.split('\n')
        ts = map(str.strip,ts)[1:-1]
        t_nums=[]
        for t in ts:
            t_nums.append(int(t[:t.find(' ')]))
        return t_nums

    def clear_zeroUp_torrents(self):
        t_nums = self.get_torrent_id()
        map(self.delete_zeroUp_torrent, t_nums)


if __name__=='__main__':
    pass

