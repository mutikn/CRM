from django.contrib import admin
from .models import Client, Offer, ClientOffer, OfferImage, ClientComment, ClientOfferComment,DefaultContract
from django.utils.html import format_html
import random
import string


admin.site.site_header = "LifeDoc"
admin.site.site_title = "LifeDoc"
admin.site.index_title = "LifeDoc"

def generate_random_email(host_name):
    first_name = ''.join(random.choices(string.ascii_lowercase, k=5))
    last_name = ''.join(random.choices(string.ascii_lowercase, k=5))
    return f"{first_name}.{last_name}@mail.com"

@admin.action(description="Assign random email to offers without email")
def assign_random_email(modeladmin, request, queryset):
    for offer in queryset:
        if not offer.email: 
            offer.email = generate_random_email(offer.host_name)
            offer.save()
    modeladmin.message_user(request, "Random emails assigned successfully!")


class ClientOfferCommentInline(admin.TabularInline):
    model = ClientOfferComment
    extra = 1

class ClientCommentInline(admin.TabularInline):
    model = ClientComment
    extra = 1 

class OfferImageInline(admin.StackedInline):
    model = OfferImage
    extra = 1
    fields = ('image', 'preview')
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" style="object-fit: cover;"/>', obj.image.url)
        return "No Image"
    preview.short_description = "Preview"

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'nationality','passport_serial', 'passport_expiry_date','contract_file', 'active', 'created_at')
    search_fields = ('name', 'email', 'phone', 'passport_serial')
    list_filter = ('active', 'nationality', 'created_at')
    inlines = (ClientCommentInline,)


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('host_name', 'phone', 'email', 'price', 'active', 'offer_type', 'condition', 'main_image')
    search_fields = ('host_name', 'email', 'phone')
    list_filter = ('active', 'offer_type', 'condition')
    actions = [assign_random_email] 
    inlines = (OfferImageInline,)

    def main_image(self, obj):
        if obj.images.exists():
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;"/>', obj.images.first().image.url)
        return "No Image"
    main_image.short_description = "Main Image"

@admin.register(ClientOffer)
class ClientOfferAdmin(admin.ModelAdmin):
    list_display = ('client', 'offer', 'status', 'created_at')
    search_fields = ('client__name', 'offer__host_name')
    list_filter = ('status', 'created_at')
    inlines = (ClientOfferCommentInline,)

@admin.register(DefaultContract)
class DefaultContractAdmin(admin.ModelAdmin):
    list_display = ('name', 'file')
    search_fields = ('name',)