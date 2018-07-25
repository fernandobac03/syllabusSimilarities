### FirstWebService with Python



FROM debian:latest
MAINTAINER Fernando Baculima


# Install required packages


RUN echo "deb http://http.debian.net/debian jessie-backports main" > /etc/apt/sources.list.d/jessie-backports.list

RUN apt-get update

RUN apt-get -q -y update && apt-get -q -y upgrade && DEBIAN_FRONTEND=noninteractive apt-get -q -y install \
				libcups2 \
				nano \
				wget \
				python-dev \
                                python-pip \
                                python-virtualenv \
				libpq-dev \
				&& apt-get -q clean

RUN mkdir todo-api
RUN cd todo-api
RUN virtualenv flask
RUN flask/bin/pip install flask

EXPOSE 5000

#COPY app.py /
#RUN chmod a+x app.py
#CMD ["/app.py"]

COPY restserviceapp.py /
RUN chmod a+x restserviceapp.py
CMD ["/restserviceapp.py"]


#RUN (apt-get update && DEBIAN_FRONTEND=noninteractive apt install -y -t jessie-backports  openjdk-8-jre-headless ca-certificates-java)

#RUN (wget -O /tmp/tomcat7.tar.gz http://archive.apache.org/dist/tomcat/tomcat-7/v${TOMCATVER}/bin/apache-tomcat-${TOMCATVER}.tar.gz && \
#  cd /opt && \
#  tar zxf /tmp/tomcat7.tar.gz && \
#  mv /opt/apache-tomcat* /opt/tomcat && \
#  rm /tmp/tomcat7.tar.gz)

### to deploy a specific war to ROOT, uncomment the following 2 lines and specify the appropriate .war
#RUN rm -rf /opt/tomcat/webapps/docs /opt/tomcat/webapps/examples /opt/tomcat/webapps/ROOT
#ADD /target/GA4Clustering.war /opt/tomcat/webapps/

#Changing default tomcat port
#RUN sed 's/8080/8081/g' /opt/tomcat/conf/server.xml > newserver.xml
#RUN mv newserver.xml /opt/tomcat/conf/server.xml


#EXPOSE 8081

#COPY /start_tomcat.sh /
#RUN chmod +x /start_tomcat.sh
#CMD ["/start_tomcat.sh"]

