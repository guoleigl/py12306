from flask import Blueprint, request
from flask.json import jsonify
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity)

from py12306.config import Config
from py12306.user.job import UserJob
from py12306.user.user import User

user = Blueprint('user', __name__)


@user.route('/login', methods=['POST'])
def login():
    """
    用户登录
    :return:
    """
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if username and password and username == Config().WEB_USER.get('username') and password == Config().WEB_USER.get(
            'password'):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)
    return jsonify({"msg": "用户名或密码错误"}), 401


@user.route('/users', methods=['GET'])
def users():
    """
    用户任务列表
    :return:
    """
    jobs = User().users
    result = map(convert_job_to_info, jobs)
    return jsonify(result)


def convert_job_to_info(job: UserJob):
    return {
        'key': job.key,
        'user_name': job.user_name,
        'is_ready': job.is_ready,
        'is_loaded': job.user_loaded,  # 是否成功加载 ready 是当前是否可用
        'last_heartbeat': job.last_heartbeat
    }