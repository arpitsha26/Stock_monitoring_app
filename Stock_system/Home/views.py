from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Stock
from .serializers import StockSerializer, UserSerializer
from django.shortcuts import render


class stocklist(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        stocks = Stock.objects.all()
        subscribed_only = request.query_params.get("subscribed_only")
        if subscribed_only == "true":
            stocks = stocks.filter(subscribers=request.user)
        serializer = StockSerializer(stocks, many=True)
        return render(request, 'Home/stock_list.html', {'stocks': serializer.data})


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

class SignUpView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'Home/signup.html')

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return Response("user create")
        return render(request, 'Home/signup.html', {"errors": serializer.errors})