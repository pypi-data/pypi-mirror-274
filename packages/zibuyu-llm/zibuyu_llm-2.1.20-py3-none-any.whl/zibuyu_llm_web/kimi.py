# -*- coding: utf-8 -*-

"""
--------------------------------------------
project: zibuyu_LLM
author: 子不语
date: 2024/5/2
contact: 【公众号】思维兵工厂
description: 逆向Kimi。

实现基本对话功能，尚未逆向文档上传。

refresh_token获取方法：
    1. 在官网聊天界面登录后；
    2. 打开开发者模式，在终端输入：window.localStorage.getItem('refresh_token')
--------------------------------------------
"""

import os
import json
import logging
from json import JSONDecodeError
from typing import Callable

import requests

from .base import LLMBase
from .errors import NeedLoginError
from .types import ReferenceLink, AiAnswer

# 一个用于测试的token，随时可能失效
TEST_TOKEN = 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTcyMjQzMTE3MiwiaWF0IjoxNzE0NjU1MTcyLCJqdGkiOiJjb3BvdmgydWw3MjI3dHFodWZoZyIsInR5cCI6InJlZnJlc2giLCJzdWIiOiJjbmc0cDgxa3FxNGg3cDY5dm1nZyIsInNwYWNlX2lkIjoiY24xcGF1bzNyMDdhcmRnNnM0aTAiLCJhYnN0cmFjdF91c2VyX2lkIjoiY24xcGF1bzNyMDdhcmRnNnM0aGcifQ.0zOu2bYYB4OdBtQTFRX5Vo-6hHQC6eqZRX1a3Z40rSGdM2vNQvtHXXFhbcISt_bu6J1vI8aDXlxIB68WbWRQRQ'


class KimiWeb(LLMBase):
    """
    Kimi Web逆向
    """

    model_name = 'Kimi'
    base_host = 'https://kimi.moonshot.cn'

    def __init__(
            self,
            refresh_token: str = None,
            logger_obj: logging.Logger = None,
            error_dir: str = None
    ):
        """
        :param refresh_token: 登录后获取的refresh_token
        :param logger_obj: 日志对象
        :param error_dir: 错误日志保存目录
        """

        if not refresh_token:
            self.refresh_token = TEST_TOKEN
        else:
            self.refresh_token = refresh_token

        self.logger = logger_obj
        self.error_dir = error_dir

        super().__init__()

        self._access_token: str = ''
        self.headers = {
            "accept": "*/*",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "User-Agent": self.user_agent,
            "Cache-Control": 'no-cache',
            "Pragma": 'no-cache',

            "sec-ch-ua": "\"Not A(Brand\";v=\"99\", \"Microsoft Edge\";v=\"121\", \"Chromium\";v=\"121\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin"
        }

        self._chat_id: str = ''
        self.group_id: str = ''

        self.single_answer: str = ''
        self.single_answer_obj: AiAnswer = AiAnswer()
        self.single_answer_obj.reference_link_list = []
        self.reference_link_index_list = []  # 链接索引列表，用来判断该链接是否已记录

        self.single_answer_url_list: list = []

    def get_new_token(self):
        """ 刷新token """

        uri = "/api/auth/token/refresh"

        headers = self.headers.copy()
        headers['authorization'] = 'Bearer ' + self.refresh_token

        response = self.request_session.get(
            self.base_host + uri,
            headers=headers,
            allow_redirects=True
        )

        file_path = os.path.join(self.resource_path, '.Kimi_refresh_token.txt')

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(response.json()['refresh_token'])

        self._access_token = response.json()['access_token']
        self.refresh_token = response.json()['refresh_token']

        return self._access_token

    @property
    def access_token(self):

        if self._access_token:
            return self._access_token

        return self.get_new_token()

    @property
    def kimi_cookies(self):
        return 'Bearer ' + self.access_token

    @property
    def chat_id(self):
        """ 获取聊天id，Kimi对于会话窗口的管理，是将chat_id嵌入到URL中的 """
        if self._chat_id:
            return self._chat_id

        return self.get_chat_id()

    def get_chat_id(self):
        """ 获取聊天id """

        url = "https://kimi.moonshot.cn/api/chat"

        headers = self.headers.copy()
        headers['authorization'] = self.kimi_cookies

        data = {
            "name": "KimiChat API",
            "is_example": False
        }

        try:
            r = requests.post(url, headers=headers, json=data)
            if r.status_code == 200:
                self._chat_id = r.json()['id']
                self.logger.info(f'成功新建聊天id，chat_id: 【{self._chat_id}】')
                return self._chat_id
        except:
            self.logger.error(f'获取聊天id失败')

    def ask(
            self,
            question: str,
            search_model: bool = True,
            chat_id: str = None,
            kimi_plus_id: str = None,
            callback_func=None,
            perfect_prompt: bool = False
    ) -> AiAnswer:
        """
        向AI提问。
        Kimi官方提供了一个提示词专家，如果perfect_prompt为真，将自动使用该助手。
        :param question: 向AI交互的文本
        :param search_model: 是否开启联网搜索
        :param chat_id: 保证上下文
        :param kimi_plus_id: Kimi助手id
        :param callback_func: 回调函数
        :param perfect_prompt: 是否是优化提示词
        :return: AiAnswer（失败时为空对象）
        """

        # 如果用户传入了chat_id，则使用用户的chat_id
        if chat_id:
            self._chat_id = chat_id

        if not kimi_plus_id and perfect_prompt:
            kimi_plus_id = 'conpg00t7lagbbsfqkq0'

        # 如果用户没有传入chat_id，则新建，kimi的通讯必须要有chat_id
        if not self.chat_id:
            self.logger.error(f'chat_id为空，通讯失败')
            return AiAnswer()

        data = {
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ],
            "refs": [],  # TODO 上传文档时，在这里添加文档id
            "use_search": search_model,
            'kimiplus_id': kimi_plus_id if kimi_plus_id else 'kimi'
        }

        uri = '/api/chat/' + str(self.chat_id) + '/completion/stream'

        headers = self.headers.copy()
        headers['authorization'] = self.kimi_cookies

        response = requests.post(
            self.base_host + uri,
            json=data,
            headers=headers,
            stream=True
        )

        if response.status_code != 200:
            self.logger.error(f'AI交互请求失败，状态码：{response.status_code}')
            return AiAnswer()

        for line in response.iter_lines():

            if not line:
                continue

            try:
                error_msg = json.loads(line)
                error_type = error_msg['error_type']
                message = error_msg['message']

                if error_type == 'auth.token.invalid':
                    self.logger.error(f'{message}')
                    raise NeedLoginError(message)
            except JSONDecodeError:
                pass

            try:
                self.parse_data(line, callback_func)
            except:
                self.logger.error(f'解析数据失败，line: {line.decode()}')

        # 封装回答
        self.single_answer_obj.is_success = True
        self.single_answer_obj.content = self.single_answer.replace('^', '')
        self.single_answer_obj.conversation_id = self.chat_id

        return self.single_answer_obj

    def parse_data(self, line: bytes, callback_func: Callable = None):
        """ 解析数据 """

        line = line.decode('utf-8')
        json_data = json.loads(line[6:])
        event = json_data['event']

        if event == 'ping':  # 测试连通性，无意义
            pass
        elif event == 'resp':  # 第一次回复，主要返回请求确认信息
            self.group_id = json_data['group_id']
        elif event == 'req':  # 第一次回复，主要返回请求确认信息
            pass
        elif event == 'cmpl':  # 流式输出回复
            padding = json_data.get('text', '').replace('^', '')

            if callable(callback_func):
                try:
                    callback_func(padding)
                except:
                    self.logger.error(f'回调函数执行失败')

            self.single_answer += padding
        elif event == 'ref_docs':
            pass
        elif event == 'search_plus':

            index = json_data['msg']['successNum']

            if index in self.reference_link_index_list:
                pass

            self.reference_link_index_list.append(index)

            obj = ReferenceLink(
                title=json_data['msg']['title'],
                url=json_data['msg']['url'],
                index=index,
            )
            self.single_answer_obj.reference_link_list.append(obj)

        elif event == 'all_done':
            if callable(callback_func):
                try:
                    callback_func(self.end_signal)
                except:
                    self.logger.error(f'回调函数执行失败')

    def send_sms_code(self, phone: str) -> bool:
        """
        发送验证码。与login方法配合实现登录
        :param phone: 手机号
        :return: 成功时返回True, 失败时返回False
        """

        if len(phone) != 11:
            self.logger.error(f'目前仅支持国内手机，手机号格式错误')
            return False

        uri = '/api/user/sms/verify-code'

        data = {
            "action": "register",
            "phone": phone,
        }

        headers = self.headers.copy()
        headers['Content-Type'] = 'application/json'
        headers['Origin'] = 'https://kimi.moonshot.cn'
        headers['Referer'] = 'https://kimi.moonshot.cn/'

        response = requests.post(
            self.base_host + uri,
            json=data,
            headers=headers,
        )

        if response.status_code == 200:
            self.logger.info(f'发送验证码成功')
            return True

        self.logger.error(f'发送验证码失败')
        return False

    def login(self, phone: str, sms_code: str):
        """
        登录
        :param phone: 手机号
        :param sms_code: 验证码
        :return:
        """

        uri = '/api/user/register/trial'

        data = {
            "phone": phone,
            "verify_code": sms_code,
            "wx_user_id": ''
        }

        headers = self.headers.copy()
        headers['Content-Type'] = 'application/json'
        headers['Origin'] = 'https://kimi.moonshot.cn'
        headers['Referer'] = 'https://kimi.moonshot.cn/'

        response = requests.post(
            self.base_host + uri,
            json=data,
            headers=headers,
        )

        if response.status_code == 200:
            self.logger.info(f'登录成功')
            data = response.json()

            self._access_token = data['access_token']
            self.refresh_token = data['refresh_token']
            return True

        self.logger.error(f'登录失败')
        return False
