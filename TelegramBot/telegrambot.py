import telegram			
from time import sleep 
from urllib2 import URLError
from random import randint

#global variables
PiFactsCollection = []

#Function: manages PI Telegram bot
#Params: bot object and update ID
#Return: update ID
def PIBot(bot, update_id):
    for update in bot.getUpdates(offset=update_id, timeout=10):
        chat_id = update.message.chat_id
        update_id = update.update_id + 1
        message = update.message.text

        if message:
           CheckAndAnswer(message, bot, chat_id) 
		

    return update_id

#Function: check message rec. and answer it (if it's needed)
#Params: message, bot telegram object and Telegram chat ID
#Return: none
def CheckAndAnswer(Msg,BotObj,ChatID):
	MsgLowerCase = Msg.lower()

	if (MsgLowerCase == "hi"):
		BotObj.sendMessage(chat_id=ChatID, text="Hi there! Do you wanna know more about PI? Type yes or facts words.")
		return

	if ((MsgLowerCase == "yes") or (MsgLowerCase == "facts")):
		RandomFact = SelectRandonFact()
		BotObj.sendMessage(chat_id=ChatID, text=RandomFact)
		return

#Function: select randon facts about PI
#Params: none
#Return: random Pi fact
def SelectRandonFact():
	global PiFactsCollection

	FactsLen = len(PiFactsCollection)
	RandonFact = randint(0,FactsLen - 1)
	return PiFactsCollection[RandonFact]


#Function: Init PI facts collection
#Params: none
#Return: none
def InitFacts():
	global	PiFactsCollection

	#Facts from: https://www.factretriever.com/pi-facts
  #You can put here as many facts you want to! There's almost no limits here.
  #For instance, I've put just three facts.

	PiFactsCollection.append("Pi is the most recognized mathematical constant in the world. Scholars often consider Pi the most important and intriguing number in all of mathematics.")
	PiFactsCollection.append("Scientists in Carl Sagan s novel Contact are able to unravel enough of pi to find hidden messages from the creators of the human race, allowing humans to access deeper levels of universal awareness")
	PiFactsCollection.append("In 1995, Hiroyoki Gotu memorized 42,195 places of pi and is considered the current pi champion. Some scholars speculate that Japanese is better suited than other languages for memorizing sequences of numbers.")


	return

#MAIN PROGRAM
update_id = None
InitFacts()

#Telegram API Token. Get yours with BotFather!
BotToken = '335996914:AAFK-w6w4qD8wTPVdh576hP59WLFiVN0H9M'

bot = telegram.Bot(BotToken)
print 'PI TELEGRAM BOT READY TO GO!'

while True:
        try:
            update_id = PIBot(bot, update_id)
        except telegram.TelegramError as e:
            if e.message in ("Bad Gateway", "Timed out"):
                sleep(1)
            else: 
                raise e
        except URLError as e:
            sleep(1)