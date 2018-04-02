#Base official python images
FROM python:3

#Support guy
MAINTAINER Dante Fana <dfana@dfb.com.do>

ENV PYTHONUNBUFFERED 1

#Update and Install dependecies's binaries of the project
RUN apt-get update

#Create install packages
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
WORKDIR /usr/pbx-dashboard

#Expose ports
EXPOSE 8080

#Command to run app
CMD [ "python", "./run.py" ]
