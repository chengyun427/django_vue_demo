from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
import json

# 解决前端post请求 csrf问题
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def testapi(request):
    print(request)
    print(request.method)
    if request.method == "GET":
        print(request.GET.get('aa'))
        resp = {'errorcode': 100, 'type': 'Get', 'data': {'main': request.GET.get('aa')}}
        return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        print(request.POST)
        print(request.body)
        str1 = str(request.body, encoding="utf-8")
        data = eval(str1)
        print(data)
        print(data['aa'])
        print(type(request.body))
        resp = {'errorcode': 100, 'type': 'Post', 'data': {'main': data['aa']}}
        return HttpResponse(json.dumps(resp), content_type="application/json")


# 前端查询左侧菜单
@csrf_exempt
def listUserMenus (request):
    print(request)
    resp = {
        'code': 0,
        'msg': '',
        'data': [
            {
                'id': '01',
                'label': '首页',
                'index': '/home',
                'attributes': [],
                'icon': 'iconfont el-icon-alishouye',
                'children': []
            },
            {
                'id': '02',
                'label': '房价预测',
                'index': '/account',
                'attributes': [],
                'icon': 'iconfont el-icon-alisujuyuce',
                'children': []
            },
            {
                'id': '03',
                'label': '情感分析',
                'index': '/goods',
                'attributes': [],
                'icon': 'iconfont el-icon-aliqinggan',
                'children': []
            },

        ]
    }
    return HttpResponse(json.dumps(resp), content_type="application/json")


# 登录
@csrf_exempt
def getUserByLogin (request):
    print(request)
    resp = {
        'code': 0,
        'msg': '',
        'data': [
            {
                'userUuid': '',
                'userAccount': 'admin',
                'userName': 'admin',
                'userIdNumber': '',
                'userTel': '',
                'userGender': '',
                'userIsUsed': '',
                'userEmail': '',
                'userComments': '',
                'version': '',
            }
        ]
    }
    return HttpResponse(json.dumps(resp), content_type="application/json")