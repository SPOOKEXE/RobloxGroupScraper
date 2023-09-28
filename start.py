
import os
import json

with open("urls.json", "r") as file:
	data = json.loads(file.read())

def start_sessions( start : int, count : int ) -> None:
	for url in data[start:start+count]:
		os.system("start " + url)

start_sessions( 0, 25 )
