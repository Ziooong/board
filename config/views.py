from msilib.schema import File
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
import hashlib
from article.models import User

#AJAX 가입가능 이메일인지 확인
def check(request):
  email = request.GET.get('email')
  try:
    User.objects.get(email=email)
  except:
    return HttpResponse("가입 가능")
  return HttpResponse("가입 불가")

def index(request):
  #비밀번호 암호화
  m = hashlib.sha256()   #hash알고리즘
  m.update(b"1")
  print( m.hexdigest() )

  return render(request, 'index.html')

from django.http import HttpResponseRedirect

def signup(request):
  if request.method == 'POST':
    # 회원정보 저장
    email = request.POST.get('email')
    name = request.POST.get('name')

    pwd = request.POST.get('pwd')
    m = hashlib.sha256()   #hash알고리즘
    m.update(bytes(pwd, 'utf-8'))
    pwd =  m.hexdigest()

    user = User(email=email, name=name, pwd=pwd)
    user.save()
    return HttpResponseRedirect('/index/')

  return render(request, 'signup.html')

def signin(request):
  if request.method == 'POST':
    # 회원정보 조회
    email = request.POST.get('email')
    pwd = request.POST.get('pwd')
    m = hashlib.sha256()   #hash알고리즘
    m.update(bytes(pwd, 'utf-8'))
    pwd = m.hexdigest()
    
    try:
      # select * from user where email=? and pwd=?
      user = User.objects.get(email=email, pwd=pwd)
      request.session['email'] = email   #session값은 이메일에 대한 정보를 기억.
      request.session['name'] = user.name
      return render(request, 'signin_success.html')
    except:
      return render(request, 'signin_fail.html')

  return render(request, 'signin.html')

def signout(request):
  del request.session['email']  # 개별 삭제
  request.session.flush()  # 전체 삭제

  return HttpResponseRedirect('/index/')

from article.models import Article
from article.models import Reply, User, File, FileAtch

import os, time
def upload(request):
  if request.method == 'POST':
    file = request.FILES.getlist('abc') #여러개 받을땐 list
    for f in file:
      name = f.name
      size = f.size
      save_name = name

      if os.path.isfile('c:/django/%s' % name):
        #중복파일이 존재하므로 파일명 변경하기
        #ex) abc.jpg -> abc_123124234.jpg
        n = name[ 0 : name.find('.')]
        ext = name[ name.find('.') : ] #extention
        save_name = '%s_%s%s' % (n, time.time(), ext)  #time.time() 유닉스타임 사용.

      #업로드된 파일 저장
      u_file = open('c:/django/%s' % save_name, 'wb')
      for chunk in file[0].chunks():
        u_file.write(chunk)
      u_file.close()

      File(s_filename=save_name, o_filename=name, filesize=size).save()

    #이거 쓰셈.
    file2 = request.FILES.getlist('xyz')
    for f in file2:
      print(f.name, f.size)
    #고객들에게 출력(보여줄 것)
    return HttpResponse(
      '%s %s' % (name,size))

  return render(request, 'upload.html', {})

def download(request): #http//127.0.0.1:8000/download/?id=1
  id = request.GET.get('id')
  # article = Article.objects.get(id=id)
  file_atch = FileAtch.objects.get(id=id)

  filename = file_atch.s_filename

  file = open('c:/django/%s' % filename, 'rb')
  res = HttpResponse(
    file,
    content_type='application/octet-stream')
    # content_type='image/jpg')
  res['Content-Disposition'] = 'attachment; filename=%s' % filename
  return res

def write(request):
  if request.method == 'POST':
    title = request.POST.get('title')
    content = request.POST.get('content')
    
    try:
      email = request.session['email']
      # select * from user where email = ?
      user = User.objects.get(email=email)
      # insert into article (title, content, user_id) values (?, ?, ?)
      article = Article(title=title, content=content, user=user)
      article.save()

      #파일 업로드 위치
      file = request.FILES.getlist('file') #여러개 받을땐 list
      for f in file:
        name = f.name
        size = f.size
        save_name = name
        print(size)

        if os.path.isfile('c:/django/%s' % name):
          #중복파일이 존재하므로 파일명 변경하기
          #ex) abc.jpg -> abc_123124234.jpg
          n = name[ 0 : name.find('.')]
          ext = name[ name.find('.') : ] #extention
          save_name = '%s_%s%s' % (n, time.time(), ext)  #time.time() 유닉스타임 사용.

        #업로드된 파일 저장
        u_file = open('c:/django/%s' % save_name, 'wb')
        for chunk in f.chunks():
          u_file.write(chunk)
        u_file.close()

        FileAtch(s_filename=save_name, o_filename=name, filesize=size, article=article).save()

      return render(request, 'write_success.html')
    except:
      return render(request, 'write_fail.html')

  return render(request, 'write.html')

from django.core.paginator import Paginator

def list(request):
  page = request.GET.get('page')  # url에 list/?page=1
  
  # select * from article order by id desc
  article_list = Article.objects.order_by('-id')

  p = Paginator(article_list, 10)
  try:
    page = int(page)    #숫자를 문자로 바꿔줘야 함. 그리고 왜 이 자리에 넣어야 하는가?
    article_list = p.page(page)  # ?page=문자열 오류 없애는 방법
  except:
    page = 1
    article_list = p.page(page)

  #리스트>넘버링
  # print('-'*20)
  # print(article_list.start_index())
  # s = article_list.count() - article_list.start_index() + 1
  # e = s - 


#Pagenation 
# ex) 7page -> 1 / 183 -> 181
# 10?? -> 11이기 때문에 (page - 1)을 함.
  start_page = (page - 1) // 10 * 10 + 1  #pagenation 중 시작 페이지
  end_page = start_page + 9  #pagenation 중 마지막 페이지

  #전체 페이지 수가 end_page 보다 적다면
  if p.num_pages < end_page:
    end_page = p.num_pages

  context = { 
    'article_list' : article_list,
    'page_info' : range(start_page, end_page + 1)
  }
  return render(request, 'list.html', context)

def detail(request, id):
  # select * from article where id = ?
  article = Article.objects.get(id=id)
  context = { 
    'article' : article 
  }

  return render(request, 'detail.html', context)

def update(request, id):
  # select * from article where id = ?  
  article = Article.objects.get(id=id)

  #로그인한 사용자의 정보 확인
  name = request.session.get('name')
  #작성자명 확인
  if article.user.name != name: #같지 않다.
    # return HttpResponse('''
    #     <script>
    #       alert("작성자만 수정할 수 있습니다.");
    #       location = "/article/detail/%s/";
    #     </script>
    #   ''' % id)
    return render(request, 'update_fail.html', {'id':id})

  if request.method == 'POST':
    title = request.POST.get('title')
    content = request.POST.get('content')
    
    try:
      # update article set title = ?, content = ? where id = ?
      article.title = title
      article.content = content
      article.save()
      return render(request, 'update_success.html')
    except:
      return render(request, 'update_fail.html')

  context = { 
    'article' : article 
  }
  return render(request, 'update.html', context)

def delete(request, id):
  try:
    # select * from article where id = ?
    name = request.session['name']  #이름은 절대 안됨. 동명이인은?
    article = Article.objects.get(id=id)

    if article.user.name == name:
      article.delete()
    else:
      #delete_fail.html에 써 주는 것이 더 좋음
      return HttpResponse('''
        <script>
          alert("작성자만 삭제할 수 있습니다.");
          location = "/article/detail/%s/";
        </script>
      ''' % id)
      
    return render(request, 'delete_success.html')
  except:
    return render(request, 'delete_fail.html')

def reply(request, id):
  email = request.session.get('email')
  user = User.objects.get(email=email)
  article = Article.objects.get(id=id)
  content = request.GET.get('content')

  reply = Reply(content=content, user=user, article=article)
  reply.save()

  return redirect('/article/detail/%s/' % id)


def map(request):
  return render(request, 'map.html')

from django.http import JsonResponse  # JSON 응답
from map.models import Point
from django.forms.models import model_to_dict

def map_data2(request):
  lat = request.GET.get('lat')
  lng = request.GET.get('lng')

  data = Point.objects.raw('''
    SELECT *,
       (6371 * acos(
         cos(radians(%s))
         * cos(radians(lat))
         * cos(radians(lng) - radians(%s))
         + sin(radians(%s))
         * sin(radians(lat)))) AS distance
     FROM map_point
    HAVING distance <= %s
    ORDER BY distance''' % (lat, lng, lat, 10))
  map_list = []
  for d in data:
    d = model_to_dict(d)  # QuerySet -> Dict
    map_list.append(d)
  # dict가 아닌 자료는 항상 safe=False 옵션 사용
  return JsonResponse(map_list, safe=False)

def map_data(request):
  data = Point.objects.all()
  lat = request.GET.get('lat')
  lng = request.GET.get('lng')
  map_list = []
  for d in data:
    d = model_to_dict(d)  # QuerySet -> Dict
    dist = distance(float(lat), float(lng), d['lat'], d['lng'])
    if(dist <= 100):  # 100km 이내의 장소만 응답결과로 저장
      map_list.append(d)
  # dict가 아닌 자료는 항상 safe=False 옵션 사용
  return JsonResponse(map_list, safe=False)

import math
def distance(lat1, lng1, lat2, lng2)  :
  theta = lng1 - lng2
  dist1 = math.sin(deg2rad(lat1)) * math.sin(deg2rad(lat2))

  dist2 = math.cos(deg2rad(lat1)) * math.cos(deg2rad(lat2)) 
  dist2 = dist2* math.cos(deg2rad(theta))

  dist = dist1 + dist2

  dist = math.acos(dist)
  dist = rad2deg(dist) * 60 * 1.1515 * 1.609344

  return dist

def deg2rad(deg):
  return deg * math.pi / 180.0

def rad2deg(rad):
  return rad * 180.0 / math.pi

def contact(request):
  if request.method == 'POST':
    email = request.POST.get('email')
    comment = request.POST.get('comment')
    #         발신자주소, 수신자주소, 메시지
    send_mail('ggoreb.kim@gmail.com', email, comment)
    return render(request, 'contact_success.html')

  return render(request, 'contact.html')

import smtplib
from email.mime.text import MIMEText
 
def send_mail(from_email, to_email, msg):
  # SMTP 설정
  smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
  # 인증정보 설정
  smtp.login(from_email, 'hwojjkbwhtxxmxdg')
  msg = MIMEText(msg)
  # 제목
  msg['Subject'] = '[문의사항]' + to_email
  # 수신 이메일
  msg['To'] = from_email
  smtp.sendmail(from_email, from_email, msg.as_string())
  smtp.quit()
