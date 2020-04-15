"""
Discord or Slacks similar @everyone feature in Facebook's Messenger!
"""
import json

from fbchat import Client, ThreadType, Message, Mention
from sys import exit


class Everyone(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        self.markAsDelivered(thread_id, message_object.uid)
        self.markAsRead(thread_id)
        
        print("{} from {} in {}".format(message_object, thread_id, thread_type.name))
        
        if thread_type == ThreadType.GROUP and author_id == self.uid and message_object.text.lower() == '@everyone':
            # Gets participants profiles
            friends = self.fetchGroupInfo(thread_id)[thread_id].participants
            friends.remove(author_id)
            friends = self.fetchUserInfo(*friends)

            # Composes the message and the mentions objects.
            msg = ''.join([f'@{p.name} ' for p in friends.values()])
            mentions = [Mention(k, msg.index(f'@{v.name}'), len(v.name) + 1) for k, v in friends.items()]
            self.send(Message(msg, mentions), thread_id, thread_type)


if __name__ == '__main__':
    file_handle = open('session.txt', 'r')

    if file_handle:
        client = Everyone('email', 'password', session_cookies=json.loads(file_handle.read()))

    else:
        print('Error logging in.')
        exit()

    file_handle.close()
    client.listen()
