import oppai

import oppai.slack_ctrl as slack_ctrl

from slack_sdk.rtm_v2 import RTMClient
import re

if __name__ == '__main__':
    data = oppai.Data("./data","./private")
    bot = oppai.Bot(data)

    
    l = input()
    while not l is None :
        channel_id = 'channel'
        thread_ts = 'ts'
        user = 'user'
        text = l
        res =  bot.incomming_message(channel_id,user,text)
        if not res is None:
            print (res)

        l = input()
