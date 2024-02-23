from django.urls import path, include
from . import views

urlpatterns = [
    path("redirect/jamb/", views.RedirectJambView.as_view(), name="jamb"),
    path("redirect/utme/", views.RedirectPostUtmeView.as_view(), name="utme"),
    path("redirect/waec/", views.RedirectWaecView.as_view(), name="waec"),
    path("redirect/neco/", views.RedirectNecoView.as_view(), name="neco"),
    path("redirect/nda/", views.RedirectNdaView.as_view(), name="nda"),
    path("redirect/nabteb/", views.RedirectNabTebView.as_view(), name="nabteb"),
    path("redirect/nimasa/", views.RedirectNimasaView.as_view(), name="nimasa"),
    path("redirect/trcn/", views.RedirectTrcnView.as_view(), name="trcn"),
]
