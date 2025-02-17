# 框架案例运行可视化工具
from frame.core.frame_bean import FrameBean

logger = FrameBean.get_service('logger')
class FrameVisualization:
    def create_visualization(self):
        pass

class FrameAllure:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        logger.info(f"Step started: {self.name}", suffer='step_start')
        # 这里可以添加更多逻辑，如记录日志、注入元数据等

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            logger.info(f"Step failed: {self.name}", suffer='step_end')
        else:
            logger.info(f"Step passed: {self.name}", suffer='step_end')
        # 这里可以添加更多逻辑，如记录日志、注入元数据等

frame = FrameVisualization()
frame.step = FrameAllure