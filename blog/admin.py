from django.contrib import admin

from .models import MicroViewEntry, OptionsStudyEntry, Post


class ResearchEntryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "status", "created_on")
    list_filter = ("status",)
    search_fields = ["title", "content"]
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Post, ResearchEntryAdmin)
admin.site.register(MicroViewEntry, ResearchEntryAdmin)
admin.site.register(OptionsStudyEntry, ResearchEntryAdmin)
