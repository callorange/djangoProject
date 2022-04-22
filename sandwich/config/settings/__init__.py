"""
차후 동작 환경별 설정 분리가 있을경우를 대비해 seetings를 세분화 해놓음
django 동작시 --settings 관련 옵션 혹은 DJANGO_SETTINGS_MODULE이 지정되지 않은경우 developement로 동작한다
"""

import os

SETTING_MODULE = os.environ.get("DJANGO_SETTINGS_MODULE")
if not SETTING_MODULE or SETTING_MODULE == 'config.settings':
    from .developement import *
