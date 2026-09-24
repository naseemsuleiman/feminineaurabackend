from django.contrib import admin
from .models import (
    UserProfile, BudgetSetup, DailyEntry,
    Article, DailyQuote, Subscriber, SiteStatus,
)


@admin.register(SiteStatus)
class SiteStatusAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_live', 'updated_at')

    def has_add_permission(self, request):
        return not SiteStatus.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at')
    search_fields = ('email',)
    ordering = ('-created_at',)


admin.site.register(UserProfile)
admin.site.register(BudgetSetup)
admin.site.register(DailyEntry)
admin.site.register(Article)
admin.site.register(DailyQuote)

admin.site.site_header = "Feminine Aura Admin"
admin.site.site_title = "Feminine Aura"
admin.site.index_title = "Site Management"