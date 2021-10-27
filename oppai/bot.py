
class Bot:
    def __init__(self,data):
        pass

    def incomming_message(self,user,message):
        if not 'おっぱい' in message and not 'oppai' in message:
            return None
        return 'おっぱいpong:' + message


