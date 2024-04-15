# -*- coding: utf-8 -*-
import requests
import time
import hashlib
import base64
import json
import pandas as pd


class OcrObject:
    def __init__(self, APPID, API_KEY, path, file_path):
        """

        :param APPID: APPID
        :param API_KEY: API_KEY
        :param path: 图片路径
        :param file_path: label文件路径
        """
        self.APPID = APPID  # 应用ID
        self.API_KEY = API_KEY  # 接口密钥
        self.base_url = "http://tupapi.xfyun.cn/v1/"  # 基础url
        self.image_path = path  # 图片路径
        self.file_path = file_path  # label路径
        self.excel_data = self.read_excel()
        self.mode = 0  # 图片路径模式：0- 本地图片；1-网络图片

    def __get_header(self):

        # 根据图片路径模式，构建param
        if self.mode == 0:  # 本地
            param = "{\"image_name\":\"" + self.image_path + "\"}"
        else:  # url
            image_name = 'img.jpg'
            param = "{\"image_name\":\"" + image_name + "\",\"image_url\":\"" + self.image_path + "\"}"
        # 构建头域中的X-Param
        curTime = str(int(time.time()))
        # 构建头域中的X-CheckSum
        paramBase64 = base64.b64encode(param.encode('utf-8'))
        # 构建头域中的X-CheckSum
        tmp = str(paramBase64, 'utf-8')
        m2 = hashlib.md5()
        m2.update((self.API_KEY + curTime + tmp).encode('utf-8'))
        checkSum = m2.hexdigest()
        # 头域
        header = {
            'X-CurTime': curTime,
            'X-Param': paramBase64,
            'X-Appid': self.APPID,
            'X-CheckSum': checkSum,
        }
        return header

    def __get_body(self):
        """
        图片二进制数据
        :return:
        """
        binfile = open(self.image_path, 'rb')
        data = binfile.read()
        return data

    def __response_url(self, type, headers, data=None):
        """
        1.请求url
        2.获取响应的label数据
        :param type:
        :param data:
        :param headers:
        :return:
        """
        result = requests.post(self.base_url + type, data=data, headers=headers)
        result = json.loads(result.content)

        return result

    def read_excel(self):
        df = pd.read_excel(self.file_path)
        return df

    def read_excel_by_label(self, label):
        df = self.excel_data
        df_res = df[(df.label == label)]
        return df_res

    def get_data(self):
        """
        1.图片二进制的读取
        2.请求头的设置
        3.从服务器获取数据
        :return: 响应数据
        """
        # 调用__get_body方法完成图片二进制的读取
        data = self.__get_body()
        # 调用__get_header方法完成图的头域的设置
        headers = self.__get_header()
        # 调用__response_url从服务器获取数据
        result = self.__response_url('currency', headers, data)
        return result

    def process_data(self, data):
        """
        解析请求数据，获取物品识别结果
        如  标签  英文         中文              分类
            0    zabaglione	 意大利甜点，蛋奶冻	  食品
        :param data: 原始数据
        :return:
        """
        print(data)
        print('-------')
        code = data['code']
        res = []
        if code == 0:  # 获取百分比前5的数据
            labels = data['data']['fileList'][0]['labels']
            rates = data['data']['fileList'][0]['rates']
            for i in range(5):
                label = labels[i]  # 识别种类
                rate = rates[i]  # 识别概率
                df_res = self.read_excel_by_label(label)
                if df_res.shape[0] == 1:
                    res.append({'desc': df_res['中文'].values[0], 'rate': "%.2f%%" % (rate * 100)})
                else:
                    res.append({'desc': '未找到此物品', 'rate': '未找到此物品'})
        else:
            res.append({'desc': data['desc'], 'rate': data['desc']})
        return res

    def object_local_analysis(self):
        """
        本地图像：物体识别
        :return:
        """
        self.mode = 0  # 设置本地图像类型
        # 调用get_data方法获取从服务器请求的数据
        request_data = self.get_data()
        # 调用process_data方法将数据进行解析
        process_data = self.process_data(request_data)
        return process_data


if __name__ == '__main__':
    APPID = "5ff6cfc7"  # 应用ID
    API_KEY = "199cb73af0eb25f95039de10cc1cf704"  # 接口密钥
    res = OcrObject(APPID, API_KEY, r'..//..//static//images//upload//object.jpg',
                    r'..//..//static//files//label.xlsx').object_local_analysis()
    print(res)

    # url = "http://hbimg.b0.upaiyun.com/a09289289df694cd6157f997ffa017cc44d4ca9e288fb-OehMYA_fw658"
    # OcrObject(url).object_web_analysis()
