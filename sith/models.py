from django.db import models


class Planet(models.Model):
    title = models.CharField('Название планеты', max_length=100)

    def __str__(self):
        return self.title


class SithManager(models.Manager):

    def get_queryset(self):
        return super(SithManager, self).get_queryset().annotate(recruits_cnt=models.Count('recruit'))

    def can_teach(self):
        return self.get_queryset().filter(recruits_cnt__lte=2)

    def more_than_one(self):
        return self.get_queryset().filter(recruits_cnt__gt=1)


class Sith(models.Model):
    name = models.CharField('Имя ситха', max_length=100)
    planet = models.ForeignKey(Planet, verbose_name='Планета на которой обучает', on_delete=models.CASCADE)
    objects = models.Manager()
    with_recruits = SithManager()

    def __str__(self):
        return self.name


class RecruitManager(models.Manager):
    def get_queryset(self):
        return super(RecruitManager, self).get_queryset().filter(sith=None)


class Recruit(models.Model):
    name = models.CharField('Имя', max_length=100)
    planet = models.ForeignKey(Planet, verbose_name='Планета обитания', on_delete=models.CASCADE)
    age = models.SmallIntegerField('Возраст')
    email = models.EmailField('Email')
    sith = models.ForeignKey(Sith, null=True, on_delete=models.CASCADE)
    objects = RecruitManager()

    def __str__(self):
        return f'{self.name} с планеты "{self.planet}"'


class Question(models.Model):
    text = models.TextField('Текст вопроса')
    right_answer = models.BooleanField('Правильный ответ')

    def __str__(self):
        return f'{self.text[:10]}...'


class Answer(models.Model):
    recruit = models.ForeignKey(Recruit, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.BooleanField()

    class Meta:
        unique_together = (('recruit', 'question'),)


class Challenge(models.Model):
    order = models.OneToOneField(Planet, on_delete=models.CASCADE)
    question = models.ManyToManyField(Question)

    def __str__(self):
        return f'Испытаение ордена {self.order}'
