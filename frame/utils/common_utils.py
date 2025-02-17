import time
import functools
import pytest
import allure

from frame.core.frame_bean import FrameBean


# 重试
def retry(func):
    """
    函数重试装饰器
    - 默认不启用重试，需通过参数动态启用
    - 触发条件：异常抛出 或 返回值不满足表达式
    - 使用参数：
        r_retry_count: 重试次数（必须 >0 才生效）
        r_wait_time: 每次重试等待时间（秒）
        r_expr: 返回值校验表达式（lambda函数）
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 提取重试参数并从kwargs中移除，避免传递给原函数
        retry_count = kwargs.pop('r_retry_count', 0)
        wait_time = kwargs.pop('r_wait_time', 0)
        expr = kwargs.pop('r_expr', None)

        # 不满足重试触发条件时直接执行
        if retry_count <= 0:
            return func(*args, **kwargs)

        last_exception = None
        for attempt in range(retry_count + 1):  # 总尝试次数 = 重试次数 + 1
            try:
                result = func(*args, **kwargs)

                # 检查返回值是否满足表达式条件
                if expr is not None and not expr(result):
                    raise ValueError(
                        f"Return value {result} does not satisfy condition"
                    )

                return result  # 执行成功且满足条件

            except Exception as e:
                last_exception = e
                if attempt < retry_count:
                    time.sleep(wait_time)
                else:
                    raise last_exception  # 重试耗尽后抛出异常

        # 理论上不会执行到此处
        return None

    return wrapper

# 用例装饰器
def frame_case(case_id=None, case_name=None, case_tags=None, case_author=None):
    """
    用例信息装饰器
    :param case_id: 用例唯一标识
    :param case_name: 用例名称
    :param case_tags: 用例标签列表
    :param case_author: 用例作者
    """
    def decorator(func):
        # 添加 pytest marker 存储用例信息
        func = pytest.mark.case_info(
            case_id=case_id,
            case_name=case_name,
            case_tags=case_tags or [],
            case_author=case_author
        )(func)

        # 添加 allure 注解
        if case_name:
            func = allure.story(case_name)(func)
            func = allure.title(case_name)(func)
        if case_tags:
            func = allure.tag(*case_tags)(func)
        if case_author:
            func = allure.description(f"Author: {case_author}")(func)

        return func
    return decorator

class AssertUtil:
    @classmethod
    def assert_equal(cls, expr, success_msg, fail_msg):
        logger = FrameBean.get_service('logger')
        try:
            if expr:
                logger.info(success_msg)
            else:
                logger.info(fail_msg)
        except Exception as e:
            logger.info(f'异常为{e}, 失败信息{fail_msg}')
        assert expr, fail_msg