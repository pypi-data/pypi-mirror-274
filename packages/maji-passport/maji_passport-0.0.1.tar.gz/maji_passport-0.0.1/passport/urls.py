from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from argo.passport.views.exchange import (
    ExchangeTokenViewSet,
    ServiceToken,
    UpdateUserInfo,
)
from argo.passport.views.passport import (
    UserPassportViewSet,
    PassportViewSet,
    ExpiredPassportViewSet,
)

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register(
    "passport", UserPassportViewSet, basename="user_merge_passport_password"
)
router.register("passport", PassportViewSet, basename="passport")

# deprecated. We don't use refresh token with Passport v2
# router.register("passport", ExpiredPassportViewSet, basename="passport-auth")

router.register("external", ExchangeTokenViewSet, basename="exchange_token")
router.register("external", ServiceToken, basename="service_token")
router.register("external/update_user", UpdateUserInfo, basename="update_user_info")

urlpatterns = router.urls
