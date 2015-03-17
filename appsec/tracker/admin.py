from django.contrib import admin
from tracker.models import Organization, DataElement
from tracker.models import Tag, Application, Environment, EnvironmentLocation, EnvironmentCredentials, Person, Relation, Engagement, Activity, EngagementComment, ActivityComment, ApplicationFileUpload
from tracker.models import ActivityType
from tracker.models import ThreadFix
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
    fields = ['application', 'person', 'owner', 'notes']
    extra = 0


class EngagementInline(admin.StackedInline):
    model = Engagement
    fieldsets = [
        (None, {'fields': ['application', 'start_date', 'end_date']}),
        ('Advanced options', {
            'classes': ['collapse'],
            'fields': ['status', 'open_date', 'close_date']
        }),
    ]
    extra = 0


class ActivityInline(admin.StackedInline):
    model = Activity
    fieldsets = [
        (None, {'fields': ['activity_type', 'users']}),
        ('Advanced options', {
            'classes': ['collapse'],
            'fields': ['status', 'open_date', 'close_date']
        }),
    ]
    extra = 0


class EngagementCommentInline(admin.StackedInline):
    model = EngagementComment
    extra = 0


class ActivityCommentInline(admin.StackedInline):
    model = ActivityComment
    extra = 0


class ApplicationFileUploadInline(admin.StackedInline):
    model = ApplicationFileUpload
    extra = 0


class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'color']
    search_fields = ['^name']

admin.site.register(Tag, TagAdmin)


admin.site.register(Organization)


class DataElementAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'weight']
    list_filter = ['category']
    search_fields = ['^name']

admin.site.register(DataElement, DataElementAdmin)

class ApplicationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['organization', 'name', 'description']}),
        ('Metadata', {
            'classes': ['collapse'],
            'fields': ['platform', 'lifecycle', 'origin', 'business_criticality', 'approximate_users', 'approximate_revenue', 'external_audience', 'internet_accessible']
        }),
        ('Tags', {
            'classes': ['collapse'],
            'fields': ['tags']
        }),
        ('Data Classification', {
            'classes': ['collapse'],
            'fields': ['data_elements']
        }),
        ('ThreadFix', {
            'classes': ['collapse'],
            'fields': ['threadfix', 'threadfix_organization_id', 'threadfix_application_id']
        }),
    ]
    list_display = ['name', 'platform', 'lifecycle', 'origin', 'business_criticality', 'external_audience', 'internet_accessible', 'data_elements_list', 'data_sensitivity_value', 'data_classification_level']
    list_filter = ('external_audience', 'internet_accessible')
    inlines = [EnvironmentInline, RelationInline, EngagementInline, ApplicationFileUploadInline]
    search_fields = ['^name']

    def data_elements_list(self, obj):
        return ", ".join([data_element.name for data_element in obj.data_elements.all()])

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


class EngagementAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['application', 'start_date', 'end_date']}),
        ('Advanced options', {
            'classes': ['collapse'],
            'fields': ['status', 'open_date', 'close_date']
        }),
    ]
    list_display = ['__str__', 'start_date', 'end_date', 'status', 'application']
    inlines = [ActivityInline, EngagementCommentInline]

admin.site.register(Engagement, EngagementAdmin)


admin.site.register(ActivityType)


class ActivityAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['engagement', 'activity_type', 'users']}),
        ('Advanced options', {
            'classes': ['collapse'],
            'fields': ['status', 'open_date', 'close_date']
        }),
    ]
    list_display = ['__str__', 'status', 'activity_type']
    inlines = [ActivityCommentInline]

admin.site.register(Activity, ActivityAdmin)

admin.site.register(ThreadFix)
