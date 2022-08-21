FROM ubuntu:20.04

WORKDIR /app
 
RUN apt-get update && apt-get -y upgrade
RUN apt-get -y install software-properties-common
RUN apt-get -y install git python3.8 python3-pip
RUN pip3 install Paver 
RUN pip3 install psycopg2-binary

RUN git clone https://bitbucket.org/genropy/genropy.git
RUN cd genropy/gnrpy && paver develop && python3 initgenropy.py

RUN sed 's/pwd=[^[:space:]]*/pwd="admin" /g' -i /root/.gnr/instanceconfig/default.xml
RUN sed -i '4i <db implementation="postgres" host="postgres" user="postgres" password="postgres" port="5432" />' /root/.gnr/instanceconfig/default.xml

RUN mkdir /app/genropy_projects/Basket 

COPY instances /app/genropy_projects/Basket/instances
COPY packages /app/genropy_projects/Basket/packages

COPY start_genropy.sh /app/start_genropy.sh
RUN chmod +x /app/start_genropy.sh