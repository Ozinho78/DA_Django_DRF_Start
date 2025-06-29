from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import MarketSerializer, SellerDetailSerializer, SellerCreateSerializer, SellerSerializer
from market_app.models import Market, Seller


# @api_view() # standardmäßig GET-Anfrage
@api_view(['GET', 'POST'])  # GET- und POST-Anfragen
def markets_view(request):
    if request.method == 'GET':
        markets = Market.objects.all()
        serializer = MarketSerializer(markets, many=True)   # da MarketSerializer für ein Element geschrieben wurde, muss man many=True angeben, dann wird es für alle Elemente verwendet und Liste übergeben
        # return Response({"message": "Hello, World!"})
        return Response(serializer.data)

    if request.method == 'POST':
        # try:
        #     msg = request.data['message']
        #     return Response({"your_message": msg}, status=status.HTTP_201_CREATED)
        # except:
        #     return Response({"message": "error"}, status=status.HTTP_400_BAD_REQUEST)
        # pass
        serializer = MarketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET', 'DELETE', 'PUT'])
def market_single_view(request, pk):
    if request.method == 'GET':
        market = Market.objects.get(pk=pk)
        serializer = MarketSerializer(market)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        market = Market.objects.get(pk=pk)
        serializer = MarketSerializer(market, data=request.data, partial=True)  # partial bedeutet, dass auch nur Teile des Objekts geändert werden können
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
    if request.method == 'DELETE':
        market = Market.objects.get(pk=pk)
        serializer = MarketSerializer(market)
        market.delete()
        return Response(serializer.data)
    

@api_view(['GET', 'POST'])
def sellers_view(request):
    if request.method == 'GET':
        sellers = Seller.objects.all()
        # serializer = SellerDetailSerializer(sellers, many=True)
        serializer = SellerSerializer(sellers, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        # serializer = SellerCreateSerializer(data=request.data)
        serializer = SellerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        