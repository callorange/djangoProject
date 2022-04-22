"""
샌드위치 API 뷰 패키지
"""
from django.shortcuts import render

from .bread import *
from .topping import *
from .cheese import *
from .sauce import *
from .sandwich import *


def error_404(request, exception):
    return render(request, "api/404.html", {})
