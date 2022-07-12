FROM python:3.8-slim 

ARG DB_
ARG HOST_
ARG PORT_
ARG USER_
ARG PASSWORD_

ENV DB=$DB_
ENV HOST=$HOST_
ENV PORT=$PORT_
ENV USER=$USER_
ENV PASSWORD=$PASSWORD_

WORKDIR /usr/src/app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /usr/src/app/services
ENTRYPOINT [ "python", "engine.py" ]
