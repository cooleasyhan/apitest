from django.contrib import admin
from .models import *
from django.http import response 
import time

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('pk','__str__',)
    list_filter = ()
    search_fields = ()

    actions = ['start_locust']
    def start_locust(self, request, queryset):
        for obj in queryset:
            n = obj.start_locust()
        time.sleep(0.5)
        return response.HttpResponseRedirect(redirect_to='http://%s:%s/' % (request.META['HTTP_HOST'].split(':')[0] ,n))

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
    list_display = ('project', 'real_url', 'headers_disp',
                    'data_disp', 'validate_disp', 'successed', 'last_run_result')
    list_filter = ()
    search_fields = ()
    inlines = [DataFieldAdmin, HeaderFieldAdmin, ValidateAdmin]

    suit_form_tabs = (('general', '主数据'), ('data', '数据'),
                      ('header', '头部'), ('validate', '校验'))

    actions = ['run']

    def get_fieldsets(self, request, obj=None):
        return [(None, {'classes': ('suit-tab suit-tab-general',), 'fields': self.get_fields(request, obj)})]

    def run(self, request, queryset):
        for obj in queryset:
            obj.run_test()
