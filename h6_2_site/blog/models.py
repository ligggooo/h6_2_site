from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.



class UserInfo(AbstractUser):
    nid = models.AutoField(primary_key=True)
    telephone = models.CharField(max_length=11, null=True, unique=True)
    avatar = models.FileField(upload_to='avatars/', default="avatars/default.png")
    # 1 https://docs.djangoproject.com/en/2.1/ref/models/fields/#filefield
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    # 2
    blog = models.OneToOneField(to='Blog', to_field='nid', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.username


class Blog(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64, verbose_name='blog title')
    #
    site_style = models.OneToOneField(to='BlogStyle', to_field='nid', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return '%s 的 %s'%(self.userinfo.username, self.title)


class BlogStyle(models.Model):
    #     定制博客风格 （皮肤）包括背景图在内的一系列参数打包
    nid = models.AutoField(primary_key=True)
    detail = models.CharField(max_length=255, verbose_name='博客皮肤')

    def __str__(self):
        return self.detail


class Category(models.Model):
    # 与Blog多多对一的关系，博主私人定制
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='分类标题', max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid', on_delete=models.CASCADE)

    def __str__(self):
        return '%s 的 %s分类'%(self.blog.userinfo.username, self.title)


class Tag(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='标签名称', max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid', on_delete=models.CASCADE)

    def __str__(self):
        return '%s 的 %s标签' % (self.blog.userinfo.username, self.title)


class Article(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=40, verbose_name='文章标题')
    desc = models.CharField(max_length=255, verbose_name='文章描述')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    content = models.TextField()
    # 3,

    comment_count = models.IntegerField(default=0)
    up_count = models.IntegerField(default=0)
    down_count = models.IntegerField(default=0)

    #     关联
    user = models.ForeignKey(to='UserInfo', to_field='nid', on_delete=models.CASCADE)
    category = models.ForeignKey(to='Category', to_field='nid',
                                 # limit_choices_to=models.Q(blog_id=user.blog_id),   # 不起作用
                                 # limit_choices_to=models.Q(blog_id=1),  # 起作用
                                 null=True, on_delete=models.CASCADE)
    # allowed to be null
    # 多多关系 通过自定义表格完成 这么做的目的是提高可控性吗？ 也可以让orm自动生成
    tags = models.ManyToManyField(to=Tag, through='Article2Tag', through_fields=('article_id', 'tag_id'))

    def __str__(self):
        return  self.title+' : '+self.user.username


class Article2Tag(models.Model):
    nid = models.AutoField(primary_key=True)
    article_id = models.ForeignKey(verbose_name='文章', to="Article", to_field='nid', on_delete=models.CASCADE)
    tag_id = models.ForeignKey(verbose_name='标签', to="Tag", to_field='nid', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.article_id) + ' --> ' + str(self.tag_id)


class ArticleUpDown(models.Model):
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(to='UserInfo', to_field='nid', null=True, on_delete=models.CASCADE)  # null 是true? 还没有ondelete?
    article = models.ForeignKey(to='Article', to_field='nid', null=True, on_delete=models.CASCADE)
    is_up = models.BooleanField(default=True)

    def __str__(self):
        return str(self.user) + ' --> ' + str(self.article)


class Comment(models.Model):
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(to='UserInfo', to_field='nid', null=True, on_delete=models.CASCADE)  # null 是true? 还没有ondelete?
    article = models.ForeignKey(to='Article', to_field='nid', null=True, on_delete=models.CASCADE)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    content = models.CharField(verbose_name='评论内容', max_length=255)

    parent_comment = models.ForeignKey(to='self', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)+ ' --> ' + str(self.article)
