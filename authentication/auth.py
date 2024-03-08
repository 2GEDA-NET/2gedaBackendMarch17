from rest_framework.authentication import TokenAuthentication as BaseTokenAuthentication


class TokenAuthentication(BaseTokenAuthentication):
    """Token Authentication"""

    keyword = "Bearer"
