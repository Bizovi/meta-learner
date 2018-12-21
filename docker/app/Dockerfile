FROM python:3.6.7-stretch

RUN apt update
RUN apt upgrade -y
RUN apt install -y python3-pip
RUN apt install -y python-dev
RUN apt install -y libxml2-dev libxslt-dev
RUN apt install -y libjpeg-dev zlib1g-dev libpng-dev
RUN pip3 install nltk
RUN curl https://raw.githubusercontent.com/codelucas/newspaper/master/download_corpora.py | python3
RUN pip3 install newspaper3k
RUN pip3 install flask
RUN pip3 install ujson

WORKDIR /var/www
ADD ../.. /var/www
CMD python app.py
