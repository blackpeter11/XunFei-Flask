#!/usr/bin/env python 
# -*- coding:utf-8 -*-

#
# 公式识别 WebAPI 接口调用示例
# 运行前：请先填写Appid、APIKey、APISecret
# 运行方法：直接运行 main 即可 
# 结果： 控制台输出结果信息
# 
# 1.接口文档（必看）：https://www.xfyun.cn/doc/words/formula-discern/API.html
# 2.错误码链接：https://www.xfyun.cn/document/error-code （错误码code为5位数字）
#

import requests
import datetime
import hashlib
import base64
import hmac
import json

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


class WEBITRTEACH(object):
    def __init__(self, APPID, APIKey, Secret, host, in_path, out_path):

        self.APPID = APPID  # 应用ID（到控制台获取）
        self.APIKey = APIKey  # 接口APIKey（到控制台公式识别服务页面获取）
        self.Secret = Secret  # 接口APISercet（到控制台公式识别服务页面获取）

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
        self.BusinessArgs = {
            "ent": "teach-photo-print",
            "aue": "raw",
        }
        # 设置图片输出路径
        self.out_path = out_path

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
        month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
                 "Oct", "Nov", "Dec"][dt.month - 1]
        return "%s, %02d %s %04d %02d:%02d:%02d GMT" % (weekday, dt.day, month,
                                                        dt.year, dt.hour, dt.minute, dt.second)

    def generateSignature(self, digest):
        signatureStr = "host: " + self.Host + "\n"
        signatureStr += "date: " + self.Date + "\n"
        signatureStr += self.HttpMethod + " " + self.RequestUri \
                        + " " + self.HttpProto + "\n"
        signatureStr += "digest: " + digest
        signature = hmac.new(bytes(self.Secret.encode(encoding='utf-8')),
                             bytes(signatureStr.encode(encoding='utf-8')),
                             digestmod=hashlib.sha256).digest()
        result = base64.b64encode(signature)
        return result.decode(encoding='utf-8')

    def init_header(self, data):
        digest = self.hashlib_256(data)
        # print(digest)
        sign = self.generateSignature(digest)
        authHeader = 'api_key="%s", algorithm="%s", ' \
                     'headers="host date request-line digest", ' \
                     'signature="%s"' \
                     % (self.APIKey, self.Algorithm, sign)
        # print(authHeader)
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Method": "POST",
            "Host": self.Host,
            "Date": self.Date,
            "Digest": digest,
            "Authorization": authHeader
        }
        return headers

    def get_body(self):
        audioData = self.imgRead((self.AudioPath))
        content = base64.b64encode(audioData).decode(encoding='utf-8')
        postdata = {
            "common": {"app_id": self.APPID},
            "business": self.BusinessArgs,
            "data": {
                "image": content,
            }
        }
        body = json.dumps(postdata)
        # print(body)
        return body

    def get_data(self):
        if self.APPID == '' or self.APIKey == '' or self.Secret == '':
            return ''
        else:
            code = 0
            body = self.get_body()
            headers = self.init_header(body)
            # print(self.url)
            response = requests.post(self.url, data=body, headers=headers, timeout=8)
            return json.loads(response.text)

    def process_result(self, respData):
        """
        解析数据，获取公式
        :param respData:
        :return:
        """
        print(respData)
        print('-----')
        code = str(respData["code"])
        if code == '0':
            data = respData['data']['region'][0]['recog']['content']
            result = {'flag': 'true', 'msg': data}
        else:
            result = {'flag': 'false', 'msg': "请前往https://www.xfyun.cn/document/error-code?code=" + code}
        return result

    def process_latex(self, raw):
        raw = raw.replace(' ifly-latex-begin ', '$')
        raw = raw.replace(' ifly-latex-end ', '$')
        result = ''
        flag = True
        while flag:
            index = 0
            while index < 80:
                index = raw.find('$\\', index + 1)
                if index == -1:
                    index = len(raw) + 1
                    flag = False
                    break
            result = result + raw[:index] + '\n'
            raw = raw[index:]
        plt.xticks([])  # 去掉x轴
        plt.yticks([])  # 去掉y轴
        plt.axis('off')  # 去掉坐标轴
        plt.text(-0.1, 0.8, result, fontsize=18, style='oblique', color="black")
        plt.savefig(self.out_path)
        plt.clf()

    def itrteach_analysis(self):
        """
        公式识别
        :return:
        """
        # 调用get_data方法获取从服务器请求的数据
        request_data = self.get_data()
        if request_data != '':
            # 调用process_data方法将数据进行解析,获取解析结果
            process_data = self.process_result(request_data)
            # 调用process_latex方法处理latex公式
            self.process_latex(process_data['msg'])  #
        else:
            process_data = {'flag': 'false', 'msg': 'Appid 或APIKey 或APISecret 为空！请打开demo代码，填写相关信息。'}

        return process_data


if __name__ == '__main__':
    APPID = "5ff6cfc7"  # 应用ID（到控制台获取）
    APIKey = "c06ba7f73f267583e0f2fbc4c39d7a1c"  # 接口APIKey（到控制台拍照速算服务页面获取）
    Secret = "00552b54926214015411d9d9c1aad5b0"  # 接口APISercet（到控制台拍照速算服务页面获取）
    #
    host = "rest-api.xfyun.cn"  # 示例:  host="rest-api.xfyun.cn"域名形式
    res = WEBITRTEACH(APPID, APIKey, Secret, host, r'..//..//static//images//upload//itrteach.jpg',
                      r'..//..//static//images//upload//itrteach_result.jpg').itrteach_analysis()
    print(res)
