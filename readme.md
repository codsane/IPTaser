# IPTaser

## A python script to zap H&R torrents on IPT

## Running
1. Make sure [geckodriver](https://github.com/mozilla/geckodriver/releases) is in PATH
2. Create config.ini with IPT credentials as follows:
	```
	[creds]
	username = asdf
	password = qwertyuiop
	```
3. Understand that you'll probably be banned if you set this up automatically (i.e. only run it when you were going to zap torrents manually anyways; as a time-saver)
4. Run `python IPTaser.py`