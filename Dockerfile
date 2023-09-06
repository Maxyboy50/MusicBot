FROM python:3.11

WORKDIR /app_files

COPY requirements.txt /app_files

RUN python3 -m pip install -r /app_files/requirements.txt

COPY bot.py /app_files/

ENV MUSIC_BOT_TOKEN=$MUSIC_BOT_TOKEN

CMD [ "python3", "/app_files/bot.py" ]