import subprocess, time
from rich import print
from rich.panel import Panel
from rich.console import Console
from rich.text import Text


class Fprobe:
	def __init__(self,url):
		self.url = url
		
	def fetchingInfos(self):
		cmd1 = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "-show_entries", "format=icy", "-pretty", self.url]
		
		try:			#print(streamInfos)
					#print(streamInfos['format']['tags']['StreamTitle'])
			while True:
				dataProc = subprocess.check_output(cmd1)
				streamInfos = json.loads(dataProc)
				streamTitle = streamInfos['format']['tags']['StreamTitle']
				userResponse = console.input("[bold red] Want playing song infos[/] (y/n) ")
				if(userResponse == 'y'):
					if(streamTitle):
						print(f" {streamTitle}")
					else:
						print(' Unknow Song')
				else:
					print(' You can try again')
				time.sleep(5)
					
		except:
			dataProc.kill()

