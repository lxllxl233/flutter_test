import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Union
from functools import wraps

from frame.core.frame_config import ConfigManager
from frame.core.frame_socket import send

# 日志颜色配置
COLORS = {
    'DEBUG': '\033[94m',  # 蓝色
    'INFO': '\033[92m',  # 绿色
    'WARNING': '\033[93m',  # 黄色
    'ERROR': '\033[91m',  # 红色
    'CRITICAL': '\033[95m',  # 品红
    'ENDC': '\033[0m'  # 结束颜色
}


class TestLogger:
    """测试框架日志组件"""

    def __init__(self,
                 name: str = "TestFramework",
                 log_level: str = "INFO",
                 log_dir: str = "logs",
                 enable_screenshot: bool = False):
        """
        初始化日志组件
        :param name: 日志名称
        :param log_level: 日志级别 (DEBUG/INFO/WARNING/ERROR/CRITICAL)
        :param log_dir: 日志存储目录
        :param enable_screenshot: 是否启用截图功能
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        self.log_dir = Path(log_dir)
        self.enable_screenshot = enable_screenshot
        self._driver = None  # 浏览器驱动（用于截图）

        # 创建日志目录
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # 初始化日志处理器
        self._init_handlers()

    def _init_handlers(self):
        """初始化日志处理器"""
        # 清除已有处理器
        self.logger.handlers.clear()

        # 控制台处理器（带颜色）
        console_handler = logging.StreamHandler(sys.stdout)
        console_formatter = ColoredFormatter(
            fmt='%(asctime)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        # 文件处理器（按日期存储）
        log_file = self.log_dir / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_formatter = logging.Formatter(
            fmt='[%(asctime)s] [%(levelname)s] [%(module)s:%(lineno)d] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

    def set_driver(self, driver):
        """设置浏览器驱动（用于截图）"""
        self._driver = driver

    def screenshot(self, name: str = None):
        """记录屏幕截图"""
        if self.enable_screenshot and self._driver:
            try:
                screenshot_dir = self.log_dir / "screenshots"
                screenshot_dir.mkdir(exist_ok=True)

                filename = f"{name or datetime.now().strftime('%H%M%S')}.png"
                path = screenshot_dir / filename
                self._driver.save_screenshot(str(path))
                self.logger.info(f"Screenshot saved: {path}")
                return path
            except Exception as e:
                self.logger.error(f"Failed to take screenshot: {str(e)}")

    def log_step(self, step: str):
        """记录测试步骤"""
        self.logger.info(f"🚀 STEP: {step}")

    def log_checkpoint(self, message: str):
        """记录检查点"""
        self.logger.info(f"✅ CHECKPOINT: {message}")

    def log_error(self, message: str, exc_info=True):
        """记录错误信息"""
        self.logger.error(message, exc_info=exc_info)
        self.screenshot("error_screenshot")

    # 快捷访问标准日志方法
    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, suffer=None, *args, **kwargs):
        if ConfigManager.get('IS_VIEW'):
            send({
                'message': msg,
                'suffer': suffer if suffer is not None else 'log'
            })
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)
        self.screenshot("error_screenshot")

    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)
        self.screenshot("critical_error")


class ColoredFormatter(logging.Formatter):
    """带颜色的日志格式化器"""

    def format(self, record):
        levelname = record.levelname
        message = super().format(record)
        return f"{COLORS[levelname]}{message}{COLORS['ENDC']}"


def log_exceptions(func):
    """异常日志装饰器"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = TestLogger(name="ExceptionLogger")
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.log_error(f"Exception occurred in {func.__name__}: {str(e)}")
            raise

    return wrapper