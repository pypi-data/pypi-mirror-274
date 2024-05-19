# -*- coding: utf-8 -*-

"""
--------------------------------------------
project: zibuyu_LLM
author: 子不语
date: 2024/5/17
contact: 【公众号】思维兵工厂
description: 
--------------------------------------------
"""

import base64
import logging
from typing import Literal

from .base import LLMBase


class EmohaaWeb(LLMBase):
    model_name = 'Emohaa'

    def __init__(
            self,
            token: str,
            logger_obj: logging.Logger = None,
            error_dir: str = None
    ):
        self.token = token
        self.error_dir = error_dir
        self.logger = logger_obj
        super().__init__()

        self.__headers = {
            'Accept': "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "zh-CN,zh;q=0.9",
            'Origin': "https://echo.turing-world.com",
            'Referer': "https://echo.turing-world.com/",
            'Host': "metaso.cn",
            "Sec-Ch-Ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",

            "X-Xss-Id": "0.06979938082110193",
            "X-Xss-Real": "6abb1b42063a4048b28fa39ae3b752d6",
            "X-Xss-Ts": "1715941102117",

            "Authorization": f"Bearer {self.token}",
            "User-Agent": self.user_agent
        }

    def text2voice(
            self,
            text: str,
            output_file_path: str,
            voice_id: Literal['BV700_V2_streaming', 'BV002_streaming'] = 'BV700_V2_streaming'
    ) -> bool:
        """
        将文本转换为语音
        :param text:
        :param output_file_path:
        :param voice_id: 音色ID
        :return: 成功时返回True，失败返回False
        """
        # BV002_streaming
        params = {
            'text': text,
            'voice_type': voice_id
        }

        host = 'https://ai-role.cn/echo-prod/tts'

        try:
            response = self.request_session.get(host, params=params, headers=self.__headers)

            if response.status_code != 200:
                self.logger.error(f'{output_file_path} 语音生成失败')
                print(response.text)
                return False

            # 解码
            decoded_data = base64.b64decode(response.content)

            with open(output_file_path, 'wb') as f:
                f.write(decoded_data)

            return True
        except:
            self.logger.error(f'{output_file_path} 语音生成失败')
            return False
