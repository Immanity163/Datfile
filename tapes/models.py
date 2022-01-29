from django.db import models


class Creator(models.Model):
    name = models.CharField(max_length=255 ,verbose_name="ник")
    is_active = models.BooleanField(default=True ,verbose_name= "активный")
    inban = models.BooleanField(default=False , verbose_name="в бане")
    data = models.TimeField(auto_now_add=True , verbose_name= "дата создания")

    def __str__(self):
        return self.name

class post(models.Model):
    user = models.ForeignKey(Creator, on_delete = models.CASCADE,verbose_name = 'Создатель')
    title = models.CharField(max_length=255,verbose_name ='Заголовок')
    text = models.TextField(verbose_name="текст поста")
    data = models.DateField(auto_now_add=True,verbose_name ='Дата')
    image = models.ImageField(upload_to = 'images',default = 'NONE',verbose_name ='Картинка1')

    Type_choices = (
        ('Общество','Общество'),
        ('Политика','Политика'),
        ('Наука','Наука'),
        ('Экономика','Экономика'),
        ('','')
    )

    type_ch = models.CharField(max_length = 10,choices = Type_choices,default = '',verbose_name ='Тип новости')
    
    def __str__(self):
        return self.title

class comment(models.Model):
    post = models.ForeignKey(post,on_delete= models.CASCADE,verbose_name="родительский пост")
    nickname = models.CharField(max_length=255,verbose_name="ник пользователя")
    date = models.DateField(auto_now_add=True,verbose_name="дата создания")
    text = models.TextField(verbose_name="текст комментария")

    def __str__(self):
        return f'{self.post}|||{self.nickname}|||{self.date}'