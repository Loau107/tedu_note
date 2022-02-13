from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from note.models import Note
from user.models import User


# 校验登录状态装饰器
def check_login(func):
    def wrap(request, *args, **kwargs):
        if 'username' not in request.session or 'uid' not in request.session:
            username = request.COOKIES.get('username')
            uid = request.COOKIES.get('uid')
            if not username or not uid:
                script = 'alert("用户未登录")'
                return render(request, 'user/login.html', {'script': script})
            else:
                request.session['username'] = username
                request.session['uid'] = uid
        return func(request, *args, **kwargs)
    return wrap


# 检测 id 状态
def check_state(func):
    def wrap(request, *args, **kwargs):
        try:
            note_id = request.GET.get('id')
            note = Note.objects.get(id=note_id)
        except Exception as e:
            print(e)
            return HttpResponse('<h2 style="color: red">未索引到笔记</h2>')
        return func(request, note, *args, **kwargs)
    return wrap


@check_login
def list_note(request):
    uid = request.session.get('uid')
    user = User.objects.get(id=uid)
    all_note = Note.objects.filter(is_active=True, user_id=uid)
    l = len(all_note)
    return render(request, 'note/list_note.html', locals())


@check_login
def add_note(request):
    if request.method == 'GET':
        return render(request, 'note/add_note.html')
    elif request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        uid = request.session.get('uid')
        print(title,content,uid)
        Note.objects.create(title=title, content=content, user_id=uid)
        return HttpResponseRedirect('/note/list')


@check_state
@check_login
def update_note(request, note):
    if not note.is_active:
        return HttpResponse('<h2 style="color: red">未索引到笔记</h2>')
    if request.method == 'GET':
        return render(request, 'note/update_note.html', locals())
    elif request.method == 'POST':
        note.title = request.POST['title']
        note.content = request.POST['content']
        note.save()
        return HttpResponseRedirect('/note/list')


@check_state
@check_login
def delete_note(request, note):
    if not note.is_active:
        return HttpResponse('<h2 style="color: red">未索引到笔记</h2>')
    note.is_active = False
    note.save()
    return HttpResponseRedirect('/note/list/')


@check_login
def list_delete_note(request):
    uid = request.session.get('uid')
    user = User.objects.get(id=uid)
    all_delete_note = Note.objects.filter(is_active=False, user_id=uid)
    l = len(all_delete_note)
    return render(request, 'note/list_delete_note.html', locals())


@check_state
@check_login
def retrieve_note(request, note):
    note.is_active = True
    note.save()
    return HttpResponseRedirect('/note/list/')


@check_state
@check_login
def view_note(request, note):
    title = note.title
    content = note.content
    content = content.replace('\r\n', '<br/>')
    content = content.replace(' ', '&nbsp;')
    return render(request, 'note/view_note.html', locals())
