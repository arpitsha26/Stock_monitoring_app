from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Stock
from .serializers import StockSerializer


class stocklist(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        stocks = Stock.objects.all()
        subscribed_only = request.query_params.get("subscribed_only")
        if subscribed_only == "true":
            stocks = stocks.filter(subscribers=request.user)
        serializer = StockSerializer(stocks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class subscribestock(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        symbols = request.data.get("symbols", [])
        stocks = Stock.objects.filter(symbol__in=symbols)
        request.user.subscribed_stocks.add(*stocks)
        return Response(
            {"message": f"Subscribed to {symbols}."}, status=status.HTTP_200_OK
        )

    def delete(self, request):
        symbols = request.data.get("symbols", [])
        stocks = Stock.objects.filter(symbol__in=symbols)
        request.user.subscribed_stocks.remove(*stocks)
        return Response(
            {"message": f"Unsubscribed from {symbols}."}, status=status.HTTP_200_OK
        )
