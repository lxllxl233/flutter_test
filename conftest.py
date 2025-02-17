# conftest.py
import json
import pytest
from frame.core.frame_bean import FrameBean
from frame.core.frame_log import TestLogger

logger: TestLogger = FrameBean.get_service('logger')

# 存储测试项信息的全局字典
items_by_nodeid = {}

@pytest.hookimpl
def pytest_itemcollected(item):
    """收集测试项时存储到全局字典"""
    items_by_nodeid[item.nodeid] = item

@pytest.hookimpl
def pytest_runtest_logstart(nodeid, location):
    """测试用例开始钩子"""
    item = items_by_nodeid.get(nodeid)
    if item:
        # 获取用例信息
        case_info = item.get_closest_marker('case_info')
        if case_info:
            info = {
                'nodeid': nodeid,
                'case_id': case_info.kwargs.get('case_id'),
                'case_name': case_info.kwargs.get('case_name'),
                'case_tags': case_info.kwargs.get('case_tags', []),
                'case_author': case_info.kwargs.get('case_author')
            }
            logger.info(info['case_name'], suffer='case_start')
        else:
            logger.info(nodeid, suffer='case_start')

@pytest.hookimpl
def pytest_runtest_logfinish(nodeid, location):
    """测试用例结束钩子"""
    item = items_by_nodeid.get(nodeid)
    if item:
        case_info = item.get_closest_marker('case_info')
        if case_info:
            info = {
                'nodeid': nodeid,
                'case_id': case_info.kwargs.get('case_id'),
                'case_name': case_info.kwargs.get('case_name')
            }
            logger.info(info['case_name'], suffer='case_end')
        else:
            logger.info(nodeid, suffer='case_end')