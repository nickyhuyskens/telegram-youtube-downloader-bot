# telegram-youtube-downloader-bot
A telegram bot in Docker to download a Youtube url, convert it to mp3 and scp it to another destination

How to use:
Create a bot in telegram and copy the token.

Build the docker container using:
docker build --tag youtube-downloader-bot:1.0.0 .

run the docker container using:
docker run --restart always -d --name youtube-downloader-bot -e SERVER_HOST='ip_from_server' -e SERVER_PORT='scp_port' -e SERVER_USER='username' -e SERVER_PASS='password' -e SERVER_PATH='path_on_server' -e TELEGRAM_BOT_TOKEN='telegram_bot_token' youtube-downloader-bot:1.0.0
