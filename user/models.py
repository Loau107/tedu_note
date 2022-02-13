from django.db import models


# Create your models here.
class User(models.Model):

    username = models.CharField('用户名', max_length=30)
    password = models.CharField('密码', max_length=32)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    is_active = models.BooleanField('状态', default=True)

    def __str__(self):
        return 'username %s' % (self.username)

    class Meta:
        db_table = 'user'