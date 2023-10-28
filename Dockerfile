FROM python:3.10-bullseye


USER root
RUN apt update && apt install -y ffmpeg

ADD /src/requirements.txt /app_files/

RUN python3 -m pip install -r /app_files/requirements.txt

ADD /src/bot.py /app_files/

ENV MUSIC_BOT_TOKEN=$MUSIC_BOT_TOKEN


CMD [ "python3", "/app_files/bot.py" ]
