from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication



class RedirectJambView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        external_url = 'https://www.jamb.gov.ng/'
        return Response({'redirect_to': external_url})
    

class RedirectPostUtmeView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        external_url = 'https://www.myschoolgist.com/ng/post-utme-updates/'
        return Response({'redirect_to': external_url})
    

class RedirectWaecView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        external_url = 'https://www.waecnigeria.org/'
        return Response({'redirect_to': external_url})
    


class RedirectNecoView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        external_url = 'https://neco.gov.ng/'
        return Response({'redirect_to': external_url})



class RedirectNdaView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        external_url = 'https://nda.edu.ng/'
        return Response({'redirect_to': external_url})


class RedirectNabTebView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        external_url = 'https://nabteb.gov.ng/'
        return Response({'redirect_to': external_url})



class RedirectNimasaView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        external_url = 'https://nimasa.gov.ng/'
        return Response({'redirect_to': external_url})



class RedirectTrcnView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        external_url = 'https://trcn.gov.ng/'
        return Response({'redirect_to': external_url})
