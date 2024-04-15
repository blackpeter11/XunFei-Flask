# -*- coding: utf-8 -*-
import requests
import time
import hashlib
import base64
import json


class ScenesDesc:
    def __init__(self, label):
        self.label = label

    def convert_scene(self):
        code = int(self.label)
        if code == 1:
            result = '教室'
        elif code == 2:
            result = '餐厅(公共)'
        elif code == 3:
            result = '草地 田地 花园'
        elif code == 4:
            result = '沙漠'
        elif code == 5:
            result = '办公室 会议室'
        elif code == 6:
            result = '酒吧 KTV 舞厅'
        elif code == 7:
            result = '室内运动场'
        elif code == 8:
            result = '商场'
        elif code == 9:
            result = '山峰'
        elif code == 10:
            result = '湖 池塘 海洋'
        elif code == 11:
            result = '森林'
        elif code == 12:
            result = '街道'
        elif code == 13:
            result = '室外运动场'
        elif code == 14:
            result = '海滩 沙滩'
        elif code == 15:
            result = '泳池'
        elif code == 16:
            result = '游乐场'
        elif code == 17:
            result = '没有场景'
        elif code == 18:
            result = '其他场景'
        elif code == 19:
            result = '车内 船上 飞机上'
        elif code == 20:
            result = '礼堂 演出厅'
        elif code == 21:
            result = '广场 空地'
        elif code == 22:
            result = '纯人物图'
        elif code == 23:
            result = '播音室'
        elif code == 24:
            result = '房屋 建筑'
        elif code == 25:
            result = '医院'
        elif code == 26:
            result = '网吧 游戏厅 棋牌室'
        elif code == 27:
            result = '雕塑 石碑 牌坊'
        elif code == 28:
            result = '宿舍'
        elif code == 29:
            result = '化妆室 理发店'
        elif code == 30:
            result = '健身房'
        elif code == 31:
            result = '机场'
        elif code == 32:
            result = '火车站'
        elif code == 33:
            result = '汽车站'
        elif code == 34:
            result = '市场 集市'
        elif code == 35:
            result = '图书馆 书店'
        elif code == 36:
            result = '公路'
        elif code == 37:
            result = '古建筑'
        elif code == 38:
            result = '厨房'
        elif code == 39:
            result = '餐厅(家里)'
        elif code == 40:
            result = '洗手间'
        elif code == 41:
            result = '浴室 洗澡间'
        elif code == 42:
            result = '停车场'
        else:
            result = '图片文件有错误，或者格式不支持（gif图不支持）'
        return result


class OcrScene:
    def __init__(self, app_id, api_key, path):
        """

        :param app_id: 应用ID
        :param api_key: 接口密钥
        :param path:  图片路径
        """
        self.APPID = app_id  # 应用ID
        self.API_KEY = api_key  # 接口密钥
        self.base_url = "http://tupapi.xfyun.cn/v1/"  # 基础url
        self.image_path = path  # 图片路径
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
        :param headers: 头域
        :param data: 数据
        :return:
        """

        result = requests.post(self.base_url + type, data=data, headers=headers)
        # print(self.base_url + type)
        result = json.loads(result.content)
        return result

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
        result = self.__response_url('scene', headers, data)
        return result

    def process_data(self, data):
        """
        解析请求数据，将数字标签值转化为对应的中文
        如 1表示‘教室’
        :param data: 原始数据
        :return:
        """
        print(data)
        code = data['code']
        if code == 0:
            scene = data['data']['fileList'][0]['label']
            scene = ScenesDesc(scene).convert_scene()
        else:
            scene = data['desc']
        result = {'desc': scene}
        return result

    def scene_local_analysis(self):
        """
        本地图像：场景识别
        :return: 分析结果
        """
        self.mode = 0  # 设置本地图像类型
        # 调用get_data方法获取从服务器请求的数据
        request_data= self.get_data()
        # 调用process_data方法将数据进行解析
        process_data = self.process_data(request_data)
        return process_data


if __name__ == '__main__':
    APPID = "5ff6cfc7"  # 应用ID
    API_KEY = "199cb73af0eb25f95039de10cc1cf704"  # 接口密钥
    res = OcrScene(APPID, API_KEY, r'..//..//static//images//upload//scene.jpg').scene_local_analysis()
    print(res)

