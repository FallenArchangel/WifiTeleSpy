# WifiTeleSpy
# Made by Fallen Archangel to scan for wifi enabled devices.
# https://github.com/FallenArchangel/WifiTeleSpy
import os
import subprocess
import telegram
import time
from urllib2 import URLError


def loadconfig(line):
    configfile = open("settings.conf").read().splitlines()
    return configfile[int(line)-1].strip()


# Opens 'Known.txt' to build known devices dictionary.
def readknown(filename="Known.txt"):
    privateknownmacs = {}
    with open(filename, "r") as cache:
        # read file into a list of lines
        lines = cache.readlines()
        # loop through lines
        for line in lines:
            # skip lines starting with "--".
            if not line.startswith("--"):
                line = line.strip().split(" ")
                # use first item in list for the key, join remaining list items
                # with ", " for the value.
                privateknownmacs[line[0]] = ", ".join(line[1:])

    return privateknownmacs


# Checks if MACs.txt exists.
# Calls getscannedmacs if it does.
def checkformacs():
    filename = "MACs.txt"
    if os.path.isfile(filename):
        return getscannedmacs()
    else:
        print("MACs.txt does not exist.")


# Reads every line from MACs.txt into a list.
# Makes variable 'macs' which contains a list without duplicates
def getscannedmacs():
    originalmacs = open("MACs.txt").read().splitlines()
    macs = list(set(originalmacs))
    return parsemacs(macs)


# Takes list of MACs and compares them to dictionary. Replaces with hostname if known.
def parsemacs(unparsedmacs):
    knownmacs = readknown()
    devicesinrange = []
    for x in range(0, len(unparsedmacs)):
        try:
            devicesinrange.append(knownmacs[unparsedmacs[x]])
        except KeyError:
            devicesinrange.append(unparsedmacs[x])
    devicesinrange.append(" ")
    devicesinrangestring = "\n".join(devicesinrange)
    return devicesinrangestring


def start():
    cmd = ['ifconfig']
    if subprocess.check_output(cmd).decode().find(loadconfig(3) + "mon") == -1:
        print loadconfig(3) + "1mon not found, launching airmon, waiting 30 seconds, and restarting"
        os.system("sudo airmon-ng start " + loadconfig(3))
        time.sleep(30)
        start()
    else:
        print loadconfig(3)+"mon found, starting scan"
        return scan()


def scan():
    try:
        os.remove('MACs.txt')
    except OSError:
        pass
    os.system('tshark -Q -l -i ' + loadconfig(3) + 'mon -T fields -e wlan.sa -a duration:' + loadconfig(6) + ' |'
              ' grep -ioE \'([a-z0-9]{2}:){5}..\' >> MACs.txt')
    return checkformacs()


# Function: manages WifiTeleSpy bot
# Params: bot object and update ID
# Return: update ID
def WifiTeleSpyBot(bot, update_id):
    for update in bot.getUpdates(offset=update_id, timeout=10):
        chat_id = update.message.chat_id
        update_id = update.update_id + 1
        message = update.message.text
        if message:
            CheckAndAnswer(message, bot, chat_id)
            # CheckAndAnswer(message, bot, chat_id)
    return update_id
# WifiTeleSpy
# Made by Fallen Archangel to scan for wifi devices.
# https://github.com/FallenArchangel/WifiTeleSpy


# Function: check message rec. and answer it (if it's needed)
# Params: message, bot telegram object and Telegram chat ID
# Return: none
def CheckAndAnswer(Msg,BotObj,ChatID):
    MsgLowerCase = Msg.lower()
    if MsgLowerCase == "/start":
        print "/start command received"
        BotObj.sendMessage(chat_id=ChatID, text="Hey there! Would you like to scan for devices? (Type Yes, or /scan)")
        return
    if (MsgLowerCase == "yes") or (MsgLowerCase == "/scan"):
        print "/scan command received, scanning for " + loadconfig(6) + " seconds."
        devicesinrange = start()
        print "Scan complete"
        try:
            BotObj.sendMessage(chat_id=ChatID, text="Scan complete: \n" + devicesinrange)
        except TypeError:
            BotObj.sendMessage(chat_id=ChatID, text="Scan complete: \n" + "No devices found")
        return


# Telegram stuff I don't yet understand
# MAIN PROGRAM
update_id = None

# Telegram API Token. Get yours with BotFather!
BotToken = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

bot = telegram.Bot(BotToken)
print 'WifiTeleSpy started!'

while True:
        try:
            update_id = WifiTeleSpyBot(bot, update_id)
        except telegram.TelegramError as e:
            if e.message in ("Bad Gateway", "Timed out"):
                sleep(1)
            else:
                raise e
        except URLError as e:
            sleep(1)
