# Generated by Django 3.0.3 on 2020-02-06 13:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Planet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название планеты')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст вопроса')),
                ('right_answer', models.BooleanField(verbose_name='Правильный ответ')),
            ],
        ),
        migrations.CreateModel(
            name='Sith',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя ситха')),
                ('planet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sith.Planet', verbose_name='Планета на которой обучает')),
            ],
        ),
        migrations.CreateModel(
            name='Recruit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('age', models.SmallIntegerField(verbose_name='Возраст')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('planet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sith.Planet', verbose_name='Планета обитания')),
                ('sith', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sith.Sith')),
            ],
        ),
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='sith.Planet')),
                ('question', models.ManyToManyField(to='sith.Question')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.BooleanField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sith.Question')),
                ('recruit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sith.Recruit')),
            ],
            options={
                'unique_together': {('recruit', 'question')},
            },
        ),
    ]
