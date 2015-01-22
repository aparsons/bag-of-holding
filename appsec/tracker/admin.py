from django.contrib import admin
from tracker.models import Tag, Application, Environment, EnvironmentLocation, EnvironmentCredentials, Person, Relation

# Register your models here.

class EnvironmentCredentials(admin.StackedInline):
    model = EnvironmentCredentials
    extra = 0


class EnvironmentInline(admin.StackedInline):
    model = Environment
    extra = 0


class EnvironmentLocationInline(admin.StackedInline):
    model = EnvironmentLocation
    extra = 0


class RelationInline(admin.StackedInline):
    model = Relation
    fields = ['application', 'person', 'role', 'owner', 'notes']
    extra = 0


class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'color']
    search_fields = ['^name']

admin.site.register(Tag, TagAdmin)


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['name', 'business_criticality', 'platform', 'origin', 'industry', 'external_audience', 'internet_accessible']
    list_filter = ('external_audience', 'internet_accessible')
    inlines = [EnvironmentInline, RelationInline]
    search_fields = ['^name']

admin.site.register(Application, ApplicationAdmin)


class EnvironmentAdmin(admin.ModelAdmin):
    fields = ['application', 'environment_type', 'description', 'testing_approved']
    list_display = ['__str__', 'environment_type', 'application', 'testing_approved']
    inlines = [EnvironmentLocationInline, EnvironmentCredentials]

admin.site.register(Environment, EnvironmentAdmin)


class PersonAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'email', 'phone_work', 'phone_mobile']
    search_fields = ['^first_name', '^last_name', '^email']
    inlines = [RelationInline]

admin.site.register(Person, PersonAdmin)
