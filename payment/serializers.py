# serializers.py
from rest_framework import serializers

from payment.models import PaymentTransaction


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentTransaction
        fields = '__all__'
