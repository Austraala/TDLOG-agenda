FROM python:3.8.5

WORKDIR /usr/src
COPY . /back
WORKDIR /back
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT [ "python" ]
RUN python src/init_db.py
CMD [ "src/main.py" ]
