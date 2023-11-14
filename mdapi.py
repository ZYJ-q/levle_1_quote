import inspect

from openctp_ctp import mdapi

import config
import json

from kafka import KafkaProducer
from kafka.errors import KafkaError

KAFKA_TOPIC = "market-data"


class CMdSpiImpl(mdapi.CThostFtdcMdSpi):
    def __init__(self, front:str):
        print("-------------------------------- 启动 mduser api demo ")
        super().__init__()
        self._front = front
        self.producer = KafkaProducer(bootstrap_servers="119.45.139.76:19092")

        self._api = mdapi.CThostFtdcMdApi.CreateFtdcMdApi(
            "market"
        )  # type: mdapi.CThostFtdcMdApi

        print("CTP行情API版本号:", self._api.GetApiVersion())
        print("行情前置:" + self._front)

        # 注册行情前置
        self._api.RegisterFront(self._front)
        # 注册行情回调实例
        self._api.RegisterSpi(self)
        # 初始化行情实例
        self._api.Init()
        print("初始化成功")
    
    def sendjsondata(self, params):
        try:
            params_message = params
            producer = self.producer
            v = producer.send(topic="level_1_quotes", key=None,  value=params_message.encode('utf-8'))
            # _ = v.get(timeout=10)
            print(f"Successfully produced message to topic: market-data, {v}")
            producer.flush()
            # producer.close()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
        except KafkaError as e:
            print(e)

    def OnFrontConnected(self):
        """行情前置连接成功"""
        print("行情前置连接成功")

        # 登录请求, 行情登录不进行信息校验
        print("登录请求")
        req = mdapi.CThostFtdcReqUserLoginField()
        self._api.ReqUserLogin(req, 0)

    def OnRspUserLogin(
        self,
        pRspUserLogin: mdapi.CThostFtdcRspUserLoginField,
        pRspInfo: mdapi.CThostFtdcRspInfoField,
        nRequestID: int,
        bIsLast: bool,
    ):
        """登录响应"""
        if pRspInfo and pRspInfo.ErrorID != 0:
            print(f"登录失败: ErrorID={pRspInfo.ErrorID}, ErrorMsg={pRspInfo.ErrorMsg}")
            return

        print("登录成功")

        if len(instruments) == 0:
            return

        # 订阅行情
        print("订阅行情请求：", instruments)
        self._api.SubscribeMarketData(
            [i.encode("utf-8") for i in instruments], len(instruments)
        )

    def OnRtnDepthMarketData(
        self, pDepthMarketData: mdapi.CThostFtdcDepthMarketDataField
    ):
        """深度行情通知"""
        params = []
        data = {}
        
        for name, value in inspect.getmembers(pDepthMarketData):
            
            if name[0].isupper():
                params.append(f"{name}={value}")
                data.update({f"{name}":f"{value}"})
                
                
        # params.append(data)
        del data["ExchangeID"]
        del data["ExchangeInstID"]
        v_value = json.dumps(data)
        print("深度行情:", v_value)
        producer = self.producer
        print("producer---------", producer)
        self.sendjsondata(v_value)
        
        
        
        



    def OnRspSubMarketData(
        self,
        pSpecificInstrument: mdapi.CThostFtdcSpecificInstrumentField,
        pRspInfo: mdapi.CThostFtdcRspInfoField,
        nRequestID: int,
        bIsLast: bool,
    ):
        """订阅行情响应"""
        if pRspInfo and pRspInfo.ErrorID != 0:
            print(
                f"订阅行情失败:ErrorID={pRspInfo.ErrorID}, ErrorMsg={pRspInfo.ErrorMsg}",
            )
            return

        print("订阅行情成功:", pSpecificInstrument.InstrumentID)

    def wait(self):
        # 阻塞 等待
        input("-------------------------------- 按任意键退出 mduser api demo ")

        self._api.Release()


if __name__ == "__main__":
    # print("11111111111111")
    spi = CMdSpiImpl(config.fronts["电信2"]["md"])

    # 注意选择有效合约, 没有行情可能是过期合约或者不再交易时间内导致
    instruments = ("zn2401", "fu2401", "sn2401", "MA2401")

    spi.wait()

