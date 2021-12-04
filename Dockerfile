# Dockerfile

# FROM directive instructing base image to build upon
FROM ubuntu:latest

# COPY startup script into known file location in container
COPY start.sh /usr/local/educative/start.sh

# COPY Django Project folder and requirements.txt into our working directory
COPY educative_django_blog  /usr/local/educative/helloworld
COPY requirements.txt  /usr/local/educative/

# install python 3 and pip
RUN apt-get update && apt-get install python3 -y &&\
    apt -y install curl
RUN apt install python3-pip -y && pip3 install --upgrade pip

# make python 3 default python environment
RUN alias python=python3

# install Django and Gunicorn dependencies from our requirements file
RUN cd /usr/local/educative && pip install -r requirements.txt

# EXPOSE port 8000 to allow communication to/from server
EXPOSE 8000

# CMD specifies the command to execute to start the server running.
CMD ["/start.sh"]
# done! :)

