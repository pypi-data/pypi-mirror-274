import subprocess
import json
import time
from rich import print
from rich.panel import Panel
from rich.console import Console
from rich.text import Text



class Fplay:

	def __init__(self,url,name):
		self.url = url
		self.name = name

	def handlePlaying(self):
		cmd = ["ffplay", "-nodisp", "-i", "-loglevel", "quiet", "-vn", self.url]
		cmd1 = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "-show_entries", "format=icy", "-pretty", self.url]
		
		try:
			console = Console()
			panel = Panel(Text(f"{self.name}",justify="center"), title= ":play_button:[bold yellow] Playing Now", subtitle= "[blink]:radio:", title_align="center", width=83)
			console.print(panel)
			playingProc = subprocess.Popen(cmd, shell=False)
			try:
				while True:
					streamTitle = ''
					dataProc = subprocess.check_output(cmd1)
					streamInfos = json.loads(dataProc)
					streamTitle = streamInfos['format']['tags']['StreamTitle']
					userResponse = console.input("[bold red] Want playing song infos[/] (y/n) ")
					if(userResponse == 'y'):
						if(streamTitle):
                           				print(f" Track title 🎶: [bold]{streamTitle}")
						else:
							print(' Unknow Song')

					else:
						print(' You can try again')
					time.sleep(5)
			except:
				dataProc.kill()


		except:
			print("Exit Playing Radio")
			playingProc.kill()


