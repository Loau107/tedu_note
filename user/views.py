from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from user.models import User
import hashlib


def reg_view(request):
    if request.method == 'GET':
        return render(request, 'user/register.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password_t = request.POST['password_t']
        old_users = User.objects.filter(username=username)
        # 未完全输入 注册失败 返回提示
        if username == '' or password  == '' or password_t == '':
            script = 'alert("用户名或密码未输入")'
            return render(request, 'user/register.html', locals())
        # 用户已存在 注册失败 返回提示
        elif old_users:
            script = 'alert("用户名已注册")'
            return render(request, 'user/register.html', locals())
        # 密码不一致 注册失败 返回提示
        elif password != password_t:
            script = 'alert("两次输入的密码不一致")'
            return render(request, 'user/register.html', locals())
        # 否则 正常注册 跳转登录界面
        else:
            m = hashlib.md5()
            # 哈希转换
            m.update(password.encode())
            try:
                user = User.objects.create(username=username, password=m.hexdigest())
            except Exception as e:
                print(e)
                # 多线程同时插入相同用户名时 插入错误
                script = 'alert("用户名已注册")'
                return render(request, 'user/register.html', locals())
            # 返回 session 数据  设置免登录
            request.session['username'] = username
            request.session['uid'] = user.id
            # 跳转主页
            return HttpResponseRedirect('/index/')


def log_view(request):

    if request.method == 'GET':
        # 判断是否存在 session 记录
        if request.session.get('username') and request.session.get('uid'):
            return HttpResponseRedirect('/index/')
        username = request.COOKIES.get('username')
        uid = request.COOKIES.get('uid')
        # 判断是否存在 cookies 记录
        if username and uid:
            # 重添加 session
            request.session['username'] = username
            request.session['uid'] = uid
            return HttpResponseRedirect('/index/')
        # 无记录获取登录页面
        return render(request, 'user/login.html')

    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # 判断是否完全输入
        if username == '' or password == '':
            script = 'alert("用户名或密码未输入")'
            return render(request, 'user/login.html', locals())
        # 判断是否存在用户
        try:
            m = hashlib.md5()
            m.update(password.encode())
            user = User.objects.get(username=username)
        except Exception as e:
            print(e)
            script = 'alert("用户名或密码错误")'
            return render(request, 'user/login.html', locals())
        else:
            # 判断密码是否正确
            if user.password != m.hexdigest():
                script = 'alert("用户名或密码错误")'
                return render(request, 'user/login.html', locals())
            else:
                request.session['username'] = username
                request.session['uid'] = user.id
                resp = HttpResponseRedirect('/index/')
                # 判断是否记住密码
                if 'remember' in request.POST:
                    resp.set_cookie('username', user.username, 3600*24*3)
                    resp.set_cookie('uid', user.id, 3600*24*3)
                return resp


def logout_view(request):
    resp = HttpResponseRedirect('/index/')
    # 删除 session 数据
    if 'username' in request.session:
        del request.session['username']
    if 'uid' in request.session:
        del request.session['uid']
    # 删除 cookie 数据
    if 'username' in request.COOKIES:
        resp.delete_cookie('username')
    if 'uid' in request.COOKIES:
        resp.delete_cookie('uid')
    return resp
