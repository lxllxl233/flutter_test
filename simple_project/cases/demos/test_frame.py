import time

import pytest

from frame.core.frame_bean import FrameBean
from frame.core.frame_visualization import frame
from frame.utils.common_utils import frame_case, AssertUtil
from frame.utils.http_utils import HttpClient

logger = FrameBean.get_service('logger')
class TestFrame:
    wait_time = 1
    already_do = False

    def setup_method(self):
        if not self.__class__.already_do:
            print('前置')
            self.frame_request = HttpClient(base_url='https://tags.growingio.com')
            self.__class__.already_do = True

    @frame_case(
        case_id=["TC001"],
        case_name="用例 1",
        case_tags=["TC001", "标签1", "标签2"],
        case_author="long"
    )
    def test_logger_1(self):
        with frame.step('1步骤 1'):
            time.sleep(TestFrame.wait_time)
            self.frame_request.get('/products/c196c3667d214851b11233f5c17f99d5/web/www.nowcoder.com/settings/general', params={
                'id' : 'OBFB.1E928B2B86E3D4E8ED1D46B83E667303',
                'pid' : 'Fb','qlt' :99,'r' :0
            })
            logger.info('1test1111111111111111111111')
            time.sleep(TestFrame.wait_time)
            logger.info('1test1111111111111111111111')
            time.sleep(TestFrame.wait_time)
            logger.info('1test1111111111111111111111')
            time.sleep(TestFrame.wait_time)
            logger.info('1test1111111111111111111111')
            AssertUtil.assert_equal(expr=(1 == 1 ), success_msg='验证成功', fail_msg='验证失败')
        with frame.step('1步骤 2'):
            time.sleep(TestFrame.wait_time)
            logger.info('1test2222222222222222222222')
        with frame.step('1步骤 3'):
            time.sleep(TestFrame.wait_time)
            logger.info('1test3333333333333')


    @frame_case(
        case_id=["TC002"],
        case_name="用例 2",
        case_tags=["TC002", "标签2", "标签2"],
        case_author="long"
    )
    def test_logger_2(self):
        with frame.step('2步骤 1'):
            time.sleep(TestFrame.wait_time)
            logger.info('2test1111111111111111111111')
        with frame.step('2步骤 2'):
            time.sleep(TestFrame.wait_time)
            logger.info('2test2222222222222222222222')
        with frame.step('2步骤 3'):
            time.sleep(TestFrame.wait_time)
            logger.info('2test3333333333333')