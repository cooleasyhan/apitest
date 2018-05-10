import builtins
import copy
import datetime
import json
import os
import signal
from multiprocessing import Manager, Process, current_process, managers
from subprocess import Popen, TimeoutExpired, call
from django.utils import timezone
import requests
from django.conf import settings
# Create your models here.
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import model_to_dict
from django.template import loader
from jinja2 import Template
from rest_framework.authtoken.models import Token

from apitest.dataformat import TCDataCell
from apitest.handler import BaseHandler
from apitest.logger import log_debug
from apitest.request import TestCaseRequest
from apitest.validator import Validator

from .comparator import comparators


class Project(models.Model):
    name = models.CharField(blank=False, max_length=100, verbose_name='项目名称')
    users = models.ManyToManyField(User)
    host = models.CharField(max_length=500, blank=True, null=True)
    min_wait = models.IntegerField(default=1000)
    max_wait = models.IntegerField(default=5000)

    _processes = dict()

    def __str__(self):
        return '-'.join([self.name if self.name else ''])

    def to_locustfile(self):
        context = {}
        context['base_dir'] = settings.BASE_DIR
        context['default_django_settings_module'] = settings.ROOT_URLCONF.split('.')[
            0] + '.settings'
        context['host'] = self.host
        context['min_wait'] = self.min_wait
        context['max_wait'] = self.max_wait
        context['project_name'] = self.name

        text = loader.render_to_string('locustfile.template', context)
        file_path = settings.LOCUST_FILE_ROOT
        file_name = 'locustfile__{pk}.py'.format(pk=self.pk)
        full_path = os.path.join(settings.BASE_DIR, file_path, file_name)
        with open(full_path, 'w') as f:
            f.write(text)
        return full_path

    def start_locust(self):
        def start(f, timeout, manager):

            call('locust --web-host=0.0.0.0 -f %s -P %s' %
                 (f, 9000 + self.pk), shell=True, timeout=60)

        if self.name in Project._processes.keys():
            p = Project._processes[self.name]

            if p.is_alive():
                return 9000 + self.pk

        f = self.to_locustfile()

        p = Process(target=start, args=(f, 300, Project._processes))
        p.daemon = True
        p.start()
        Project._processes[self.name] = p

        return 9000 + self.pk


class RestApiTestCase(models.Model):
    name = models.CharField(blank=False, max_length=100)
    project = models.ForeignKey(Project, on_delete=True)
    url = models.CharField(blank=False, max_length=2000)
    method = models.CharField(max_length=20,
                              choices=(('GET', 'GET'), ('POST', 'POST'), ('OPTION', 'OPTION')))
    data_type = models.CharField(max_length=200, choices=(
        ('DATA', 'DATA'), ('JSON', 'JSON')), default='JSON')

    response_data_type = models.CharField(max_length=200, choices=(
        ('DATA', 'DATA'), ('JSON', 'JSON')), default='JSON')
    last_run_time = models.DateTimeField(blank=True, null=True)
    # successed = models.BooleanField(default=False)
    last_run_result = models.TextField(blank=True, null=True)
    last_run_status_code = models.IntegerField(blank=True, null=True)

    def to_testapi_request(self, client=None):
        if hasattr(self, '_tc_request', ):
            return self._tc_request

        self._tc_request = TestCaseRequest(name=self.name, attr1=self.project.name, method=self.method, url=self.real_url,
                                           headers=self.headers, files=None, data=self.data, json=self.json, validators=self.validators, client=client)
        return self._tc_request

    @property
    def headers(self):
        tmp = []
        for header in HeaderField.objects.filter(tc=self):
            tmp.append(header.to_tc_cell())

        return tmp

    @property
    def headers_disp(self):
        return json.dumps(self.headers)

    @property
    def data(self):
        if self.data_type == 'DATA':
            tmp = []
            for field in DataField.objects.filter(tc=self):
                tmp.append(field.to_tc_cell())

            return tmp
        else:
            return None

    @property
    def json(self):
        if self.data_type == 'JSON':
            tmp = []
            for field in DataField.objects.filter(tc=self):
                tmp.append(field.to_tc_cell())

            return tmp
        else:
            return None

    @property
    def real_url(self):
        if not self.url.startswith('http'):
            return self.project.host + self.url
        else:
            return self.url

    # @property
    # def data_disp(self):
    #     return json.dumps(self.data)

    # def validate_disp(self):
    #     return [str(v) for v in Validate.objects.filter(tc=self)]

    @property
    def validators(self):

        return [v.to_validator() for v in Validate.objects.filter(tc=self)]

    # @property
    # def validate_result(self):
    #     tmp = []
    #     for v in Validate.objects.filter(tc=self):
    #         successed, value, expected_value, comparator = v.validate(
    #             self.result)

    def run_test(self):
        request = self.to_testapi_request()
        handler = BaseHandler()

        handler.load_middleware()
        # try:
        rst = handler.get_response(request)
        

        # self.successed = True if self.validate() else False
        self.last_run_status_code = rst.extract_field('status_code', raise_exception=False) or 500
        self.last_run_time = timezone.now()
        self.last_run_result = rst.resp_text
        log_debug('Validation Result: %s' % str(rst.validator_success))
        log_debug('Validation Result: %s' % str(rst.validators))
        self.save()

        return rst

    def run_locust(self, client):
        request = self.to_testapi_request(client=client)
        request.validators = []
        handler = BaseHandler()
        handler.load_middleware()
        rst = handler.get_response(request)

class Field(models.Model):
    tc = models.ForeignKey(RestApiTestCase, on_delete=True)
    name = models.CharField(max_length=200)
    data_type = models.CharField(max_length=20, choices=(
        ('int', 'int'), ('str', 'string'), ('boolean', 'boolean'), ('float', 'float'), ('jinja2', 'jinja2'), ('json','json')))
    value = models.CharField(max_length=2000, blank=True, null=True)

    def to_tc_cell(self):
        return TCDataCell(name=self.name, value=self.value, data_type=self.data_type)

    class Meta():
        abstract = True

class DataField(Field):
    pass

class HeaderField(Field):
    pass

class Validate(models.Model):
    tc = models.ForeignKey(RestApiTestCase, on_delete=True)
    field_name = models.CharField(max_length=200)
    comparator = models.CharField(
        max_length=50, choices=comparators)
    data_type = models.CharField(max_length=20, choices=(
        ('int', 'int'), ('str', 'string'), ('boolean', 'boolean'), ('float', 'float')))
    expected = models.CharField(max_length=2000)

    def __str__(self):
        return '%s %s %s' % (self.field_name, self.comparator, self.expected)

    def to_validator(self):
        return Validator(field=self.field_name, comparator=self.comparator, expect_value=self.expected, field_type=self.data_type)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
