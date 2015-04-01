FROM        paultag/uwsgi:latest
MAINTAINER  Paul R. Tagliamonte <tag@pault.ag>

RUN apt-get update && apt-get install -y \
    python3.4 python3-pip \
    python3-psycopg2 \
    uwsgi-plugin-python3

RUN mkdir -p /opt/pault.ag/
ADD . /opt/pault.ag/sic/
RUN python3.4 /usr/bin/pip3 install -r /opt/pault.ag/sic/requirements.txt

WORKDIR /opt/pault.ag/sic/
