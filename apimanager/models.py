import builtins
import copy
import datetime
import json

import requests
# Create your models here.
from django.contrib.auth.models import User
from django.db import models
from django.forms import model_to_dict
from jinja2 import Template

from .func import g


class Project(models.Model):
    name = models.CharField(blank=False, max_length=100, verbose_name='项目名称')
    users = models.ManyToManyField(User)
    # available_minions = models.ManyToManyField(Minion)
    # available_resps = models.ManyToManyField(Repository)

    # @property
    # def users_str(self):
    #     return ', '.join(['[%s]' % str(i) for i in self.users.all()])

    def __str__(self):
        return '-'.join([self.name if self.name else ''])


class RestApiTestCase(models.Model):
    name = models.CharField(blank=False, max_length=100)
    project = models.ForeignKey(Project, on_delete=True)
    url = models.URLField(blank=False, max_length=2000)
    method = models.CharField(max_length=20,
                              choices=(('GET', 'GET'), ('POST', 'POST'), ('OPTION', 'OPTION')))
    data_type = models.CharField(max_length=200, choices=(('DATA','DATA'),('JSON','JSON')), default='JSON')
    last_run_time = models.DateTimeField(blank=True, null=True)
    successed = models.BooleanField(default=False)
    last_run_result = models.TextField(blank=True, null=True)
    last_run_status_code = models.IntegerField(blank=True, null=True)

    @property
    def headers(self):
        tmp = {}
        for header in HeaderField.objects.filter(tc=self):
            tmp[header.name] = tmp[header.value]

        return tmp

    @property
    def headers_disp(self):
        return json.dumps(self.headers)

    @property
    def data(self):
        tmp = {}
        fields = DataField.objects.filter(tc=self)
        for f in fields:
            if f.data_type != 'jinja2': 
                _func = getattr(builtins, f.data_type)
                tmp[f.name] = _func(f.value)

        for f in fields:
            if f.data_type == 'jinja2':
                template = Template(f.value)
                context = copy.copy(g)
                context.update(tmp)
                tmp[f.name] = template.render(context)

        return tmp

    @property
    def data_disp(self):
        return json.dumps(self.data)

    def validate_disp(self):
        return [str(v) for v in Validate.objects.filter(tc=self)]

    def validate(self):
        for v in Validate.objects.filter(tc=self):
            if not v.validate(self.result):
                return False

        return True

    def run_test(self):
        if self.data_type == 'JSON':
            rst = requests.request(
                url=self.url, method=self.method, json=self.data)
        else:
            rst = requests.request(
                url=self.url, method=self.method, data=self.data)

        self.result = rst.json()

        self.last_run_status_code = rst.status_code
        self.last_run_result = rst.text

        self.successed = True if self.validate() else False

        self.last_run_time = datetime.datetime.now()
        self.save()

    def run_lucust(self, client):
        if self.data_type == 'JSON':
            rst = client.request(
                url=self.url, method=self.method, json=self.data)
        else:
            rst = client.request(
                url=self.url, method=self.method, data=self.data)


class DataField(models.Model):
    tc = models.ForeignKey(RestApiTestCase, on_delete=True)
    name = models.CharField(max_length=200)
    data_type = models.CharField(max_length=20, choices=(
        ('int', 'int'), ('str', 'string'), ('boolean', 'boolean'), ('float', 'float'), ('jinja2','jinja2')))
    value = models.CharField(max_length=2000, blank=True, null=True)



class HeaderField(models.Model):
    tc = models.ForeignKey(RestApiTestCase, on_delete=True)
    name = models.CharField(max_length=200)
    value = models.CharField(max_length=2000, blank=True, null=True)


class Validate(models.Model):
    tc = models.ForeignKey(RestApiTestCase, on_delete=True)
    field_name = models.CharField(max_length=200)
    comparator = models.CharField(
        max_length=20, choices=(('eq', 'eq'), ('exists', 'exists')))
    data_type = models.CharField(max_length=20, choices=(
        ('int', 'int'), ('str', 'string'), ('boolean', 'boolean'), ('float', 'float')))
    expected = models.CharField(max_length=2000)

    def __str__(self):
        return '%s %s %s' % (self.field_name, self.comparator, self.expected)

    def validate(self, data):
        try:
            value=data
            for field in self.field_name.split('/'):
                value=data[field]
            if self.comparator == 'exists':
                return True

        except KeyError:
            if self.comparator == 'not_exists':
                return True
            raise

        func=getattr(builtins, self.data_type)
        value=func(value)
        expected_value=func(self.expected)
        if self.comparator == 'eq':

            if value == expected_value:
                return True
            else:
                print(value, expected_value)

        return False
