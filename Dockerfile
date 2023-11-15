FROM ubuntu:22.04

RUN apt update && apt install python3-pip -y

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

RUN apt-get install -y locales
RUN locale-gen zh_CN.GB18030

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install tzdata
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN dpkg-reconfigure --frontend noninteractive tzdata
ENV DEBIAN_FRONTEND noninteractive

RUN pip install fastavro requests confluent-kafka numpy openctp-ctp

COPY  . /workspace
WORKDIR /workspace


CMD [ "python3", "mdapi.py" ]