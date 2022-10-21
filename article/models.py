from tkinter import CASCADE
from unittest.util import _MAX_LENGTH
from django.db import models

class User(models.Model):
  email = models.CharField(max_length=50)
  pwd = models.CharField(max_length=100)
  name = models.CharField(max_length=10)

class Article(models.Model):
  title = models.CharField(max_length=100)
  content = models.CharField(max_length=1000)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

class Reply(models.Model):
  content = models.CharField(max_length=1000)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  article = models.ForeignKey(Article, on_delete=models.CASCADE)
  #migrate, migration 해야 함!

class File(models.Model):
  o_filename = models.CharField(max_length=1000)  #o : original
  s_filename = models.CharField(max_length=1000)  #s : save
  filesize = models.IntegerField(default=0) #장고에서 숫자 쓸 땐, default=0, null=True 지정 

#     Fileattach
class FileAtch(models.Model):
  o_filename = models.CharField(max_length=1000)  #o : original
  s_filename = models.CharField(max_length=1000)  #s : save
  filesize = models.IntegerField(default=0) #장고에서 숫자 쓸 땐, default=0, null=True 지정
  article = models.ForeignKey(Article, on_delete=models.CASCADE)
  #파일 여러개 첨부할거면 새로 테이블 만들어야해!