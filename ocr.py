#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import json
from flask import Flask, render_template, request

from business.ocr.handwriting import HandWriting  # 手写文字识别
from business.ocr.yinshua import General  # 印刷文字识别
from business.ocr.WebITR import WEBITR  # 拍照速算识别
from business.ocr.WebITRTeach import WEBITRTEACH  # 公式识别

UPLOAD_FOLDER = r'static/images/upload/'  # 文件存放路径
UPLOAD_HAND_IMAGE = 'hand.jpg'  # 手写文字图片的文件名
UPLOAD_GENERAL_IMAGE = 'yinshua.jpg'  # 印刷文字图片的文件名
UPLOAD_ITR_IMAGE = 'itr.jpg'  # 速算图片的文件名
SHOW_ITR_IMAGE = 'itr_result.jpg'  # 速算识别结果的文件名
UPLOAD_ITRTEACH_IMAGE = 'itrteach.jpg'  # 公式的文件名
SHOW_ITRTEACH_IMAGE = 'itrteach_result.jpg'  # 公式识别结果的文件名

app = Flask(__name__)  # 创建程序实例
app.config['UPLOAD_HAND_IMAGE'] = UPLOAD_FOLDER + UPLOAD_HAND_IMAGE  # 手写文字图像路径
app.config['UPLOAD_GENERAL_IMAGE'] = UPLOAD_FOLDER + UPLOAD_GENERAL_IMAGE  # 印刷文字图像路径
app.config['UPLOAD_ITR_IMAGE'] = UPLOAD_FOLDER + UPLOAD_ITR_IMAGE  # 速算文字图像路径
app.config['SHOW_ITR_IMAGE'] = UPLOAD_FOLDER + SHOW_ITR_IMAGE  # 速算识别结果图像路径
app.config['UPLOAD_ITRTEACH_IMAGE'] = UPLOAD_FOLDER + UPLOAD_ITRTEACH_IMAGE  # 公式图像路径
app.config['SHOW_ITRTEACH_IMAGE'] = UPLOAD_FOLDER + SHOW_ITRTEACH_IMAGE  # 公式图像存储路径


def clear_pic(file_path):
    """
    清空图片
    :param file_path:
    :return:
    """
    if os.path.exists(file_path):
        os.remove(file_path)


def clear_handwriting_pic():
    """
    清空手写文字图片
    :return:
    """
    # 如果存在上传文件，则删除
    clear_pic(app.config['UPLOAD_HAND_IMAGE'])


def clear_general_pic():
    """
    清空印刷文字图片
    :return:
    """
    # 如果存在上传文件，则删除
    clear_pic(app.config['UPLOAD_GENERAL_IMAGE'])


def clear_itr_pic():
    """
    清空速算文字图片
    :return:
    """
    # 如果存在上传文件，则删除
    clear_pic(app.config['UPLOAD_ITR_IMAGE'])
    clear_pic(app.config['SHOW_ITR_IMAGE'])


def clear_itrteach_pic():
    """
    清空速算文字图片
    :return:
    """
    # 如果存在上传文件，则删除
    clear_pic(app.config['UPLOAD_ITRTEACH_IMAGE'])
    clear_pic(app.config['SHOW_ITRTEACH_IMAGE'])


@app.route('/')
def index():
    return render_template('ocr/home.html')  # send_file('face/home.html')


@app.route('/upload', methods=['post'])
def up_photo():
    """
    上传图片
    :return:
    """
    img = request.files.get('upfile')  # 获取文件内容
    type = request.form.get('type')  # 获取文件类型
    print(type)
    if type == 'hand':
        path = app.config['UPLOAD_HAND_IMAGE']
        clear_handwriting_pic()  # 删除文件
    elif type == 'general':
        path = app.config['UPLOAD_GENERAL_IMAGE']
        clear_general_pic()  # 删除文件
    elif type == 'itr':
        path = app.config['UPLOAD_ITR_IMAGE']
        clear_itr_pic()  # 删除文件
    else:  # itrteach
        path = app.config['UPLOAD_ITRTEACH_IMAGE']
        clear_itrteach_pic()  # 删除文件
    img.save(path)  # 保存文件
    return ''


@app.route('/handwriting')
def handwriting():
    """
    手写文字上传页面
    :return:
    """
    clear_handwriting_pic()  # 刷新页面时候，清除之前上传的文件
    return render_template('ocr/handwriting.html')  # send_file('index.html')


@app.route('/handapi', methods=['post'])
def hand_API():
    """
    手写文字页面
    :return:
    """
    res = {}
    # TODO:判断是否存在待分析的图片
    if not os.path.exists(app.config['UPLOAD_HAND_IMAGE']):
        res['flag'] = 'false'
        res['msg'] = '请上传图片'
    else:
        res['flag'] = 'true'
        APPID = '5ff6cfc7'  # 应用ID
        API_KEY = '81acbab379fa516044c0e8632787f314'  # 接口密钥
        # TODO:调用手写文字识别类获取分析结果
        data=HandWriting(APPID,API_KEY,app.config['UPLOAD_HAND_IMAGE']).handwriting_analysis()
        res['data'] = data
        print(res)
    return json.dumps(res)


@app.route('/general')
def general():
    """
    印刷文字页面
    :return:
    """
    clear_general_pic()  # 刷新页面时候，清除之前上传的文件
    return render_template('ocr/general.html')  # send_file('index.html')


@app.route('/generalapi', methods=['post'])
def general_API():
    """
    印刷文字页面
    :return:
    """
    res = {}
    # TODO:判断是否存在待分析的图片
    if not os.path.exists(app.config['UPLOAD_GENERAL_IMAGE']):
        res['flag'] = 'false'
        res['msg'] = '请上传图片'
    else:
        res['flag'] = 'true'
        APPID = '5ff6cfc7'  # 应用ID
        API_KEY = '81acbab379fa516044c0e8632787f314'  # 接口密钥
        # TODO:调用印刷文字识别类获取分析结果
        data=General(APPID,API_KEY,app.config['UPLOAD_GENERAL_IMAGE']).general_analysis()
        res['data'] = data
    return json.dumps(res)


@app.route('/itr')
def itr():
    """
    拍照速算识别
    :return:
    """
    clear_itr_pic()  # 刷新页面时候，清除之前上传的文件
    return render_template('ocr/itr.html')  # send_file('index.html')


@app.route('/itrapi', methods=['post'])
def itr_API():
    """
    拍照速算识别
    :return:
    """
    # TODO:判断是否存在待分析的图片
    res = {}
    if not os.path.exists(app.config['UPLOAD_ITR_IMAGE']):
        res['flag'] = 'false'
        res['msg'] = '请上传图片'
    else:
        APPID = "5ff6cfc7"  # 应用ID（到控制台获取）
        APIKey = "c06ba7f73f267583e0f2fbc4c39d7a1c"  # 接口APIKey（到控制台拍照速算服务页面获取）
        Secret = "00552b54926214015411d9d9c1aad5b0"  # 接口APISercet（到控制台拍照速算服务页面获取）
        host = "rest-api.xfyun.cn"  # 示例:  host="rest-api.xfyun.cn"域名形式
        # TODO:调用拍照速算识别类获取分析结果
        data=WEBITR(APPID,APIKey,Secret,host,app.config['UPLOAD_ITR_IMAGE'],app.config['SHOW_ITR_IMAGE']).itr_analysis()
        res = data
        res['path'] = app.config['SHOW_ITR_IMAGE']
    return json.dumps(res)


@app.route('/itr_teach')
def itr_teach():
    """
    公式识别
    :return:
    """
    clear_itrteach_pic()  # 刷新页面时候，清除之前上传的文件
    return render_template('ocr/itr_teach.html')  # send_file('index.html')


@app.route('/itrteachapi', methods=['post'])
def itr_teach_api():
    """
    公式识别
    :return:
    """
    res = {}
    # TODO:判断是否存在待分析的图片
    if not os.path.exists(app.config['UPLOAD_ITRTEACH_IMAGE']):
        res['flag'] = 'false'
        res['msg'] = '请上传图片'
    else:
        APPID = "5ff6cfc7"  # 应用ID（到控制台获取）
        APIKey = "c06ba7f73f267583e0f2fbc4c39d7a1c"  # 接口APIKey（到控制台拍照速算服务页面获取）
        Secret = "00552b54926214015411d9d9c1aad5b0"  # 接口APISercet（到控制台拍照速算服务页面获取）
        host = "rest-api.xfyun.cn"  # 示例:  host="rest-api.xfyun.cn"域名形式
        # TODO:调用公式识别类获取分析结果
        data=WEBITRTEACH(APPID,APIKey,Secret,host,app.config['UPLOAD_ITRTEACH_IMAGE'],app.config['SHOW_ITRTEACH_IMAGE']).itrteach_analysis()
        res = data
        res['path'] = app.config['SHOW_ITRTEACH_IMAGE']
    return json.dumps(res)


if __name__ == '__main__':
    app.run(debug=True)
