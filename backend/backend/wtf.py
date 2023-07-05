from rest_framework.views import APIView
from rest_framework.response import Response
from cryptography.fernet import Fernet


class DecryptView(APIView):
    def get(self, request, format=None):
        # Ваш зашифрованный текст
        cipher_text = b"gAAAAABkpTu4jSiVxR3tST1QM7VWtK0Ld-ZeXymBUaQMQx271d95V8D3ReRFlStH_0f8nUhJsQXmxIl8IotIvzIGBKGJuzd0Hbk-qN9pi8-nzS-AdA2dVDE="

        # Используйте ваш ключ для дешифрования
        key = b"Teg2f5LYVSWTS-E77Gnltiy287qCFBqsWc68m0Is_Dg="  # Ключ должен храниться в безопасном месте, не в коде!
        cipher_suite = Fernet(key)
        plain_text = cipher_suite.decrypt(cipher_text)

        return Response({"message": plain_text.decode('utf-8')})
