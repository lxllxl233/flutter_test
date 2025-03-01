import argparse
import json
import os
import sys
from datetime import datetime

import pytest
from typing import List, Optional

from frame.core.frame_bean import FrameBean
from frame.core.frame_config import ConfigManager
from frame.core.frame_log import TestLogger


class FrameApplication:
    """
    测试框架主应用程序，负责启动测试框架并运行测试任务。
    """

    def __init__(self):
        # 初始化配置
        config_manager = ConfigManager
        config_manager.init_class()
        self.config_manager = config_manager
        self.base_dir = config_manager.get('PROJECT_ROOT')
        self.report_dir = config_manager.get('REPORT_DIR')
        self.log_dir = config_manager.get('LOG_DIR')
        # 初始化日志
        logger = TestLogger(
            log_level="DEBUG",
            log_dir=self.log_dir,
            enable_screenshot=True
        )
        # 初始化目录
        self._init_directories()
        FrameBean.set_bean('logger', logger)

    def _init_directories(self):
        """
        初始化必要的目录（报告目录和日志目录）。
        """
        print(self.report_dir)
        os.makedirs(self.report_dir, exist_ok=True)
        os.makedirs(self.log_dir, exist_ok=True)

    def run(self):
        try:
            task = self.config_manager.get('TASK', None)
            case_ids = []
            if task is not None:
                task_file_path = os.path.join(os.path.join(self.config_manager.get('PROJECT_NAME'), 'task'), task+'.json')
                print('任务文件路径 : ', task_file_path)
                case_ids = json.load(open(task_file_path))['case_ids']
                print(case_ids)
            pytest_args = self._build_pytest_args(case_ids)

            # 运行测试
            print(pytest_args)
            exit_code = self._run_tests(pytest_args)
            print('用例执行完成，退出码 ：', exit_code)
            # 判断是否生成allure报告
            print(self.config_manager.get('AUTO_CREATE_ALLURE_REPORT'))
            if self.config_manager.get('AUTO_CREATE_ALLURE_REPORT'):
                print('开始生成测试报告')
                os.system(f'allure generate {self.allure_dir} -o {self.allure_report_dir} --clean')
        except Exception as e:
            print(f"❌ 框架启动失败: {str(e)}")
            sys.exit(1)

    def _load_task(self, task_file: str) -> List[str]:
        """
        加载任务文件，提取用例ID列表。

        :param task_file: 任务文件路径。
        :return: 用例ID列表。
        :raises FileNotFoundError: 如果任务文件不存在。
        :raises ValueError: 如果任务文件中没有有效的用例ID。
        """
        # 检查任务文件是否存在
        if not os.path.exists(task_file):
            raise FileNotFoundError(f"任务文件不存在: {task_file}")

        # 读取任务文件并提取用例ID
        with open(task_file, "r", encoding="utf-8") as f:
            test_ids = [line.strip() for line in f if line.strip()]

        # 检查是否提取到有效的用例ID
        if not test_ids:
            raise ValueError("任务文件中未找到有效的用例ID")

        print(f"📄 已加载任务文件: {task_file}")
        return test_ids

    def _build_pytest_args(self, test_ids: Optional[List[str]] = None) -> List[str]:
        """
        构建 pytest 执行参数。

        :param test_ids: 用例ID列表（可选）。
        :return: pytest 参数列表。
        """
        args = self._parse_args()
        print(args)
        current_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        self.allure_dir = os.path.join(self.config_manager.get('REPORT_DIR'), current_time)
        self.allure_report_dir = os.path.join(self.allure_dir, 'report')
        print('当前allure输出位置 : ', self.allure_dir)
        os.makedirs(self.allure_dir, exist_ok=True)
        os.makedirs(self.allure_report_dir, exist_ok=True)
        pytest_args = [
            "-s",  # 详细输出
            "--capture=no",  # 禁用输出捕获
            "--alluredir=" + self.allure_dir,
            "-m=" + ' or '.join(test_ids),
            "-W ignore::pytest.PytestUnknownMarkWarning",
            "-W ignore::pytest.PytestConfigWarning"
        ]
        return pytest_args

    def _run_tests(self, pytest_args: List[str]):
        """
        使用 pytest 运行测试。

        :param pytest_args: pytest 参数列表。
        """
        print("🚀 启动测试框架...")
        print(pytest_args)
        exit_code = pytest.main(pytest_args)

        # 输出结果
        if exit_code == 0:
            print("✅ 所有测试通过！")
        else:
            print(f"❌ 测试失败，退出码: {exit_code}")

        return exit_code

    def _parse_args(self) -> argparse.Namespace:
        """
        解析控制台参数。

        :return: 包含解析后参数的命名空间对象。
        """
        parser = argparse.ArgumentParser(description="测试框架启动程序")

        # 添加控制台参数
        parser.add_argument(
            "-m", "--mark",
            dest="markexpr",
            help="仅运行指定标记的用例 (如: smoke, regression)"
        )
        parser.add_argument(
            "-k", "--keyword",
            dest="keywordexpr",
            help="仅运行名称匹配关键字的用例"
        )
        parser.add_argument(
            "--html",
            action="store_true",
            help="生成HTML测试报告"
        )
        parser.add_argument(
            "--allure",
            action="store_true",
            help="生成Allure报告"
        )
        parser.add_argument(
            "-v", "--verbose",
            action="count",
            default=0,
            help="增加日志详细程度 (-v: INFO, -vv: DEBUG)"
        )

        return parser.parse_args()
