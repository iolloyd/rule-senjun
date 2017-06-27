FROM ubuntu 
MAINTAINER Lloyd Moore <lloyd@codegood.co>

RUN apt-get update
RUN apt-get -y install python-software-properties git build-essential

ADD package.json /tmp/package.json
RUN cd /tmp && yarn start
RUN mkdir -p /opt/app && cp -a /tmp/node_modules /opt/app

WORKDIR /opt/app
ADD . /opt/app

EXPOSE 3300

CMD ["python3", "lib/cli_outfit.py", "28292"]
