import time

from frame.core.frame_bean import FrameBean
from frame.core.frame_visualization import frame
from frame.utils.common_utils import frame_case, AssertUtil

logger = FrameBean.get_service('logger')
class TestFrame:
    wait_time = 1
    def setup(self):
        pass
    @frame_case(
        case_id=["TC001"],
        case_name="用例 1",
        case_tags=["标签1", "标签2"],
        case_author="long"
    )
    def test_logger_1(self):
        with frame.step('1步骤 1'):
            time.sleep(TestFrame.wait_time)
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
            AssertUtil.assert_equal(expr=((1 / 0)==0), success_msg='验证成功', fail_msg='验证失败')
        with frame.step('1步骤 3'):
            time.sleep(TestFrame.wait_time)
            logger.info('1test3333333333333')


    @frame_case(
        case_id=["TC002"],
        case_name="用例 2",
        case_tags=["标签2", "标签2"],
        case_author="long"
    )
    def test_logger_2(self):
        with frame.step('2步骤 1'):
            time.sleep(TestFrame.wait_time)
            logger.info('2test1111111111111111111111')
            AssertUtil.assert_equal(expr=(1 ==2), success_msg='验证成功', fail_msg='验证失败')
        with frame.step('2步骤 2'):
            time.sleep(TestFrame.wait_time)
            logger.info('2test2222222222222222222222')
        with frame.step('2步骤 3'):
            time.sleep(TestFrame.wait_time)
            logger.info('2test3333333333333')