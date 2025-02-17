class FrameBean:
    bean_map = {}
    @classmethod
    def set_bean(cls, service_name, service):
        FrameBean.bean_map[service_name] = service

    @classmethod
    def get_service(cls, service_name):
        return FrameBean.bean_map[service_name]