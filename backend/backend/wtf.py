from cryptography.fernet import Fernet
from rest_framework.response import Response
from rest_framework.views import APIView


class DecryptView(APIView):
    def get(self, request, format=None):
        cipher_text = (b'gAAAAABkpTu4jSiVxR3tST1QM7VWtK0Ld'
                       b'-ZeXymBUaQMQx271d95V8D3ReRFlStH_0f8nUhJsQ'
                       b'XmxIl8IotIvzIGBKGJuzd0Hbk-qN9pi8-nzS-AdA2dVDE=')

        key = b'Teg2f5LYVSWTS-E77Gnltiy287qCFBqsWc68m0Is_Dg='
        cipher_suite = Fernet(key)
        plain_text = cipher_suite.decrypt(cipher_text)

        return Response({'message': plain_text.decode('utf-8')})
