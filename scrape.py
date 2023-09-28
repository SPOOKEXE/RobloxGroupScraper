import requests
import json

GROUP_SEARCH_URL = "https://groups.roblox.com/v1/groups/search?cursor={}&keyword={}&limit=100&prioritizeExactMatch=true&sortOrder=Asc"

# with open("cookie", "r") as file:
# 	cookie = file.read()

def search_for_group( search_term : str, min_members=-1, max_members=-1, max_groups=-1 ) -> list:
	if max_groups == -1:
		max_groups = 1000

	base_url = GROUP_SEARCH_URL.format( "", search_term )
	groups = []

	HEADERS = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"}

	while len( groups ) < max_groups:
		print(base_url)

		response = requests.get( base_url, headers=HEADERS )
		data = response.json()

		for group_data in data.get("data"):
			memberCount = int( group_data.get("memberCount") )

			if min_members != -1 and memberCount < min_members:
					continue

			if max_members != -1 and memberCount > max_members:
				continue

			if group_data.get("publicEntryAllowed") == False:
				continue

			groups.append( group_data )
			if len( groups ) >= max_groups:
				break

		nextCursor = data.get("nextPageCursor")
		print( nextCursor )
		if nextCursor == None:
			break

		base_url = GROUP_SEARCH_URL.format( nextCursor, search_term )

	return groups

group_data = search_for_group( "SCP", min_members=-1, max_members=1000, max_groups=2500 )

group_links = [ "https://www.roblox.com/groups/" + str(group_dict["id"]) + "/unnamed" for group_dict in group_data ]

with open("data.json", "w") as file:
	file.write( json.dumps( group_data, indent=4 ) )

with open("urls.json", "w") as file:
	file.write( json.dumps( group_links, indent=4 ) )
