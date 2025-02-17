import os

# PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
# PROJECT_NAME = 'simple_project'
# LOG_DIR = os.path.join(PROJECT_NAME, 'case_log')
# REPORT_DIR = os.path.join(PROJECT_NAME, 'report')

CONFIG_DICT = {
    'PROJECT_ROOT' : os.path.dirname(os.path.abspath(__file__)),
    'PROJECT_NAME' : 'simple_project',
    'TEST_BED' : None,
    # 是否可视化运行
    'IS_VIEW': True,
    'REMOTE_URL': 'http://localhost:8080'
}
CONFIG_DICT['LOG_DIR'] = os.path.join(CONFIG_DICT['PROJECT_NAME'], 'case_log')
CONFIG_DICT['REPORT_DIR'] = os.path.join(CONFIG_DICT['PROJECT_NAME'], 'report')
