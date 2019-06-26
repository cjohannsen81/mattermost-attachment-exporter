import requests
import json

url = "http://3.80.208.135:8065"
auth_token = ""
login_url = url+"/api/v4/users/login"

payload = { "login_id": "admin@mattermost.com",
            "password": "MattermostDemo,1"}
headers = {"content-type": "application/json"}
s = requests.Session()
r = s.post(login_url, data=json.dumps(payload), headers=headers)
auth_token = r.headers.get("Token")
hed = {'Authorization': 'Bearer ' + auth_token}

#team_name= raw_input("Please enter the team name (lowercase, no blanks): ")
team_name = "demoteam"
#channel_name = raw_input("Please enter the channel name to check (lowercase, no blanks): ")
channel_name = "testexport"

files = []

def get_team_id():
    team_url = url+"/api/v4/teams/search"
    payload = { "term": team_name}
    response = requests.post(team_url, headers=hed, json=payload)
    info = response.json()
    print("Found team" + info[0]["name"])
    team_id = info[0]["id"]
    get_channel_id(team_id)

def get_channel_id(team_id):
    team_url = url+"/api/v4/teams/"+team_id+"/channels/search"
    payload = { "term": channel_name}
    response = requests.post(team_url, headers=hed, json=payload)
    info = response.json()
    print("Found channel" + info[0]["name"])
    channel_id = info[0]["id"]
    get_posts(channel_id)

def get_posts(channel_id):
    team_url = url+"/api/v4/channels/"+channel_id+"/posts"
    response = requests.get(team_url, headers=hed)
    info = response.json()
    for k, v in info['posts'].items():
        for k, v in v.items():
            if k == "file_ids":
                for fileid in v:
                    files.append(fileid)

def get_uploads(files):
    for id in files:
        info_url = url+"/api/v4/files/" + id + '/info'
        response = requests.get(info_url, headers=hed)
        info = response.json()
        filename = info["name"]

        file_url = url+"/api/v4/files/" + id
        response = requests.get(file_url, headers=hed)
        open(filename, 'wb').write(response.content)

get_team_id()
get_uploads(files)
