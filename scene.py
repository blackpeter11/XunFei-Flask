# #!/usr/bin/python
# # -*- coding: UTF-8 -*-

# import os
# import json
# from flask import Flask, render_template, request
# from business.scene.ocr_scenes import OcrScene  # 场景识别方法

# UPLOAD_FOLDER = r'static/images/upload/'  # 文件存放路径
# UPLOAD_SCENE_IMAGE = 'scene.jpg'  # 场景图片的文件名

# app = Flask(__name__)  # 创建程序实例
# app.config['UPLOAD_SCENE_IMAGE'] = UPLOAD_FOLDER + UPLOAD_SCENE_IMAGE  # 场景图像路径


# def clear_pic(file_path):
#     """
#     清空图片
#     :param file_path:
#     :return:
#     """
#     if os.path.exists(file_path):
#         os.remove(file_path)


# def clear_scene_pic(file_path=None):
#     """
#     清空场景图片
#     :return:
#     """
#     # 如果存在上传文件，则删除
#     clear_pic(app.config['UPLOAD_SCENE_IMAGE'])


# @app.route('/')
# def index():
#     return render_template('scene/index.html')  # send_file('face/home.html')


# @app.route('/secne')
# def feature():
#     """
#     人脸分析页面
#     :return:
#     """
#     clear_scene_pic()  # 刷新页面时候，清除之前上传的文件
#     return render_template('scene/ocr_scene.html')  # send_file('index.html')


# @app.route('/upload', methods=['post'])
# def up_photo():
#     """
#     上传图片
#     :return:
#     """
#     img = request.files.get('upfile')  # 获取文件内容
#     # type = request.form.get('type')  # 获取文件类型
#     path = app.config['UPLOAD_SCENE_IMAGE']
#     clear_scene_pic(path)  # 如果存在文件，则删除
#     img.save(path)  # 保存文件
#     return ''


# @app.route('/ocr_scene', methods=['post'])
# def ocr_scene():
#     """
#     场景识别页面
#     :return:
#     """
#     res = dict()
#     # TODO:判断是否存在待分析的图片
#     if not os.path.exists(app.config['UPLOAD_SCENE_IMAGE']):
#         res['flag'] = 'false'
#         res['msg'] = '请上传图片'
#     else:
#         res['flag'] = 'true'
#         APPID = "5ff6cfc7"  # 应用ID
#         API_KEY = "199cb73af0eb25f95039de10cc1cf704"  # 接口密钥
#         # TODO:调用场景识别类获取分析结果
#         data=OcrScene(APPID,API_KEY,app.config['UPLOAD_SCENE_IMAGE']).scene_local_analysis()
#         res['data'] = data
#         print(res)
#     return json.dumps(res)


# if __name__ == '__main__':
#     app.run(debug=True)
