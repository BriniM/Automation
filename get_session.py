from fbchat import Client
import json

client = Client('email', 'pass')

file_handle = open('session.txt', 'w+')
file_handle.write(json.dumps(client.getSession()))
file_handle.close()
