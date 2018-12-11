# This script will compile a remote repo using the Mbed Remote Compile API
# I dont guarantee this will work, but when it does its smooth as butter


# Input: args dictionary
# clean		- clean build
# platform	- Platform name from os.mbed.com/platforms/ URL
# repo		- repo hosted on os.mbed.com/* (does not work with github links)
# extra_symbols	- dictionary of key:value pairs that are replaced in file as #define key value
# user		- username to compile with
# api 		- API endpoint, default to "https://build.mbed.com"
# pass		- password for user to compile with
# destdir	- destination to save the file to - defaults to current dir
# debug		- debug true or false


"""

Usage example:

python mbedapi.py  --repo http://developer.mbed.org/users/dan/code/pubtest/ --user dan --api http://developer.mbed.org --platform mbed-LPC1768 --destdir /tmp/ --debug 2

#This will compile http://developer.mbed.org/users/dan/code/pubtest/ for the 1768 and download the result.

Examples of options:
--extra_symbols "foo=bar,x=y" 

--replace_file "main.cpp:/tmp/replace_main.cpp"  
(can be repeated)

"""
import os, getpass, sys, json, time, requests, logging

def build_repo(user,password,repo,platform,extra_symbols,clean=False,debug=True,destdir=os.getcwd(),replace_file=False,api="https://build.mbed.com"):
	# set defaults
	if debug:
		logging.basicConfig(level=logging.DEBUG)
	else:
		logging.basicConfig(level=logging.INFO)

	payload = {'clean':clean, 'platform':platform, 'repo':repo, 'extra_symbols': extra_symbols}

	if replace_file:
		replace = []
		for pair in replace_file:
			dest = pair.split(':')[0]
			src = pair.split(':')[1]
			print dest
			cwd = os.getcwd()
			srcfile = open(os.path.join(cwd, src), 'r')
			replace.append({dest:srcfile.read()})

		payload['replace'] = json.dumps(replace)
		logging.debug("Payload is: %s"%payload)

	auth = (user, password)

	#send task to api
	logging.debug(api + "/api/v2/tasks/compiler/start/" + "| data: " + str(payload))
	r = requests.post(api + "/api/v2/tasks/compiler/start/", data=payload, auth=auth)

	logging.debug(r.content)

	if r.status_code != 200:
		print("Error code is %d",r.status_code)
		raise Exception("Error while talking to the mbed API")

	uuid = json.loads(r.content)['result']['data']['task_id']
	logging.debug("Task accepted and given ID: %s"%uuid)
	success = False


	#poll for output
	for check in range(0,40):
		logging.debug("Checking for output: cycle %s of %s"%(check, 10))
		time.sleep(2)
		r = requests.get(api + "/api/v2/tasks/compiler/output/%s"%uuid, auth=auth)
		logging.debug(r.content)
		response = json.loads(r.content)
		messages = response['result']['data']['new_messages']
		percent = 0
		for message in messages:
			if message.get('message'):
				if message.get('type') != 'debug':
					logging.info("[%s] %s"%(message['type'], message['message']))
			if message.get('action'):
				if message.get('percent'):
					percent = message['percent']
				logging.info("[%s%% - %s] %s "%(percent, message['action'], message.get('file', '')))

		if response['result']['data']['task_complete']:
			logging.info("Task completed.")
			success = response['result']['data']['compilation_success']
			logging.info("Compile success: %s"%(success))
			break

	#now download
	if success:
		logging.info("Downloading your binary")
		params = {
				'repomode': True,
				'program': response['result']['data']['program'],
				'binary': response['result']['data']['binary'],
				'task_id': uuid }
		r = requests.get(api + "/api/v2/tasks/compiler/bin/", params=params, auth=auth)
		destination = os.path.join(destdir, response['result']['data']['binary'])

		with open(destination, 'wb') as fd:
			for chunk in r.iter_content(1024):
				fd.write(chunk)

		logging.info("Finished!")

