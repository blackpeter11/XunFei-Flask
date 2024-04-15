#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import json
from flask import Flask, render_template, request
from business.object.ocr_object import OcrObject

UPLOAD_FOLDER = r'static/images/upload/'  # 文件存放路径
UPLOAD_OBJECT_IMAGE = 'object.jpg'  # 物体图片的文件名
LABEL_PATH = r'static/files/label.xlsx'  # 物体码Excel路径
app = Flask(__name__)  # 创建程序实例
app.config['UPLOAD_OBJECT_IMAGE'] = UPLOAD_FOLDER + UPLOAD_OBJECT_IMAGE  # 物体识别图像路径
app.config['LABEL_PATH'] = LABEL_PATH  # 物体码Excel路径


def clear_pic(file_path):
    """
    清空图片
    :param file_path:
    :return:
    """
    if os.path.exists(file_path):
        os.remove(file_path)


def clear_object_pic(file_path=None):
    """
    清空场景图片
    :return:
    """
    # 如果存在上传文件，则删除
    clear_pic(app.config['UPLOAD_OBJECT_IMAGE'])


@app.route('/')
def index():
    return render_template('object/home.html')  # send_file('face/home.html')


@app.route('/object')
def object():
    """
    人脸分析页面
    :return:
    """
    clear_object_pic()  # 刷新页面时候，清除之前上传的文件
    return render_template('object/ocr_object.html')  # send_file('index.html')


@app.route('/upload', methods=['post'])
def up_photo():
    """
    上传图片
    :return:
    """
    img = request.files.get('upfile')  # 获取文件内容
    # type = request.form.get('type')  # 获取文件类型
    path = app.config['UPLOAD_OBJECT_IMAGE']
    clear_object_pic()  # 如果存在文件，则删除
    img.save(path)  # 保存文件
    return ''


@app.route('/ocr_object', methods=['post'])
def ocr_object():
    """
    物体识别界面
    :return:
    """
    res = {}
    # TODO:判断是否存在待分析的图片
    if not os.path.exists(app.config['UPLOAD_OBJECT_IMAGE']):
        res['flag'] = 'false'
        res['msg'] = '请上传图片'
    else:
        res['flag'] = 'true'
        APPID = "5965e82d"  # 应用ID
        API_KEY = "7eb600e6f6148104ac29554acee9d9dc"  # 接口密钥
        # TODO:调用OcrObject类获取分析结果
        data=OcrObject(APPID,API_KEY,app.config['UPLOAD_OBJECT_IMAGE'],app.config['LABEL_PATH']).object_local_analysis()
        res['data'] = data
    return json.dumps(res)


if __name__ == '__main__':
    app.run(debug=True)
