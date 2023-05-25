# Basic flask container

FROM fanoftal2/flask-crud-base:1

# # ADD . /home/app/
# WORKDIR /home/app/

# COPY ./app/requirements.txt ./
# RUN pip3 install -r requirements.txt
# COPY . ./

COPY . /home/app/
WORKDIR /home/app/
RUN pip3 install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python3", "app.py"]
