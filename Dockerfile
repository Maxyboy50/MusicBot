FROM ubuntu:22.04


USER root
RUN apt update && apt install -y python3.10 && apt install -y python3-pip && apt install -y ffmpeg

ADD requirements.txt /app_files/

RUN python3 -m pip install -r /app_files/requirements.txt

ADD bot.py /app_files/

ENV MUSIC_BOT_TOKEN=$MUSIC_BOT_TOKEN


CMD [ "python3", "/app_files/bot.py" ]
