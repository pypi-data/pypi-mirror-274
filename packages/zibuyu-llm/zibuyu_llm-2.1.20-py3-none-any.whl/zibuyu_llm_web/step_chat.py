# -*- coding: utf-8 -*-

"""
--------------------------------------------
project: zibuyu_LLM
author: 子不语
date: 2024/5/18
contact: 【公众号】思维兵工厂
description: 【未完成】
--------------------------------------------
"""

import json
import struct
import logging
import time
from typing import Union, Optional

from .base import LLMBase, END_SIGNAL
from .types import AiAnswer, ReferenceLink


class StepChatWeb(LLMBase):
    """
    StepChatWeb
    """

    model_name = 'StepChatWeb'

    base_host = 'https://yuewen.cn'

    def __init__(
            self,
            access_token: str = None,
            refresh_token: str = None,
            oasis_web_id: str = None,
            logger_obj: logging.Logger = None,
            error_dir: str = None
    ):
        """
        StepChatWeb
        :param access_token:
        :param refresh_token:
        :param oasis_web_id: 设备id，该id与登录态绑定
        :param logger_obj:
        :param error_dir:
        """

        self.logger = logger_obj
        self.error_dir = error_dir

        super().__init__()

        self._access_token: str = access_token or ''  # 存储登录后的access_token
        self._refresh_token: str = refresh_token or ''  # 存储登录后的refresh_token
        self._oasis_web_id: str = oasis_web_id or ''  # 请求头参数，通过register_device接口获取
        self.cookie: str = f"Oasis-Webid={self._oasis_web_id}; Oasis-Token={self._access_token}...{self._refresh_token}"

        self.request_session.cookies.update({
            'Oasis-Webid': self._oasis_web_id,
            'Cookie': f"Oasis-Webid={self._oasis_web_id}; Oasis-Token={self._access_token}...{self._refresh_token}",
        })

        self.__headers = {
            'Accept': "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "zh-CN,zh;q=0.9",
            'Origin': "https://yuewen.cn",
            'Cookie': self.cookie,
            "Connect-Protocol-Version": "1",
            "Oasis-Appid": "10200",
            "Oasis-Platform": "web",
            "Sec-Ch-Ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": self.user_agent,
        }

        self.single_answer: str = ''
        self.single_padding: str = ''
        self.single_answer_obj: AiAnswer = AiAnswer()
        self.single_answer_obj.reference_link_list = []

        self.single_chat_id: str = ''

        self.single_message_id: str = ''  # 本次交互消息id
        self.latest_message_id: str = ''  # 上一次消息id

    @property
    def oasis_web_id(self):

        if not self._oasis_web_id:
            self.register_device()

        return self._oasis_web_id

    @property
    def oasis_token(self):

        if not self.cookie:
            self.register_device()
        return self.cookie

    def get_expire_time(self, token: str):

        payload = self.parse_jwt_token(token)
        return payload['exp']

    @property
    def access_token(self):

        now = int(time.time())

        if now > self.access_token_expire:
            self.logger.info(f'access Token 过期了，需要刷新')
            self.register_device()

        if self._access_token:
            return self._access_token

    @property
    def access_token_expire(self):

        return self.get_expire_time(self._access_token)

    @property
    def refresh_token_expire(self):
        return self.get_expire_time(self._refresh_token)

    @property
    def refresh_token(self):

        now = int(time.time())

        if now > self.refresh_token_expire:
            self.logger.info(f'refresh Token 过期了，需要重新登录')
            raise Exception('refresh Token 过期了，需要重新登录')

        if self._refresh_token:
            return self._refresh_token

    def scan_index(self):
        """ 访问首页，获取初始Token """

        host = 'https://yuewen.cn/chats/new'

        response = self.request_session.get(
            url=host,
            headers=self.__headers,
        )

        if response.status_code == 200:
            self.logger.info(f'[跃问] 首页访问成功')
            print(self.request_session.cookies.get_dict())
            return True
        else:
            self.logger.error(f'[跃问] 首页访问失败，状态码：{response.status_code}')
            return False

    def send_sms_code(self, phone: Union[str, int]) -> bool:

        self.register_device()

        if not self.is_valid_cn_phone(phone):
            self.logger.error(f'[跃问] 输入号码【{phone}】不是合法的国内手机号')
            return False

        uri = '/passport/proto.api.passport.v1.PassportService/SendVerifyCode'

        data = {
            "mobileCc": "86",
            "mobileNum": phone
        }

        headers = self.__headers.copy()
        headers['Content-Type'] = 'application/json'
        headers['Referer'] = 'https://yuewen.cn/chats/new'

        try:
            response = self.request_session.post(
                url=self.base_host + uri,
                headers=headers,
                json=data
            )

            if response.status_code == 200:
                self.logger.info(f'[跃问] 发送验证码成功，手机号：{phone}')
                return True
            else:
                self.logger.error(f'[跃问] 发送验证码失败，手机号：{phone}')
                return False
        except:
            self.logger.error(f'[跃问] 发送验证码失败，手机号：{phone}', exc_info=True)
            return False

    def login(self, phone: Union[str, int], sms_code: Union[str, int]):

        if not self.is_valid_cn_phone(phone):
            self.logger.error(f'输入号码【{phone}】不是合法的国内手机号')
            return False

        uri = '/passport/proto.api.passport.v1.PassportService/SignIn'

        data = {
            "authCode": "9138",
            "mobileCc": "86",
            "mobileNum": "13602714584"
        }

        headers = self.__headers.copy()
        headers['Content-Type'] = 'application/json'
        headers['Referer'] = 'https://yuewen.cn/chats/new'

        try:
            response = self.request_session.post(
                url=self.base_host + uri,
                headers=headers,
                json=data
            )

            resp_data = response.json()
            self._access_token = resp_data.get('accessToken', {}).get('raw')
            self._refresh_token = resp_data.get('refreshToken', {}).get('raw')

            if self._access_token and self._refresh_token:
                self.logger.info(f'[跃问] 登录成功，手机号：{phone}')
                return True

            self.logger.error(f'[跃问] 登录失败，手机号：{phone}')
            return False

        except:
            self.logger.error(f'[跃问] 登录出现未知错误\n\n手机号：【{phone}】\n验证码：【{sms_code}】', exc_info=True)
            return False

    def register_device(self):
        """ 注册设备：该接口返回的设备与登录态绑定 """

        host = '/passport/proto.api.passport.v1.PassportService/RegisterDevice'

        response = self.request_session.post(
            url=self.base_host + host,
            headers=self.__headers,
            json={}
        )

        if response.status_code == 200:
            self.logger.info(f'[跃问] 注册设备成功')

            resp_data = response.json()
            self._access_token = resp_data.get('accessToken', {}).get('raw')
            self._refresh_token = resp_data.get('refreshToken', {}).get('raw')

            data = self.request_session.cookies.get_dict()
            self._oasis_web_id = data.get('Oasis-Webid')
            self.cookie = f"Oasis-Webid={self._oasis_web_id}; Oasis-Token={self.access_token}...{self.refresh_token}",

            return True
        else:
            self.logger.error(f'[跃问] 注册设备失败，状态码：{response.status_code}')
            return False

    def create_chat(self, chat_name: str = "新会话") -> Optional[str]:
        """ 创建会话 """

        uri = '/api/proto.chat.v1.ChatService/CreateChat'

        data = {"chatName": chat_name}

        try:
            response = self.request_session.post(
                url=self.base_host + uri,
                headers=self.__headers,
                json=data
            )

            if response.status_code != 200:
                self.logger.error(f'[跃问] 创建会话失败，状态码：{response.status_code}')
                return

            resp_data = response.json()

            chat_id = resp_data.get('chatId')

            if not chat_id:
                self.logger.error(f'[跃问] 创建会话失败')
                return

            self.logger.info(f'[跃问] 创建会话成功，会话ID：{chat_id}')
            self.single_chat_id = chat_id
            return chat_id
        except:
            self.logger.error(f'[跃问] 创建会话发生未知错误', exc_info=True)

    @staticmethod
    def wrap_data(json_str):
        # 将 JSON 字符串转换为字节数据
        data = json_str.encode('utf-8')

        # 分配新的字节缓冲区，比原始数据多 5 个字节
        buffer_length = len(data) + 5
        buffer = bytearray(buffer_length)

        # 设置前缀值
        buffer[0] = 0x00  # 第一个字节设置为 0x00
        buffer[1:5] = struct.pack('>I', len(data))  # 接下来的 4 个字节设置为数据的长度 (大端序)

        # 将数据复制到缓冲区的第 5 个字节开始的位置
        buffer[5:] = data

        return buffer

    @staticmethod
    def parse_data(byte_data: bytes) -> list[dict]:
        """ 解析字节数据 """

        content_list = []
        offset = 1
        while offset < len(byte_data):
            chunk_size = struct.unpack_from(">I", byte_data, offset)[0]

            json_bytes = byte_data[offset - 1: offset - 1 + 5 + chunk_size]
            decoded_json = json.loads(json_bytes[5:].decode('utf-8'))
            content_list.append(decoded_json)
            offset += chunk_size + 5
        return content_list

    def ask(
            self,
            question: str,
            chat_id: str,
            callback_func=None,
    ) -> Optional[AiAnswer]:

        uri = '/api/proto.chat.v1.ChatMessageService/SendMessageStream'
        headers = self.__headers.copy()
        headers['Referer'] = f'https://yuewen.cn/chats/{chat_id}'
        headers['Content-Type'] = 'application/connect+json'
        headers['Oasis-Webid'] = self.oasis_web_id

        headers['Cookie'] = f"Oasis-Webid={self.oasis_web_id}; Oasis-Token={self.access_token}...{self.refresh_token}"

        # return
        data = {
            "chatId": chat_id,
            "messageInfo": {"text": question, "author": {"role": "user"}}
        }

        response = self.request_session.post(
            url=self.base_host + uri,
            headers=headers,
            data=self.wrap_data(json.dumps(data)),
        )

        if response.status_code != 200:
            self.logger.error(f'[跃问] AI交互失败，状态码：{response.status_code}')
            return

        content_list = self.parse_data(response.content)

        for content in content_list:

            try:
                if 'startEvent' in content:
                    self.single_message_id = content['startEvent']['messageId']
                    self.latest_message_id = content['startEvent']['parentMessageId']
                elif 'pipelineEvent' in content:
                    data = content['pipelineEvent']

                    search_result = data.get('eventSearch')

                    if not search_result:
                        continue

                    result: list = search_result.get('results')
                    if not result:
                        continue

                    for index, item in enumerate(result):
                        obj = ReferenceLink(
                            title=item.get('title'),
                            url=item.get('url'),
                            index=index,
                            description=item.get('snippet'),
                        )

                        self.single_answer_obj.reference_link_list.append(obj)
                elif 'textEvent' in content:

                    text = content.get('textEvent', {}).get('text')

                    if not text:
                        continue

                    self.single_padding = text
                    self.single_answer += text
                elif 'doneEvent' in content:

                    self.single_answer_obj.content = self.single_answer
                    self.single_answer_obj.is_success = True
                    self.single_answer_obj.latest_msg_id = self.latest_message_id
                    self.single_answer_obj.conversation_id = self.single_chat_id

                    if callable(callback_func):
                        try:
                            callback_func(END_SIGNAL)
                        except:
                            self.logger.error(f'[跃问] 回调函数执行失败', exc_info=True)
                else:
                    continue
            except:
                self.logger.error(f'[跃问] 解析数据失败，数据：{content}', exc_info=True)
                print(content)

        return self.single_answer_obj
