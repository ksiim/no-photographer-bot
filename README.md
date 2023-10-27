# aiogram3.x-bot-template
template for aiogram3.x bots
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
command to generate requirements.txt from poetry:
poetry export --without-hashes --without-urls | awk '{ print $1 }' FS=';' > requirements.txt
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
