import os
import random
from flask import Flask, json, request
import requests

from random import randint

app = Flask(__name__)

def reply(message):
	payload = {
		'bot_id' : os.environ['BOT_ID'],
		'text'   : message,
	}
	requests.post('https://api.groupme.com/v3/bots/post', json=payload)

def roll_usage():
	reply("Usage: /roll [max_value [roll_quantity]]")

@app.route('/roll/', methods=['POST'])
def roll_callback():
	json_body = request.get_json()
	if json_body['group_id'] == os.environ['GROUP_ID'] and json_body['sender_type'] != 'bot':
		# some degree of verification that it is sent via a groupme callback
		# could also check for "User-Agent: GroupMeBotNotifier/1.0", but that's plenty spoofable

		message = json_body['text']
		### BOT CODE GOES HERE! ###
		message = message.strip()
		if len(message) > 0 and message[0] == "/":
			# perhaps it is a bot command
			msg_parts = message.split()
			cmd, flags = msg_parts[0].lower(), msg_parts[1:]
			
			# reply("DEBUG: " + repr((cmd, flags)))
			if cmd == "/roll":
				if len(flags) == 1:
					try:
						max_value = int(flags[0])
					except ValueError:
						roll_usage()
						return

					reply( str(randint(1, max_value)) )

				elif len(flags) == 2:
					# /roll [max_value [roll_quantity]]
					try:
						max_value, roll_quantity = map(int, flags)
					except ValueError:
						roll_usage()
						return
					rolls = [randint(1, max_value) for _ in range(roll_quantity)]
					reply( str(rolls)[1:-1] )

				else:
					roll_usage()
					return

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	# app.run(host='0.0.0.0', port=port, debug=True)
	app.run(host='0.0.0.0', port=port)
