from rest_framework.authentication import TokenAuthentication as tk

class TokenAuthentication(tk):
    keyword = 'Bearer'