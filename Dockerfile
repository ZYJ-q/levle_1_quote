FROM ubuntu:22.04

RUN apt update && apt install python3-pip -y

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

RUN apt-get install -y locales
RUN locale-gen zh_CN.GB18030

RUN pip install fastavro requests confluent-kafka numpy openctp-ctp

COPY  . /workspace
WORKDIR /workspace


CMD [ "python3", "mdapi.py" ]