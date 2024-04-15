# -*- coding: utf-8 -*-
import requests
import time
import hashlib
import base64
import json
import cv2


class General:
    def __init__(self, APPID, API_KEY, path):
        """

        :param path: 图片路径
        """
        self.APPID = APPID  # 应用ID
        self.API_KEY = API_KEY  # 接口密钥
        self.url = 'http://webapi.xfyun.cn/v1/service/v1/ocr/general'  # url
        self.language = 'cn|en'  # 语种设置
        self.location = "false"  # 是否返回文本位置信息
        self.path = path  # 图片路径

    def __get_header(self):

        curTime = str(int(time.time()))
        param = "{\"language\":\"" + self.language + "\",\"location\":\"" + self.location + "\"}"
        paramBase64 = base64.b64encode(param.encode('utf-8'))

        m2 = hashlib.md5()
        str1 = self.API_KEY + curTime + str(paramBase64, 'utf-8')
        m2.update(str1.encode('utf-8'))
        checkSum = m2.hexdigest()
        # 组装http请求头
        header = {
            'X-CurTime': curTime,
            'X-Param': paramBase64,
            'X-Appid': self.APPID,
            'X-CheckSum': checkSum,
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        }
        return header

    def __get_body(self):
        """
        图片二进制数据
        :return:
        """
        with open(self.path, 'rb') as f:
            imgfile = f.read()
        data = {'image': str(base64.b64encode(imgfile), 'utf-8')}
        return data

    def __response_url(self, data, headers):
        """
        1.请求url
        2.获取响应的label数据
        :param data:
        :param headers:
        :return:
        """
        result = requests.post(self.url, data=data, headers=headers)
        result = json.loads(result.content)
        # result = str(req.content, 'utf-8')
        return result

    def get_data(self):
        """
        :return: 响应数据
        """
        # 调用__get_body方法完成图片二进制的读取
        data = self.__get_body()
        # 调用__get_header方法完成图的头域的设置
        headers = self.__get_header()
        # 调用__response_url从服务器获取数据
        result = self.__response_url(data, headers)
        return result

    def process_data(self, data):
        """
         解析请求数据，获取印刷文字识别结果
         :param data: 原始数据
         :return:
         """
        print(data)
        print('-------')
        # 分析code
        code = data['code']
        process_result = []
        if code == '0':
            # 分析data中的数据
            result = data['data']['block']
            for item in result:
                if item['type'] == 'text':
                    line = item['line']
                    for words in line:
                        msg = ''
                        word = words['word']
                        for content in word:
                            msg += content['content'] + ' '
                        process_result.append(msg)
        return process_result

    def general_analysis(self):
        """
        本地图像：印刷文字识别
        :return:
        """
        # 调用get_data方法获取从服务器请求的数据
        request_data = self.get_data()
        # 调用process_data方法将数据进行解析
        process_data = self.process_data(request_data)
        return process_data


if __name__ == '__main__':
    APPID = '5b14d46d'  # 应用ID
    API_KEY = 'c4118058b9769001261349c4efea13d6'  # 接口密钥
    res = General(APPID, API_KEY, r'..//..//static//images//upload//ocr1.jpg').general_analysis()
    print(res)
