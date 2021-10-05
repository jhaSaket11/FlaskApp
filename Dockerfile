FROM python:3.7

# set the working directory in the container
WORKDIR /app

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local  script file the working directory
COPY src/ .

# expose port
EXPOSE 8001

# command to run on container start
CMD [ "python", "./api.py" ]