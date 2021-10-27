import oppai

import oppai.slack_ctrl as slack_ctrl

from slack_sdk.rtm_v2 import RTMClient
import re

if __name__ == '__main__':
    data = oppai.Data("./data","./private")
    bot = oppai.Bot(data)
    auth_data = slack_ctrl.auth_load(data.conf['slack']['accessToken'])
    # slack read
    rtm = RTMClient(token=data.conf['slack']['accessToken'])

    @rtm.on("message")
    def slack_message_handle(client: RTMClient, event: dict):
        channel_id = event['channel']
        thread_ts = event['ts']
        user = event['user']
        if user == auth_data['user_id']:
            return # self
        if 'text' in event:
            # input
            text = event['text']
            res =  bot.incomming_message(user,text)
            if not res is None:
                client.web_client.chat_postMessage(
                    channel=channel_id,
                    #thread_ts=thread_ts,
                    text=res,
                    as_user=True
                )
    
    rtm.start()
