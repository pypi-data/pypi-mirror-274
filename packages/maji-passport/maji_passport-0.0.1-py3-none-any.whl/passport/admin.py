from django.contrib import admin

from argo.passport.models import PassportUser, AccessToken


@admin.register(PassportUser)
class PassportUserAdmin(admin.ModelAdmin):
    readonly_fields = ("argo_user",)
    search_fields = ("argo_user__email", "user_auth_code")


@admin.register(AccessToken)
class AccessTokenAdmin(admin.ModelAdmin):
    readonly_fields = ("token", "token_expiration", "passport_user")
