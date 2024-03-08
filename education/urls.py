from django.urls import path

from . import api

app_name = "education"

urlpatterns = [
    path("redirect/jamb/", api.RedirectJambView.as_view(), name="jamb"),
    path("redirect/utme/", api.RedirectPostUtmeView.as_view(), name="utme"),
    path("redirect/waec/", api.RedirectWaecView.as_view(), name="waec"),
    path("redirect/neco/", api.RedirectNecoView.as_view(), name="neco"),
    path("redirect/nda/", api.RedirectNdaView.as_view(), name="nda"),
    path("redirect/nabteb/", api.RedirectNabTebView.as_view(), name="nabteb"),
    path("redirect/nimasa/", api.RedirectNimasaView.as_view(), name="nimasa"),
    path("redirect/trcn/", api.RedirectTrcnView.as_view(), name="trcn"),
]
