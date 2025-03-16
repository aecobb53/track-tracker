FROM python

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY track_tracker track_tracker
COPY entrypoint.sh .
COPY info.json .

RUN mkdir /db
COPY etc/testing_db /db

# COPY . .

ENTRYPOINT [ "bash", "entrypoint.sh" ]
