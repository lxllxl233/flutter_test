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

# 用例收集钩子
def pytest_collection_modifyitems(items):
    print(items)
    print(f"已收集 {len(items)} 个测试用例")

# 用例过滤完成钩子，这里是实际执行用例的地方
def pytest_collection_finish(session):
    # 获取所有用例信息
    selected = session.items
    print(f"已选中执行 {len(selected)} 个测试用例")
    print('初始化自定义组件')
    ######## 这里放置自己的组件 ########
    # 放置组件 : FrameBean.set_bean('组件名', 组件对象)
    # 获取组件 : FrameBean.get_service('组件名')
    print('初始化自定义组件完成')

# 用例执行完成钩子
def pytest_sessionfinish(session, exitstatus):
    if exitstatus == 0:
        print("✅ 所有测试通过")
    else:
        print("❌ 存在失败的用例")

