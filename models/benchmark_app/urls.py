"""benchmark_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from rest_framework import routers

import views

router = routers.DefaultRouter()
router.register(r'job', views.JobViewSet, base_name='job')
router.register(r'job_result', views.ViewJobResultModelViewSet, base_name='job_result')
router.register(r'models', views.BenchmarkModelViewSet, base_name='models')
router.register(r'frame', views.FrameViewSet, base_name='frame')
router.register(r'image', views.ImageViewSet, base_name='image')
# urlpatterns = [
#     url(r'^job/$', views.job_list),
#     url(r'job/<int>/$', views.job_detail),
# ]

urlpatterns = [
    url(r'', include(router.urls)),
]
