# -*- coding: utf-8 -*-

"""
--------------------------------------------
project: zibuyu_LLM
author: 子不语
date: 2024/5/17
contact: 【公众号】思维兵工厂
description: 秘塔AI搜索web逆向

已实现登录获取cookie
--------------------------------------------
"""

import json
import logging
from typing import Literal

from bs4 import BeautifulSoup

from .types import AiAnswer, ReferenceLink
from .base import LLMBase, END_SIGNAL


class MetaSoWeb(LLMBase):
    """
    秘塔AI搜索web逆向
    """

    model_name = 'MetaSo'
    base_host = 'https://metaso.cn'

    def __init__(
            self,
            logger_obj: logging.Logger = None,
            error_dir: str = None
    ):
        self.error_dir = error_dir
        self.logger = logger_obj
        super().__init__()

        self.__token: str = ''  # 用来存放token

        self.__headers = {
            'Accept': "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "zh-CN,zh;q=0.9",
            'Origin': "https://metaso.cn",
            'Host': "metaso.cn",
            "Sec-Ch-Ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": self.user_agent,
        }

        self.single_answer: str = ''  # Ai回复的完整内容
        self.single_padding: str = ''  # Ai回复的增量部分
        self.single_answer_obj: AiAnswer = AiAnswer()
        self.single_answer_obj.reference_link_list = []

        self._sid: str = ''  # 鉴权相关
        self._uid: str = ''  # 鉴权相关

    @property
    def token(self):

        if not self.__token:
            self.__token = self.get_token()

        return self.__token

    def get_token(self):
        """ 获取token """

        url = 'https://metaso.cn/'

        headers = self.__headers.copy()

        headers['Sec-Fetch-Dest'] = 'document'
        headers['Sec-Fetch-Mode'] = 'navigate'
        headers['Sec-Fetch-User'] = '?1'
        headers['Upgrade-Insecure-Requests'] = '1'
        headers['Accept'] = 'text/html,application/xml;q=0.9,'
        headers['Host'] = 'metaso.cn'

        response = self.request_session.get(url=url, headers=headers)

        main_soup = BeautifulSoup(response.text, 'html.parser')

        token = main_soup.find('meta', attrs={'id': 'meta-token'})['content']

        if not token:
            self.logger.error('获取token失败')
            raise Exception('获取token失败')

        self.logger.info(f'成功获取token: 【{token}】')
        return token

    def get_session_id(
            self,
            question: str,
            engine_type: str = '',
            scholar_search_domain: str = 'all',
            mode: str = 'detail',
    ):
        """ 获取session_id """

        uri = '/api/session'

        data = {
            "question": question,
            "mode": mode,
            "engineType": engine_type,
            "scholarSearchDomain": scholar_search_domain
        }

        headers = self.__headers.copy()
        headers['Is-Mini-Webview'] = '0'
        headers['Token'] = self.token

        response = self.request_session.post(
            url=self.base_host + uri,
            json=data,
            headers=headers,
        )

        resp_json = response.json()

        session_id = resp_json.get('data', {}).get('id')
        if not session_id:
            self.logger.error('获取session_id失败')
            raise Exception('获取session_id失败')

        self.logger.info(f'成功获取session_id: 【{session_id}】')
        return session_id

    def ask(
            self,
            question: str,
            lang: str = 'zh',
            engine_type: Literal['podcast', 'scholar',] = '',
            mode: Literal['concise', 'detail', 'research'] = 'detail',
            is_mini_webview: int = 0,
            callback_func=None
    ):
        """
        提问
        :param question: 问题
        :param lang: 语言
        :param engine_type: 搜索类型：全网（为空）、学术（scholar）、播客（podcast）
        :param mode: 模式：concise（简洁）；detail（深入）；research（学术）
        :param is_mini_webview: 是否是mini webview
        :param callback_func: 回调函数
        :return:
        """

        uri = '/api/searchV2'

        if mode not in ['concise', 'detail', 'research']:
            self.logger.error('mode参数错误，使用默认【concise】')
            mode = 'concise'

        if engine_type not in ['podcast', 'scholar', ]:
            self.logger.error('engineType参数错误，使用默认【concise】')
            mode = ''

        session_id = self.get_session_id(
            question=question,
            mode=mode,
            engine_type=engine_type
        )

        params = {
            "sessionId": session_id,
            "question": question,
            "lang": lang,
            "mode": mode,
            "searchType": '',
            "is-mini-webview": is_mini_webview,
            "token": self.token,
        }

        headers = self.__headers.copy()
        headers['Token'] = self.token
        headers['Is-Mini-Webview'] = '0'

        response = self.request_session.get(
            url=self.base_host + uri,
            params=params,
            headers=headers,
            stream=True,
        )

        padding = ''

        for line in response.iter_lines():

            if not line:
                continue

            padding += line.decode('utf-8')

            if not padding.endswith('}') and not padding.endswith(']'):
                print('数据不完全')
                continue

            if padding == 'data:[DONE]':

                if callable(callback_func):
                    try:
                        callback_func(END_SIGNAL)
                    except:
                        self.logger.error('回调函数执行失败')

                self.single_answer_obj.content = self.single_answer

                return self.single_answer_obj

            data = json.loads(padding.split(':', maxsplit=1)[-1])
            padding = ''

            message_type = data.get('type')

            if message_type == 'heartbeat' or message_type == 'query':
                # 心跳包和查询确认包，不解析
                continue
            elif message_type == 'append-text':
                # 输出文本
                content = data.get('text')
                self.single_answer += content

                if callable(callback_func):
                    try:
                        callback_func(content)
                    except:
                        self.logger.error('回调函数执行失败')

            elif message_type == 'set-reference':
                # 相关链接
                reference_list = data.get('list', [])
                for index, reference in enumerate(reference_list, start=1):
                    reference_link = ReferenceLink(
                        title=reference.get('title'),
                        url=reference.get('link'),
                        index=index,
                    )
                    self.single_answer_obj.reference_link_list.append(reference_link)

        return self.single_answer_obj

    def send_sms_code(self, phone: str) -> bool:

        if not self.is_valid_cn_phone(phone):
            self.logger.error(f'输入号码【{phone}】不是合法的国内手机号')
            return False

        host = 'https://metaso.cn/verify?type=sms'
        data = {"phone": f"86-{phone}"}

        headers = self.__headers.copy()
        headers['Token'] = self.token
        headers['Is-Mini-Webview'] = '0'

        try:
            response = self.request_session.post(
                url=host,
                json=data,
                headers=headers,
            )

            resp_data = response.json()

            code = resp_data.get('code')

            if code == 0:
                self.logger.info('发送成功')
                return True

            self.logger.error(f'发送失败，错误码：{code}')
            return False
        except:
            self.logger.error('发送手机验证码发送未知错误！', exc_info=True)
            return False

    def login_by_phone(self, code: str):
        """
        手机验证码登录
        :param code: 验证码
        :return: 登录之后，请求头的cookie更新了
        """

        host = f'https://metaso.cn/verify?type=sms&content={code}'

        headers = self.__headers.copy()
        headers['Token'] = self.token
        headers['Is-Mini-Webview'] = '0'

        try:
            response = self.request_session.get(
                url=host,
                headers=headers,
            )

            resp_data = response.json()
            code = resp_data.get('code')
            if code != 0:
                self.logger.info('手机登录失败')
                return

            uid = resp_data.get('data', {}).get('uid')
            sid = resp_data.get('data', {}).get('sid')

            cookie = self.request_session.cookies.get_dict()
            self._sid = cookie.get('sid')
            self._uid = cookie.get('uid')

            if self._sid == uid and self._uid == sid:
                self.logger.info('成功更新token')
                return True

            self.logger.error('手机登录失败')
            return False

        except:
            self.logger.error('手机登录失败', exc_info=True)
            return False

    def login_by_pwd(self, account: str, pwd: str):
        """
        登录
        :param account: 账号
        :param pwd: 密码的密文形式
        :return:
        """

        host = 'https://metaso.cn/login'

        headers = self.__headers.copy()
        headers['Token'] = self.token
        headers['Is-Mini-Webview'] = '0'

        data = {
            "login_by": "account",
            "account": account,
            "pwd": pwd
        }

        try:
            response = self.request_session.post(
                url=host,
                json=data,
                headers=headers,
            )

            resp_data = response.json()
            code = resp_data.get('code')
            if code != 0:
                self.logger.info('密码登录失败')
                return

            uid = resp_data.get('data', {}).get('uid')
            sid = resp_data.get('data', {}).get('sid')

            cookie = self.request_session.cookies.get_dict()
            self._sid = cookie.get('sid')
            self._uid = cookie.get('uid')

            if self._sid == uid and self._uid == sid:
                self.logger.info('成功更新token')
                return True

            self.logger.error('密码登录失败')
            return False

        except:
            self.logger.error('密码登录失败', exc_info=True)
            return False
