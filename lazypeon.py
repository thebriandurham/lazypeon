#/bin/python3

# Creator: Brian D ("mox folder")
# 2022-07-14
# v0.0
# License: MIT OSSL

# Imports
import random, sys
from optparse import OptionParser
from colorama import Fore

# Vars
usage = "lazypeon.py -m <mode> <options>"
versionNumber = "0.1"
breaker = Fore.GREEN + "\n\n" + "¤" * 40 + "\n\n" + Fore.WHITE
prompt = Fore.CYAN + "@tlp # " + Fore.WHITE
shellCommands = None
reconCommands = None
miscCommands = None

##### Core Functions

def main():

	printBanner()

	parser = initParser()
	options = (parser.parse_args())[0]
	options = validateOptions(parser,options)

	if options.mode == 'i':
		handleInteractiveMode(options)
	elif options.mode == 's':
		blobShells(options)
	elif options.mode == 'r':
		blobRecon(options)
	elif options.mode == 'm':
		showMiscCommands(options)
	elif options.mode == 'b':
		blobAll(options)
	else:
		parser.error("Unexpected mode value: this should have been caught. pls report <3")

def handleInteractiveMode(options):

	exitCommands = ['q','quit','exit']
	validTargets = ['localhost','localport','targethost','targetport']

	badInputMessage = Fore.YELLOW + "\nUnexpected command, try again bud.\n" + Fore.WHITE
	setErrorNoArgs = Fore.YELLOW + "\nAlert" + Fore.WHITE + ": Set has been called, but no option or value has been provided. Usage: set <option> <value>. See help message for valid options.\n"
	userExitMessage = Fore.RED + '\nUser exit requested. Goodbye!' + Fore.WHITE

	interactiveHelpMessage = Fore.CYAN + "\nAvailable Commands:\n" + Fore.WHITE
	interactiveHelpMessage += Fore.GREEN + "\thelp" + Fore.WHITE + ":\tdisplay this message\n"
	interactiveHelpMessage += Fore.GREEN + "\tmisc" + Fore.WHITE + ":\tshow handy misc. commands\n"
	interactiveHelpMessage += Fore.GREEN +"\treset" + Fore.WHITE + ":\treset all options to default values\n"
	interactiveHelpMessage += Fore.GREEN +"\tset" + Fore.WHITE + ":\tsets stored option value (valid options: localhost, localport, targethost, targetport); example: set localhost 127.0.0.1\n"
	interactiveHelpMessage += Fore.GREEN +"\tblob" + Fore.WHITE + ":\t generate and print all shells, recon commands, and misc commands\n"
	interactiveHelpMessage += Fore.GREEN +"\tblob-shells" + Fore.WHITE + ":\t generate and print all shells\n"
	interactiveHelpMessage += Fore.GREEN +"\tblob-recon" + Fore.WHITE + ":\t generate and print all recon commands\n"
	interactiveHelpMessage += Fore.YELLOW + "\n\tq, quit, exit:" + Fore.WHITE + "\texit TLP\n\n"


	print("Interactive mode enabled, enter" + Fore.YELLOW + " help " + Fore.WHITE + "for list of interactive commands.\n")

	userInput = ""
	while True:
		userInput = (input(prompt).lower()).split(' ')
		if len(userInput) == 1:
			uInput = str(userInput[0]) # don't care if it's redundant, casting to string for sec paranoia
			if uInput == 'help':
				print(interactiveHelpMessage)	
			elif uInput == 'misc':
				showMiscCommands(options)
				print()
			elif uInput == 'reset':
				options = resetOptions(options)
			elif uInput == 'set':
				print(setErrorNoArgs)
			elif uInput == 'blob':
				blobAll(options)
				print()
			elif uInput == 'blob-shells':
				blobShells(options)
			elif uInput == 'blob-recon':
				blobRecon(options)
			elif uInput in exitCommands:
				print(userExitMessage)
				sys.exit(1)
			elif uInput == '':
				print(prompt)
			else:
				print(badInputMessage)
		elif len(userInput) == 2:
			function = userInput[0]
			dataTarget = userInput[1]
			if function == 'set' and dataTarget in validTargets:
				print(Fore.YELLOW + "\nAlert: " + Fore.WHITE + "set has been called on " + Fore.BLUE + dataTarget + Fore.WHITE + ", but no value was given. Usage: set <option> <value>.\n")
			else:
				print(badInputMessage)
			# todo: account for getting individual commands from subsets 
		elif len(userInput) == 3:
			if 'set' not in userInput:
				print(badInputMessage)
			else:
				function = userInput[0]
				dataTarget = userInput[1]
				targetValue = userInput[2]
				if function == "set" and dataTarget in validTargets and targetValue:
					if dataTarget == 'localhost':
						options.localhost = targetValue
					elif dataTarget == 'localport':
						options.localport = targetValue
					elif dataTarget == 'targethost':
						options.targethost = targetValue
					elif dataTarget == 'targetport':
						options.targetport == targetValue
					print("\nValue " + Fore.BLUE + dataTarget + Fore.WHITE + "updated to" + Fore.BLUE + targetValue)
					print(Fore.GREEN + "Current Options: %s\n" % (options) + Fore.WHITE)
				else:
					print(badInputMessage)


def blobAll(options):
	blobRecon(options)
	blobShells(options)
	showMiscCommands(options)

def blobShells(options):
	shellCommands = readFile(options,"reverseshells.txt",True)
	output = Fore.CYAN + "\n[Shells]\n\n" + Fore.WHITE
	for title, shell in shellCommands.items():
		output += Fore.GREEN + title + Fore.WHITE + ":\n%s\n" % (shell.replace("\\n","\n"))
	print(output)

def blobRecon(options):
	reconCommands = readFile(options,"reconcmds.txt",True)
	output = Fore.CYAN + "\n[Recon Commands]\n\n" + Fore.WHITE
	for title, command in reconCommands.items():
		output += Fore.GREEN + title + Fore.WHITE + ":\n%s\n" % (command.replace("\\n","\n"))
	print(output)

def showMiscCommands(options):
	miscCommands = readFile(options,"misc.txt",False)
	print(Fore.CYAN + "\n[Misc Commands]\n" + Fore.WHITE)
	for title,command in miscCommands.items():
		print(Fore.GREEN + title + Fore.WHITE + ":\n" + command) 

##### End Core Functions

##### Init Functions

def initParser():
	parser = OptionParser(usage)

	parser.add_option(
		"-m",
		"--mode",
		type="string",
		dest="mode",
		help="Set TLP mode. Modes(i=interactive, b=blob [generate & print everything], s=shellsOnly [shell cheats only], r=reconOnly [recon cheats only]. Defaults to interactive if not provided, m=misc [non-targeted helpful commands]",
		default='i')

	parser.add_option(
		"--targethost",
		type="string",
		dest="targethost",
		help="Set target IP; non-interactive")
	
	parser.add_option(
		"--targetport",
		type="string",
		dest="targetport",
		help="Set target port; non-interactive")

	parser.add_option(
		"--localhost",
		type="string",
		dest="localhost",
		help="Set your local IP; non-interactive")

	parser.add_option(
		"--localport",
		type="string",
		dest="localport",
		help="Set your local port; non-interactive")

	return parser

##### Misc Functions

def printBanner():

	# todo
	# use text formatting here instead of concat
	versionText = "The Lazy Peon :: v" + versionNumber
	creatorText = "Created by: Brian D (Mox Folder)"
	cheekyText = "File complaints here: twitter@mox_folder_"

	quotes = [
	'Yes?',
	'What you want?',
	'What...?',
	'Me busy, leave me alone!',
	'Me not that kind of orc!',
	'Work, work.',
	'Okie Dokie',
	'Something need doing?'
	'I can do that',
	'Be happy to',
	'Ok!',
	'Kill \'em!',
	'I\'ll try...',
	'Why not?!',
	'Whaaaat?',
	'No time for play'
	]

	quote = quotes[random.randint(0,len(quotes)-1)]
	print(breaker + Fore.MAGENTA + "\t" + quote + breaker)
	print(Fore.BLUE + versionText)
	print(creatorText)
	print(cheekyText + '\n' + Fore.WHITE)

def resetOptions(options):
	options.localhost = "localhost"
	options.localport = str(0)
	options.targethost = "X.X.X.X"
	options.targetport = str(0)

	print(Fore.YELLOW + "\nAlert" + Fore.WHITE + ": options values have been reset to their defaults!")
	print(Fore.GREEN + str(options) + '\n' + Fore.WHITE)

	return options

##### End Misc Functions

##### File Read Functions

def readFile(options, path, replaceDorks):
	hostDork = None
	portDork = None

	data = {}
	file = open(path,'r')
	lines = file.readlines()
	file.close()

	for line in lines:
		if (path == "reverseshells.txt"):
			split = line.split('z')
			# using z as delimitter here as it's very hard to find a special char that's not used in these
		else:
			split = line.split(',')
		data[split[0]] = split[1]

	if replaceDorks:
		for title,datum in data.items():
			if path == "reverseshells.txt":
				datum = datum.replace('$HOST$',options.localhost)
				datum = datum.replace('$PORT$',options.localport)
			elif path == "reconcmds.txt":
				datum = datum.replace('$HOST$',options.targethost)
				datum = datum.replace('$PORT$',options.targetport)
			data[title] = datum

	return data

def getShellCodes(options):
	commands = {}
	path = "reverseshells.txt"

	file = open(path,'r')
	lines = file.readlines()
	file.close()

	for line in lines:
		split = line.split(',')
		commands[split[0]] = split[1]

	for title,command in commands.items():
		command = command.replace('$HOST$',options.localhost)
		command = command.replace('$PORT$',options.localport)
		commands[title] = command

	# note: when finally displaying these commands to the user, you must call $string$.replace("\\n","\n") to have newlines actually print

	return commands

def getReconCommands(options):
	commands = {}
	path = "reconcmds.txt"

	file = open(path,'r')
	lines = file.readlines()
	file.close()

	for line in lines:
		split = line.split(',')
		commands[split[0]]=split[1]

	for title,command in commands.items():
		command = command.replace('$HOST$',options.targethost)
		command = command.replace('$PORT$',options.targetport)
		commands[title] = command

	return commands

def getMiscCommands():
	commands = {}
	path = "misc.txt"

	file = open(path,'r')
	lines = file.readlines()
	file.close()

	for line in lines:
		split = line.split(',')
		commands[split[0]] = split[1]

	return commands

##### Validation Functions 

def validateShellsOptions(options):
	if not options.localhost:
		print(Fore.YELLOW + "ShellsWarning" + Fore.WHITE + ": localhost not provided, generators will use default value of 'localhost'")
		options.localhost = "localhost"
	if not options.localport:
		print(Fore.YELLOW + "ShellsWarning" + Fore.WHITE + ": localport not provided, generators will use default value of '0'")
		options.localport = str(0)
	return options

def validateReconOptions(options):
	if not options.targethost:
		print(Fore.YELLOW + "BlobWarning" + Fore.WHITE + ": targethost not provided, generators will use default value of 'X.X.X.X")
		options.targethost = "X.X.X.X"
	if not options.targetport:
		print(Fore.YELLOW + Fore.YELLOW + "BlobWarning" + Fore.WHITE + ": targetport not provided, generators will use default value of '0'")
		options.targetport = str(0)
	return options

def validateOptions(parser,options):

	modeDescriptors = {
		'i':'interactive',
		'b':'blob',
		's':'shells',
		'r':'recon',
		'm':'misc'
	}

	validModes = ['i','b','s','r']

	if options.mode and options.mode in modeDescriptors.keys():
		print("Mode set:" + Fore.CYAN + " %s" % (modeDescriptors[options.mode]) + Fore.WHITE )
	else:
		parser.error(Fore.RED + "Invalid flag set for mode. Valid modes: i, b, s, r, m" + Fore.WHITE)
	
	if options.mode == 'i':
		options = validateShellsOptions(options)
		options = validateReconOptions(options)
		pass
	elif options.mode == 'b':
		options = validateShellsOptions(options)
		options = validateReconOptions(options)
	elif options.mode == 's':
		options = validateShellsOptions(options)
	elif options.mode == 'r':
		options = validateReconOptions(options)

	print(Fore.GREEN + "Current Options: " + str(options) + Fore.WHITE)
	return options

##### End Validation Functions

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print(Fore.RED + 'User initiated interrupt. Goodbye!' + Fore.WHITE)
		sys.exit(0)
