import requests
import json
from typing import Dict, Optional, Union, Tuple
from pathlib import Path
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from frame.core.frame_bean import FrameBean


class HttpClient:
    """
    HTTP客户端工具类，集成测试框架所需的核心功能

    特性：
    - 支持 GET/POST/PUT/DELETE/PATCH 方法
    - 自动会话管理
    - 可配置重试机制
    - 请求/响应日志跟踪
    - 文件上传/下载支持
    - 响应结果断言
    - 集成配置管理
    """

    def __init__(self, base_url:str):
        """
        初始化HTTP客户端
        :param config: 框架配置对象
        :param base_url: 基础API地址 (从配置自动读取)
        """
        # 设置默认请求头
        self.base_url = base_url
        self.default_headers = {
            "User-Agent": "FlutterTest/1.0",
            "Accept": "application/json"
        }
        # 初始化日志
        self.session = requests.Session()
        self.logger = FrameBean.get_service('logger')
        self.timeout = 10
        self.retry = 3

    def _log_request(self, method: str, url: str, **kwargs):
        """记录请求日志"""
        # method, url, params=params, data=data, json=json_data, headers=headers, response=response
        class Resp:
            text = '{}'
        self.logger.info({
            'url': url,
            'method': method.upper(),
            'params': json.dumps(kwargs.get('params', {})),
            'headers': json.dumps(kwargs.get('headers', {})),
            'request': json.dumps(kwargs.get('data', {})),
            'response': kwargs.get('response', Resp()).text
        }, suffer='request')

    def _request(
            self,
            method: str,
            endpoint: str,
            params: Optional[Dict] = None,
            data: Optional[Union[Dict, str]] = None,
            json_data: Optional[Dict] = None,
            headers: Optional[Dict] = None,
            files: Optional[Dict] = None
    ) -> requests.Response:
        """
        统一请求处理方法

        :param method: HTTP方法
        :param endpoint: API端点路径
        :param params: 查询参数
        :param data: 表单数据
        :param json_data: JSON数据
        :param headers: 请求头
        :param files: 上传文件
        :return: 响应对象
        """
        url = f"{self.base_url}{endpoint}"
        headers = {**self.default_headers, **(headers or {})}

        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                data=data,
                json=json_data,
                headers=headers,
                files=files,
                timeout=self.timeout,
                verify=True
            )
            self._log_request(method, url, params=params, data=data, json=json_data, headers=headers, response=response)
            return response

        except requests.RequestException as e:
            self.logger.info(f"Request failed: {str(e)}")
            raise

    def get(self, endpoint: str, params: Optional[Dict] = None, **kwargs) -> requests.Response:
        return self._request('GET', endpoint, params=params, **kwargs)

    def post(self, endpoint: str, data: Optional[Dict] = None, **kwargs) -> requests.Response:
        return self._request('POST', endpoint, data=data, **kwargs)

    def put(self, endpoint: str, data: Optional[Dict] = None, **kwargs) -> requests.Response:
        return self._request('PUT', endpoint, data=data, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        return self._request('DELETE', endpoint, **kwargs)

    def download_file(self, endpoint: str, save_path: Union[str, Path]) -> Tuple[bool, str]:
        """
        下载文件到本地

        :param endpoint: 文件下载端点
        :param save_path: 本地存储路径
        :return: (是否成功, 错误信息)
        """
        try:
            response = self.get(endpoint, stream=True)
            if response.status_code != 200:
                return False, f"下载失败，状态码：{response.status_code}"

            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            return True, ""

        except Exception as e:
            return False, f"下载异常：{str(e)}"

    def upload_file(self, endpoint: str, file_field: str, file_path: Union[str, Path], **kwargs) -> requests.Response:
        """
        上传文件
        :param endpoint: 上传端点
        :param file_field: 表单文件字段名
        :param file_path: 本地文件路径
        :return: 响应对象
        """
        try:
            with open(file_path, 'rb') as f:
                files = {file_field: (Path(file_path).name, f)}
                return self.post(endpoint, files=files, **kwargs)
        except FileNotFoundError:
            raise ValueError(f"文件不存在：{file_path}")


    def set_auth_token(self, auth_key: str, token: str):
        """设置认证Token"""
        self.default_headers[auth_key] = f"Bearer {token}"