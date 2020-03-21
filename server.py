import os
import subprocess
import paramiko
from scp import SCPClient
from telegram.ext import Updater, MessageHandler, Filters

server = os.environ['SERVER_HOST']
port = os.environ['SERVER_PORT']
user = os.environ['SERVER_USER']
password = os.environ['SERVER_PASS']
path = os.environ['SERVER_PATH']
telegram_bot_token = os.environ['TELEGRAM_BOT_TOKEN']
fileName = ""

updater = Updater(token=telegram_bot_token, use_context=True)
dispatcher = updater.dispatcher

def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client

ssh = createSSHClient(server, port, user, password)
scp = SCPClient(ssh.get_transport())

def transferYoutubeVideoToServer(fileName):
    print("starting scp")
    scp.put(fileName, remote_path=path + fileName)
    print(fileName + " transferred to " + path + " on remote host")
    os.remove(fileName)

def downloadYoutubeVideo(url):
    global fileName
    result = subprocess.run(["youtube-dl", url, "-x", "--no-check-certificate", "--embed-thumbnail", "--audio-format=mp3", "-o", "./%(title)s.%(ext)s"], capture_output=True)
    print(result.stdout)
    print(result.stderr)
    splittedResults = result.stdout.decode("utf-8").split('\n')
    for split in splittedResults:
        if "Destination" in split and "mp3" in split:
            fileName = split[22:]
            print("Downloaded " + fileName + ", sending to server over scp")
    print("sending download to server...")

def handleMessage(update, context):
    print(update.message.text)
    if "youtube" in update.message.text:
        context.bot.send_message(chat_id=update.effective_chat.id, text="started downloading...")
        downloadYoutubeVideo(update.message.text)
        context.bot.send_message(chat_id=update.effective_chat.id, text="downloading of "+ fileName +" finished, transferring to server.")
        transferYoutubeVideoToServer(fileName)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Song transferred to server.")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Not a valid youtube URL.")

message_handler = MessageHandler(Filters.text, handleMessage)
dispatcher.add_handler(message_handler)

updater.start_polling()
