#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import json
from flask import Flask, render_template, request

from business.face.face_feature_analysis import FaceFeature  # 人脸特征分析方法
from business.face.face_compare import FaceCompare  # 人脸比对方法

UPLOAD_FOLDER = r'static/images/upload/'  # 文件存放路径
UPLOAD_FEATURE_IMAGE = 'feature.jpg'  # 人脸特征图片的文件名
UPLOAD_COMPARE1_IMAGE = 'compare1.jpg'  # 人脸比对图片1的文件名
UPLOAD_COMPARE2_IMAGE = 'compare2.jpg'  # 人脸比对图片2的文件名

app = Flask(__name__)  # 创建程序实例
app.config['UPLOAD_FEATURE_IMAGE'] = UPLOAD_FOLDER + UPLOAD_FEATURE_IMAGE  # 人脸特征分析图像路径
app.config['UPLOAD_COMPARE1_IMAGE'] = UPLOAD_FOLDER + UPLOAD_COMPARE1_IMAGE  # 人脸比对图像1路径
app.config['UPLOAD_COMPARE2_IMAGE'] = UPLOAD_FOLDER + UPLOAD_COMPARE2_IMAGE  # 人脸比对图像2路径


def clear_pic(file_path):
    """
    清空图片
    :param file_path:
    :return:
    """
    if os.path.exists(file_path):
        os.remove(file_path)


def clear_feature_pic(file_path=None):
    """
    清空人脸特征图片
    :return:
    """
    # 如果存在上传文件，则删除
    clear_pic(app.config['UPLOAD_FEATURE_IMAGE'])


def clear_compare_pic(file_path=None):
    """
    清空人脸比对图片
    :return:
    """
    # 如果存在上传文件，则删除
    clear_pic(app.config['UPLOAD_COMPARE1_IMAGE'])
    clear_pic(app.config['UPLOAD_COMPARE2_IMAGE'])


@app.route('/')
def index():
    return render_template('face/home.html')  # send_file('face/home.html')


@app.route('/feature')
def feature():
    """
    人脸分析页面
    :return:
    """
    clear_feature_pic()  # 刷新页面时候，清除之前上传的文件
    return render_template('face/feature_analysis.html')  # send_file('index.html')


@app.route('/upload', methods=['post'])
def up_photo():
    """
    上传图片
    :return:
    """
    img = request.files.get('upfile')  # 获取文件内容
    type = request.form.get('type')  # 获取文件类型
    print(type)
    if type == 'feature':
        path = app.config['UPLOAD_FEATURE_IMAGE']
    elif type == 'compare1':
        path = app.config['UPLOAD_COMPARE1_IMAGE']
    else:
        path = app.config['UPLOAD_COMPARE2_IMAGE']
    clear_pic(path)  # 如果存在文件，则删除
    img.save(path)  # 保存文件
    return ''


@app.route('/feature_analysis', methods=['post'])
def feature_analysis():
    """
    人脸特征分析页面
    :return:
    """
    res = {}
    # TODO:判断是否存在待分析的图片
    if not os.path.exists(app.config['UPLOAD_FEATURE_IMAGE']):
        res['flag'] = 'false'
        res['msg'] = '请上传图片'
    else:
        res['flag'] = 'true'
        APPID = "5965e82d"  # 应用ID
        API_KEY = "7eb600e6f6148104ac29554acee9d9dc"  # 接口密钥
        # TODO:调用人脸特征类获取分析结果
        data=FaceFeature(APPID,API_KEY,app.config['UPLOAD_FEATURE_IMAGE']).face_local_analysis()
        res['data'] = data
    return json.dumps(res)


@app.route('/compare')
def compare():
    """
    人脸分析页面
    :return:
    """
    clear_compare_pic()
    return render_template('face/feature_compare.html')


@app.route('/feature_compare', methods=['post'])
def feature_compare():
    """
    人脸比对页面
    :return:
    """
    res = {}
    # TODO:判断是否存在待分析的图片
    if not os.path.exists(app.config['UPLOAD_COMPARE1_IMAGE']):
        res['flag'] = 'false'
        res['msg'] = '请上传左边的图片'
    elif not os.path.exists(app.config['UPLOAD_COMPARE2_IMAGE']):
        res['flag'] = 'false'
        res['msg'] = '请上传右边的图片'
    else:
        res['flag'] = 'true'
        appid = '5965e82d'  # 应用ID
        api_secret = 'f091fd2e638c7e06de4276de1092d90c'  # 接口secret
        api_key = '5a36e098821e4a5a3b05428b0340e1ac'  # 接口密钥
        # TODO:调用人脸比对类获取分析结果
        data=FaceCompare(appid,api_secret,api_key,app.config['UPLOAD_COMPARE1_IMAGE'],app.config['UPLOAD_COMPARE2_IMAGE']).run()
        res['data'] = data
    return json.dumps(res)


if __name__ == '__main__':
    app.run(debug=True)
