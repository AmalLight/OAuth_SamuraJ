FROM debian

RUN mkdir /frontend_files/
WORKDIR /frontend_files/

EXPOSE 80

RUN apt update
RUN apt install -y python3 python3-dev python3-pip
RUN pip3 install --upgrade pip

RUN apt install -y build-essential libssl-dev libffi-dev cargo wget curl nmap rustc

# curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

RUN pip3 install Flask flask-json PyJWT flask-cors pybase64 requests cryptography
RUN pip3 install --upgrade requests

RUN export FLASK_APP=/backend_files/app.py
RUN export FLASK_ENV=development

CMD [ "/bin/bash" , "run.sh" ]
