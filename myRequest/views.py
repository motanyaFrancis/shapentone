from datetime import datetime
import logging

import pytz
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from myRequest.serializers import LipaNaMpesaSerializer
from payment.models import LipaNaMpesaOnline


class LipaNaMpesaAPIView(CreateAPIView):
    queryset = LipaNaMpesaOnline.objects.all()
    serializer_class = LipaNaMpesaSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        try:
            logger = logging.getLogger("selfservice")
            logger.info("Mpesa Data: %s", request.data)

            callback_data = request.data.get("Body", {}).get("stkCallback", {})
            if not callback_data:
                raise KeyError("Invalid M-Pesa callback data")

            merchant_request_id = callback_data.get("MerchantRequestID")
            checkout_request_id = callback_data.get("CheckoutRequestID")
            result_code = callback_data.get("ResultCode")
            result_description = callback_data.get("ResultDesc")

            callback_metadata = callback_data.get(
                "CallbackMetadata", {}).get("Item", [])
            if len(callback_metadata) >= 5:
                amount = callback_metadata[0].get("Value")
                mpesa_receipt_number = callback_metadata[1].get("Value")
                transaction_date = callback_metadata[3].get("Value")
                phone_number = callback_metadata[4].get("Value")
            else:
                raise KeyError("Invalid M-Pesa callback data")

            str_transaction_date = str(transaction_date)

            transaction_datetime = datetime.strptime(
                str_transaction_date, "%Y%m%d%H%M%S")
            aware_transaction_datetime = pytz.utc.localize(
                transaction_datetime)

            our_model = LipaNaMpesaOnline.objects.create(
                CheckoutRequestID=checkout_request_id,
                MerchantRequestID=merchant_request_id,
                Amount=amount,
                ResultCode=result_code,
                ResultDesc=result_description,
                MpesaReceiptNumber=mpesa_receipt_number,
                TransactionDate=aware_transaction_datetime,
                PhoneNumber=phone_number,
            )

            our_model.save()
            return Response({"OurResultDesc": "YEEY!!! It worked!"})

        except KeyError as e:
            logger.error("Missing key in M-Pesa callback data. Error: %s", e)
            return Response({"error": "Invalid M-Pesa callback data"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error("Error processing M-Pesa callback. Error: %s", e)
            return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
