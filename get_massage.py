import os
import slack
import configdata
import pprint
import json
import time

client = slack.WebClient(configdata.slack_token)

res = client.channels_list()
# pprint.pprint(res.data)
users = {}
if res.data["ok"]:
    for channel in res.data["channels"]:
        ts = None
        flag = True
        c = 0
        while flag:
            time.sleep(1)
            if ts != None:
                history_res = client.channels_history(channel=channel["id"], count=1000, latest=ts)
            if ts == None:
                history_res = client.channels_history(channel=channel["id"], count=1000)
            if history_res.data["ok"]:
                c += len(history_res.data["messages"])
                for message in history_res.data["messages"]:
                    if "text" in message.keys() and "bot_id" not in message.keys():
                        if not("subtype" in message.keys() and message["subtype"] in ["channel_archive","channel_join"]):
                            if message["user"] not in users.keys():
                                users[message["user"]] = []
                            users[message["user"]].append(message["text"])
                if len(history_res.data["messages"]) == 1000:
                    ts = str(float(history_res.data["messages"][-1]["ts"])-0.000001)
                else:
                    flag = False
            print(channel["name"], channel["id"], c)
# pprint.pprint(users)
for user, messages in users.items():
    user_res = client.users_info(user=user)
    fname = user+".txt"
    if user_res.data["ok"]:
        fname = user_res.data["user"]["name"] +" "+ fname
    f = open("text/"+fname, "w", encoding='UTF-8')
    f.write("\n".join(messages))
    f.close()