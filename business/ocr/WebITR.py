#!/usr/bin/env python 
# -*- coding:utf-8 -*-

#
# 拍照速算识别 WebAPI 接口调用示例
# 运行前：请先填写Appid、APIKey、APISecret
# 运行方法：直接运行 main 即可 
# 结果： 控制台输出结果信息
# 
# 1.接口文档（必看）：https://www.xfyun.cn/doc/words/photo-calculate-recg/API.html
# 2.错误码链接：https://www.xfyun.cn/document/error-code （错误码code为5位数字）
#

import requests
import datetime
import hashlib
import base64
import hmac
import json
import cv2


class WEBITR(object):
    def __init__(self, APPID, APIKey, Secret, host, in_path, out_path):
        # 应用ID（到控制台获取）
        self.APPID = APPID
        # 接口APIKey（到控制台拍照速算服务页面获取）
        self.APIKey = APIKey
        # 接口APISercet（到控制台拍照速算服务页面获取）
        self.Secret = Secret

        # 以下为POST请求
        self.Host = host
        self.RequestUri = "/v2/itr"
        # 设置url
        # print(host)
        self.url = "https://" + host + self.RequestUri
        self.HttpMethod = "POST"
        self.Algorithm = "hmac-sha256"
        self.HttpProto = "HTTP/1.1"

        # 设置当前时间
        curTime_utc = datetime.datetime.utcnow()
        self.Date = self.httpdate(curTime_utc)
        # 设置测试图片文件
        self.AudioPath = in_path
        self.outPath = out_path
        self.BusinessArgs = {"ent": "math-arith", "aue": "raw", }

    def imgRead(self, path):
        with open(path, 'rb') as fo:
            return fo.read()

    def hashlib_256(self, res):
        m = hashlib.sha256(bytes(res.encode(encoding='utf-8'))).digest()
        result = "SHA-256=" + base64.b64encode(m).decode(encoding='utf-8')
        return result

    def httpdate(self, dt):
        """
        Return a string representation of a date according to RFC 1123
        (HTTP/1.1).

        The supplied date must be in UTC.

        """
        weekday = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][dt.weekday()]
        month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][dt.month - 1]
        return "%s, %02d %s %04d %02d:%02d:%02d GMT" % (weekday, dt.day, month, dt.year, dt.hour, dt.minute, dt.second)

    def generateSignature(self, digest):
        signatureStr = "host: " + self.Host + "\n"
        signatureStr += "date: " + self.Date + "\n"
        signatureStr += self.HttpMethod + " " + self.RequestUri + " " + self.HttpProto + "\n"
        signatureStr += "digest: " + digest
        signature = hmac.new(bytes(self.Secret.encode(encoding='utf-8')), bytes(signatureStr.encode(encoding='utf-8')),
                             digestmod=hashlib.sha256).digest()
        result = base64.b64encode(signature)
        return result.decode(encoding='utf-8')

    def init_header(self, data):
        digest = self.hashlib_256(data)
        # print(digest)
        sign = self.generateSignature(digest)
        authHeader = 'api_key="%s", algorithm="%s", ' \
                     'headers="host date request-line digest", ' \
                     'signature="%s"' % (self.APIKey, self.Algorithm, sign)
        # print(authHeader)
        headers = {"Content-Type": "application/json", "Accept": "application/json", "Method": "POST",
                   "Host": self.Host, "Date": self.Date, "Digest": digest, "Authorization": authHeader}
        return headers

    def get_body(self):
        audioData = self.imgRead((self.AudioPath))
        content = base64.b64encode(audioData).decode(encoding='utf-8')
        postdata = {"common": {"app_id": self.APPID}, "business": self.BusinessArgs, "data": {"image": content, }}
        body = json.dumps(postdata)
        # print(body)
        return body

    def __response_url(self, data, headers):
        """
        1.请求url
        2.获取响应的label数据
        :param type:
        :param data:
        :param headers:
        :return:
        """
        result = requests.post(self.url, data=data, headers=headers,timeout=8)
        result = json.loads(result.content)
        # result = str(req.content, 'utf-8')
        return result

    def get_data(self):
        if self.APPID == '' or self.APIKey == '' or self.Secret == '':
            return ''
        else:
            # 调用__get_body方法完成图片二进制的读取
            data = self.get_body()
            # 调用__get_header方法完成图的头域的设置
            headers = self.init_header(data)
            # 调用__response_url从服务器获取数据
            result = self.__response_url(data, headers)
            return result

    def process_result(self, respData):
        print(respData)
        print('-------')
        itr_Result = {'right': 0, 'wrong': 0, 'flag': 'true'}
        points = []
        # 以下仅用于调试
        code = str(respData["code"])
        if code == '0':
            data = respData["data"]
            for line_info in data['ITRResult']['multi_line_info']['imp_line_info']:
                if line_info['total_score'] == 0:

                    imp_line_rect = line_info['imp_line_rect']
                    points.append({'x1': imp_line_rect['left_up_point_x'], 'y1': imp_line_rect['left_up_point_y'],
                                   'x2': imp_line_rect['right_down_point_x'],
                                   'y2': imp_line_rect['right_down_point_y'], })
                    itr_Result['wrong'] = itr_Result['wrong'] + 1
                else:
                    itr_Result['right'] = itr_Result['right'] + 1
        else:
            itr_Result['flag'] = 'false'
            itr_Result['msg'] = "请前往https://www.xfyun.cn/document/error-code?code=" + code;
        return points, itr_Result

    def draw(self, points):
        image = cv2.imread(self.AudioPath)
        for point in points:
            first_point = (point['x1'], point['y1'])
            last_point = (point['x2'], point['y2'])
            cv2.rectangle(image, first_point, last_point, (0, 0, 255), 2)
        cv2.imwrite(self.outPath, image)

    def itr_analysis(self):
        """
        拍照速算识别
        :return:
        """
        # 调用get_data方法获取从服务器请求的数据
        request_data = self.get_data()
        if request_data != '':
            # 调用process_data方法将数据进行解析,获取坐标和结果
            points, process_data = self.process_result(request_data)
            # 调用draw方法根据坐标绘制错误区域
            self.draw(points)
        else:
            process_data = {'flag': 'false', 'msg': 'Appid 或APIKey 或APISecret 为空！请打开demo代码，填写相关信息。'}

        return process_data


if __name__ == '__main__':
    APPID = "5ff6cfc7"  # 应用ID（到控制台获取）
    APIKey = "c06ba7f73f267583e0f2fbc4c39d7a1c"  # 接口APIKey（到控制台拍照速算服务页面获取）
    Secret = "00552b54926214015411d9d9c1aad5b0"  # 接口APISercet（到控制台拍照速算服务页面获取）
    host = "rest-api.xfyun.cn"  ##示例:  host="rest-api.xfyun.cn"域名形式
    # 初始化类
    res = WEBITR(APPID, APIKey, Secret, host, r'..//..//static//images//upload//itr.jpg',
                 r'..//..//static//images//upload//itr_result.jpg').itr_analysis()
    print(res)
