from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import api

router = DefaultRouter()
router.register("", api.UserProfileAPI, basename="profile")
router.register("profile", api.UserProfileUpdateAPI, basename="update_profile")

account_routes = [path("", include(router.urls))]


# path(
#     "profile/update-status/",
#     api.UserProfileHasUpdatedProfileView.as_view(),
#     name="user-profile-update-status",
# ),
# path("update-profile/", api.update_user_profile, name="update_user_profile"),
# path(
#     "user-profile/update/",
#     api.UserProfileViewSet.as_view({"put": "update"}),
#     name="user-profile-update",
# ),
# path("search-user/", api.UserSearchAPIView.as_view(), name="search_user"),
# path("block/", api.block_user, name="block-user"),
# path("blocked-users/", api.list_blocked_users, name="list-blocked-users"),
# #     Stick urls
# path("stick/<int:user_id>/", api.stick_user, name="stick_user"),
# path("list-stickers/<int:user_id>/", api.list_stickers, name="list_stickers"),
# path("list-sticking/<int:user_id>/", api.list_sticking, name="list_sticking"),
# path("my-sticking/", api.my_sticking, name="my_sticking"),
# path("my-stickers/", api.my_stickers, name="my_stickers"),
# # CRSF token
# # path("get-csrf-token/", get_csrf_token, name="get-csrf-token"),
# #     Report Users urls
# path("report_user/", api.report_user, name="report_user"),
# path(
#     "reported_user_list/<int:user_id>/",
#     api.ReportUserViewSet.as_view(),
#     name="reported_user_list",
# ),
# #     Business Profile urls
# path(
#     "create-business-profile/",
#     api.create_business_profile,
#     name="create-business-profile",
# ),
# path(
#     "update-business-profile/<int:pk>/",
#     api.update_business_profile,
#     name="update-business-profile",
# ),
# path(
#     "business-availability/",
#     api.BusinessAvailabilityListCreateView.as_view(),
#     name="business-availability-list",
# ),
# path(
#     "business-availability/<int:pk>/",
#     api.BusinessAvailabilityDetailView.as_view(),
#     name="business-availability-detail",
# ),
# path(
#     "business-profile/",
#     api.BusinessAccountListCreateView.as_view(),
#     name="business-profile-list",
# ),
# path(
#     "business-profile/<int:pk>/",
#     api.BusinessAccountDetailView.as_view(),
#     name="business-profile-detail",
# ),
# path(
#     "business-category/",
#     api.BusinessCategoryListCreateView.as_view(),
#     name="business-category-list",
# ),
# path(
#     "business-category/<int:pk>/",
#     api.BusinessCategoryDetailView.as_view(),
#     name="business-category-detail",
# ),
# # Address Urls
# path("address/", api.AddressListCreateView.as_view(), name="address-list"),
# path("address/<int:pk>/", api.AddressDetailView.as_view(), name="address-detail"),
# path("get-notifications/", api.get_notifications, name="get-notification"),
# # Get conversations encryption keys
# path(
#     "get_encryption_keys/",
#     api.EncryptionKeyAPIView.as_view(),
#     name="get_encryption_keys",
# ),
# # Business authentication
# # path(
# #     "business/register/",
# #     api.BusinessAccountRegistrationView.as_view(),
# #     name="business_account_register",
# # ),
# path(
#     "business/login/",
#     api.BusinessAccountLoginView.as_view(),
#     name="business_account_login",
# ),
# path(
#     "business-accounts/",
#     api.ManagedBusinessAccountsView.as_view(),
#     name="managed_business_accounts",
# ),
# # path(
# #     "business/change-password/",
# #     api.BusinessAccountChangePasswordView.as_view(),
# #     name="business_change_password",
# # ),
# # path("flag-profile/", api.flag_user_profile, name="flag-user-profile"),
