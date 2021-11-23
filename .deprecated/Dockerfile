FROM python

# RUN adduser todoserver

WORKDIR /home/todoserver

COPY ../requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

COPY ../server server
COPY ../app.py .env ./

# RUN chown -R todoserver:todoserver ./
# USER todoserver

EXPOSE 5000
ENTRYPOINT ["flask run"]
