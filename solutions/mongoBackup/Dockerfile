FROM python:3

WORKDIR /usr/src/mongobackup

COPY requirements.txt ./
COPY mongoRepsetBackup.py ./

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./mongoRepsetBackup.py", "'mongodb://admin:admin@mongo1:27017,mongo1:27018,mongo1:27019/?authSource=test&replicaSet=dbrs'" ]
