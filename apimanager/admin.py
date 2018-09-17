import time
from collections import Counter

from django.contrib import admin
from django.http import response
from django.shortcuts import render_to_response
from rest_framework.authtoken.admin import TokenAdmin

from .models import *
from .services import run_test

TokenAdmin.raw_id_fields = ('user',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('pk', '__str__', 'host')
    list_filter = ()
    search_fields = ()

    actions = ['start_locust']

    def start_locust(self, request, queryset):
        for obj in queryset:
            n = obj.start_locust()
        time.sleep(0.5)
        return response.HttpResponseRedirect(redirect_to='http://%s:%s/' % (request.META['HTTP_HOST'].split(':')[0], n))


class DataFieldAdmin(admin.TabularInline):
    suit_classes = 'suit-tab suit-tab-data'
    model = DataField


class HeaderFieldAdmin(admin.TabularInline):
    suit_classes = 'suit-tab suit-tab-header'
    model = HeaderField


class ValidateAdmin(admin.TabularInline):
    suit_classes = 'suit-tab suit-tab-validate'
    model = Validate


@admin.register(RestApiTestCase)
class RestApiTestCaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'real_url',
                    # 'data_disp', 'validate_disp',
                    #  'successed',
                    # 'last_run_result'
                    )
    actions_on_top = True
    list_filter = ('project',)
    search_fields = ()
    inlines = [DataFieldAdmin, HeaderFieldAdmin, ValidateAdmin]

    suit_form_tabs = (('general', '主数据'), ('data', '数据'),
                      ('header', '头部'), ('validate', '校验'))

    actions = ['run', 'copy']

    def get_fieldsets(self, request, obj=None):
        return [(None, {'classes': ('suit-tab suit-tab-general',), 'fields': self.get_fields(request, obj)})]

    def run(self, request, queryset):
        rst = run_test(queryset)
        return render_to_response('test_report.html', rst)

    def copy(self, request, queryset):
        for origin in queryset:
            new_one = RestApiTestCase.objects.get(pk=origin.pk)
            new_one.pk = None
            new_one.name = origin.name + '_copy'
            new_one.save()

            for df in DataField.objects.filter(tc=origin):
                df.pk = None
                df.tc = new_one
                df.save()

            for df in HeaderField.objects.filter(tc=origin):
                df.pk = None
                df.tc = new_one
                df.save()

            for df in Validate.objects.filter(tc=origin):
                df.pk = None
                df.tc = new_one
                df.save()
