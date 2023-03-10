# base image  
FROM python:3.8   
# setup environment variable  
ENV DockerHOME=/home/app/webapp  

# set work directory  
RUN mkdir -p $DockerHOME  

# where your code lives  
WORKDIR $DockerHOME  

# set environment variables  
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

# install dependencies  
RUN pip install --upgrade pip 
COPY ./requirements.txt $DockerHOME  
RUN pip install -r requirements.txt

# copy project
COPY . $DockerHOME

EXPOSE 8000

CMD ["gunicorn", "--workers=4", "yoc_certificates_backend.wsgi:application", "--bind", "0.0.0.0:8000"]