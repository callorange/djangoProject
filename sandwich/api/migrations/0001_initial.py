# Generated by Django 3.2.13 on 2022-04-22 20:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bread',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='100자 이내. 중복 불가', max_length=100, unique=True, verbose_name='이름')),
                ('stock', models.PositiveIntegerField(default=0, help_text='재고수량', validators=[django.core.validators.MinValueValidator(0)], verbose_name='재고')),
                ('price', models.DecimalField(blank=True, decimal_places=2, default=0, help_text='가격. 0원 이상', max_digits=12, validators=[django.core.validators.MinValueValidator(0)], verbose_name='가격')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='등록일', verbose_name='등록일')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='수정일', verbose_name='수정일')),
            ],
            options={
                'verbose_name': '빵',
                'verbose_name_plural': '빵 리스트',
                'ordering': ['-id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Cheese',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='100자 이내. 중복 불가', max_length=100, unique=True, verbose_name='이름')),
                ('stock', models.PositiveIntegerField(default=0, help_text='재고수량', validators=[django.core.validators.MinValueValidator(0)], verbose_name='재고')),
                ('price', models.DecimalField(blank=True, decimal_places=2, default=0, help_text='가격. 0원 이상', max_digits=12, validators=[django.core.validators.MinValueValidator(0)], verbose_name='가격')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='등록일', verbose_name='등록일')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='수정일', verbose_name='수정일')),
            ],
            options={
                'verbose_name': '치즈',
                'verbose_name_plural': '치즈 리스트',
                'ordering': ['-id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Sauce',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='100자 이내. 중복 불가', max_length=100, unique=True, verbose_name='이름')),
                ('stock', models.PositiveIntegerField(default=0, help_text='재고수량', validators=[django.core.validators.MinValueValidator(0)], verbose_name='재고')),
                ('price', models.DecimalField(blank=True, decimal_places=2, default=0, help_text='가격. 0원 이상', max_digits=12, validators=[django.core.validators.MinValueValidator(0)], verbose_name='가격')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='등록일', verbose_name='등록일')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='수정일', verbose_name='수정일')),
            ],
            options={
                'verbose_name': '소스',
                'verbose_name_plural': '소스 리스트',
                'ordering': ['-id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Topping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='100자 이내. 중복 불가', max_length=100, unique=True, verbose_name='이름')),
                ('stock', models.PositiveIntegerField(default=0, help_text='재고수량', validators=[django.core.validators.MinValueValidator(0)], verbose_name='재고')),
                ('price', models.DecimalField(blank=True, decimal_places=2, default=0, help_text='가격. 0원 이상', max_digits=12, validators=[django.core.validators.MinValueValidator(0)], verbose_name='가격')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='등록일', verbose_name='등록일')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='수정일', verbose_name='수정일')),
            ],
            options={
                'verbose_name': '토핑',
                'verbose_name_plural': '토핑 리스트',
                'ordering': ['-id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Sandwich',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='100자 이내. 중복 불가', max_length=100, unique=True, verbose_name='이름')),
                ('price', models.DecimalField(blank=True, decimal_places=2, default=0, help_text='가격. 0원 이상', max_digits=12, validators=[django.core.validators.MinValueValidator(0)], verbose_name='가격')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='등록일', verbose_name='등록일')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='수정일', verbose_name='수정일')),
                ('bread', models.ManyToManyField(to='api.Bread', verbose_name='빵')),
                ('cheese', models.ManyToManyField(to='api.Cheese', verbose_name='치즈')),
                ('sauce', models.ManyToManyField(to='api.Sauce', verbose_name='소스')),
                ('topping', models.ManyToManyField(to='api.Topping', verbose_name='토핑')),
            ],
            options={
                'verbose_name': '샌드위치',
                'verbose_name_plural': '샌드위치 리스트',
                'ordering': ['-id'],
            },
        ),
    ]
