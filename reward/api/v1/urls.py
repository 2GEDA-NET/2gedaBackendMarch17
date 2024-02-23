from django.urls import path

from .views import (
    Claim_Reward,
    Claims_Record,
    Get_All_Rewards,
    Get_Rewards,
    Reward_User,
)

urlpatterns = [
    path("user/", Reward_User.as_view()),
    path("get", Get_Rewards.as_view()),
    path("get-all/", Get_All_Rewards.as_view()),
    path("claim/", Claim_Reward.as_view()),
    path("claim/history/", Claims_Record.as_view()),
]
