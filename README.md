Docker/Flask sample application
following
https://docs.docker.com/language/python/build-images/
https://docs.docker.com/language/python/run-containers/
https://docs.docker.com/language/python/develop/
https://docs.docker.com/language/python/configure-ci-cd/



Recommend using WSL to kick off docker cmds...

----------------
TO AVOID BLUE-ON-BLUE OUTPUT FROM docker build...
IF RUNNING WSL:
  export BUILDKIT_PROGRESS='plain'
  (put in ~/.bashrc)
OR if running POWERSHELL...
  $env:BUILDKIT_PROGRESS='plain'
  and put this into your windows powershell profile by...
  notepad $profile  which is in C:\Users\chris\Documents\WindowsPowerShell
------------------

NOW... back to building a Docker Flask...
   8 mkdir code_docker
   9 cd code_docker
  13 python -m venv .venv
  16 source .venv/bin/activate
  17 python -m pip install Flask
  18 python -m pip freeze > requirements.txt

Above created a simmple Flask website and exported the requirments.txt (venv).
We now want to create a Docker image with those same parts/pieces.

So  - create a Dockerfile. The Dockerfile will build an image using:
start with standard python3 docker image
add python libraries from requirements.txt above
do all the building in the /app sub-folder

# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]


BUILD the docker image...
docker build --tag my_docker_flask_app .

VIEW images...
docker images

RUN exposing port 8000, and detach, and name it
docker run --detach --publish 8000:5000 --name docker_flask_123 my_docker_flask_app

START, STOP, RESTART
docker ps
docker ps -a
docker stop 33333333333
docker restart 33333333333
docker rm 33333333333

FOR MYSQL - CREATE VOLUMES, NETWORK
docker volume create mysql
docker volume create mysql_config
docker network create mysqlnet

RUN MYSQL container
docker run --rm -d -v mysql:/var/lib/mysql \
  -v mysql_config:/etc/mysql -p 3306:3306 \
  --network mysqlnet \
  --name mysqldb \
  -e MYSQL_ROOT_PASSWORD=p@ssw0rd1 \
  mysql

Connect to MySQL
docker exec -ti mysqldb mysql -u root -p

UPDATE app.py to include flask routes "/" /widgets and /initdb
REBUILD:
docker build --tag flask_mysql_app .

RUN:
$ docker run   --rm -d   --network mysqlnet   --name rest-server   -p 8000:5000   flask_mysql_app

 curl http://localhost:8000/
 curl http://localhost:8000/initdb
 curl http://localhost:8000/widgets

CREATE a docker-compose.dev.yml 

version: '3.8'

services:
 web:
  build:
   context: .
  ports:
  - 8000:5000
  volumes:
  - ./:/app

 mysqldb:
  image: mysql
  ports:
  - 3306:3306
  environment:
  - MYSQL_ROOT_PASSWORD=p@ssw0rd1
  volumes:
  - mysql:/var/lib/mysql
  - mysql_config:/etc/mysql

volumes:
  mysql:
  mysql_config:

------------------
$ docker compose -f docker-compose.dev.yml up --build

CONFIGURE CI/CD using github...


