from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, ListView
from django.http import HttpResponseRedirect
from django.db.models import Q

from .forms import SignUpForm
from .models import User, Character

class Welcome(TemplateView):
    template_name = 'AKTool/welcome.html'

def signin(request):
    if request.method == "GET":
        return render(request, 'AKTool/login.html')
    user = None
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return render(request, 'AKTool/login_success.html')
    else:
        return render(request, 'AKTool/login.html', {'error_message': 'login failed.'})

class Signout(LogoutView):
    template_name = 'AKTool/welcome.html'

class SignUp(CreateView):
    form_class = SignUpForm
    template_name = 'AKTool/create.html'
    success_url = reverse_lazy('AKTool:create_success')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.object = user
        return HttpResponseRedirect(self.get_success_url())

def create_account(request):
    return render(request, 'AKTool/create_success.html')

def home(request, username):
    user = User.objects.get(username=username)
    if request.method == "POST":    #登録削除
        number = int(request.POST.get('number'))
        if user.character_name_1 == number:
            user.character_name_1 = 0
        if user.character_name_2 == number:
            user.character_name_2 = 0
        if user.character_name_3 == number:
            user.character_name_3 = 0
        if user.character_name_4 == number:
            user.character_name_4 = 0
        if user.character_name_5 == number:
            user.character_name_5 = 0
        user.save()
    character_list = []

    #登録キャラリスト制作
    if user.character_name_1 != 0:
        character = get_object_or_404(Character, pk=user.character_name_1)
        character_list.append(character)
    if user.character_name_2 != 0:
        character = get_object_or_404(Character, pk=user.character_name_2)
        character_list.append(character)
    if user.character_name_3 != 0:
        character = get_object_or_404(Character, pk=user.character_name_3)
        character_list.append(character)
    if user.character_name_4 != 0:
        character = get_object_or_404(Character, pk=user.character_name_4)
        character_list.append(character)
    if user.character_name_5 != 0:
        character = get_object_or_404(Character, pk=user.character_name_5)
        character_list.append(character)
    context = {'character_list': character_list}
    return render(request, 'AKTool/index.html', context)

def charaSelect(request, username):
    user = User.objects.get(username=username)
    keyword = request.GET.get('keyword')
    character_list = Character.objects.order_by('character_rare')

    # 登録キャラリストアップ
    select_list = []
    if user.character_name_1 != 0:
        select_list.append(user.character_name_1)
    if user.character_name_2 != 0:
        select_list.append(user.character_name_2)
    if user.character_name_3 != 0:
        select_list.append(user.character_name_3)
    if user.character_name_4 != 0:
        select_list.append(user.character_name_4)
    if user.character_name_5 != 0:
        select_list.append(user.character_name_5)

    #　名前検索部分
    if keyword:
        character_list = character_list.filter(Q(character_name__icontains=keyword))
        messages.success(request, '「{}」の検索結果'.format(keyword))
    context = {'character_list': character_list,
               'select_list': select_list}
    return render(request, 'AKTool/charaSelect.html', context)

def charaDetail(request, username, chara_id):
    if request.method == "POST":
        user = User.objects.get(username=username)
        character = get_object_or_404(Character, pk=chara_id)
        message_ok = "登録しました"
        message_already = "登録済みです"
        if user.character_name_1 == 0:
            user.character_name_1 = character.id
            user.save()
            context = {'character': character,
                       'message': message_ok}
            return render(request, 'AKTool/charaDetail.html', context)
        elif user.character_name_1 == character.id:
            context = {'character': character,
                       'message': message_already}
            return render(request, 'AKTool/charaDetail.html', context)
        if user.character_name_2 == 0:
            user.character_name_2 = character.id
            user.save()
            context = {'character': character,
                       'message': message_ok}
            return render(request, 'AKTool/charaDetail.html', context)
        elif user.character_name_2 == character.id:
            context = {'character': character,
                       'message': message_already}
            return render(request, 'AKTool/charaDetail.html', context)
        if user.character_name_3 == 0:
            user.character_name_3 = character.id
            user.save()
            context = {'character': character,
                       'message': message_ok}
            return render(request, 'AKTool/charaDetail.html', context)
        elif user.character_name_3 == character.id:
            context = {'character': character,
                       'message': message_already}
            return render(request, 'AKTool/charaDetail.html', context)
        if user.character_name_4 == 0:
            user.character_name_4 = character.id
            user.save()
            context = {'character': character,
                       'message': message_ok}
            return render(request, 'AKTool/charaDetail.html', context)
        elif user.character_name_4 == character.id:
            context = {'character': character,
                       'message': message_already}
            return render(request, 'AKTool/charaDetail.html', context)
        if user.character_name_5 == 0:
            user.character_name_5 = character.id
            user.save()
            context = {'character': character,
                       'message': message_ok}
            return render(request, 'AKTool/charaDetail.html', context)
        elif user.character_name_5 == character.id:
            context = {'character': character,
                       'message': message_already}
            return render(request, 'AKTool/charaDetail.html', context)

        message = "登録最大数を超えています。他の登録を削除してください。"
        context = {'character': character,
                   'message': message}
        return render(request, 'AKTool/charaDetail.html', context)

    if request.method == "GET":
        character = get_object_or_404(Character, pk=chara_id)
        message = ""
        context = {'character': character,
                   'message': message}
        return render(request, 'AKTool/charaDetail.html', context)

def tagSelect(request,username):
    user = User.objects.get(username=username)

    # 登録キャラリストアップ
    select_list = []
    if user.character_name_1 != 0:
        select_list.append(user.character_name_1)
    if user.character_name_2 != 0:
        select_list.append(user.character_name_2)
    if user.character_name_3 != 0:
        select_list.append(user.character_name_3)
    if user.character_name_4 != 0:
        select_list.append(user.character_name_4)
    if user.character_name_5 != 0:
        select_list.append(user.character_name_5)

    if request.method == "GET":
        context = {'character_list': [],
                   'select_list': select_list,
                   'tag_list': [],
                   }
        return render(request, 'AKTool/tagSelect.html', context)

    if request.method == "POST":
        character_list = Character.objects.order_by('character_rare')
        tag_list = request.POST.getlist("tag")
        c_l_l = {}
        # キャラクターごとにtag_listのタグを持つか確認し、すべての確認を終えたら辞書配列に追加
        for c in character_list:
            t = ""
            for tag in tag_list:
                if tag in c.tags:
                    if t == "":
                        t = tag
                    else:
                        t = t + " + " + tag
            if t == "":
                continue
            if t in c_l_l:
                c_l_l[t].append(c)
            else:
                c_l_l[t] = [c]
        print(c_l_l)

        context = {'character_list': c_l_l,
                   'select_list': select_list,
                   'tag_list': tag_list,
                   }
        return render(request, 'AKTool/tagSelect.html', context)
# Create your views here.
