from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import MarketSerializer, SellerDetailSerializer, SellerCreateSerializer, SellerSerializer, MarketHyperlinkedSerializer, SellerListSerializer
from market_app.models import Market, Seller
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics


# class MarketsView(APIView):
# class MarketsView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
class MarketsView(generics.ListAPIView):
    queryset = Market.objects.all()
    serializer_class = MarketSerializer
    
    # Mixins
    # def get(self, request, *args, **kwargs):
    #     return self.list(request, *args, **kwargs)
    
    # def post(self, request, *args, **kwargs):
    #     return self.create(request, *args, **kwargs)
    
    # def get(self, request):
    #     markets = Market.objects.all()
    #     # serializer = MarketHyperlinkedSerializer(markets, many=True, context={'request': request})
    #     serializer = MarketSerializer(markets, many=True, context={'request': request})
    #     return Response(serializer.data)

    # def post(self, request):
    #     serializer = MarketSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# class MarketSingleView(mixins.RetrieveModelMixin,mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
class MarketSingleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Market.objects.all()
    serializer_class = MarketSerializer

    # def get(self, request, *args, **kwargs):
    #     return self.retrieve(request, *args, **kwargs)

    # def put(self, request, *args, **kwargs):
    #     return self.update(request, *args, **kwargs)

    # def delete(self, request, *args, **kwargs):
    #     return self.destroy(request, *args, **kwargs)
    
    
class MarketSellerView(generics.ListCreateAPIView):
    # serializer_class = SellerSerializer
    serializer_class = SellerListSerializer # separater Serializer, in dem die Market-Daten entfernt wurden
    
    def get_queryset(self):
        pk = self.kwargs['pk']  # get the id from the url
        market = Market.objects.get(pk=pk)
        return market.sellers.all()
    
    
    
    
    
    
    
    
    
    


# @api_view() # standardmäßig GET-Anfrage
@api_view(['GET', 'POST'])  # GET- und POST-Anfragen
def markets_view(request):
    if request.method == 'GET':
        markets = Market.objects.all()
        # serializer = MarketSerializer(markets, many=True)   # da MarketSerializer für ein Element geschrieben wurde, muss man many=True angeben, dann wird es für alle Elemente verwendet und Liste übergeben
        # return Response({"message": "Hello, World!"})
        serializer = MarketSerializer(markets, many=True, context={'request': request}) # Context notwendig, da HyperLinkedRelatedField verwendet wird
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
        # serializer = MarketSerializer(market)
        serializer = MarketSerializer(market, context={'request': request})
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
        serializer = SellerSerializer(sellers, many=True, context={'request': request})
        return Response(serializer.data)

    if request.method == 'POST':
        # serializer = SellerCreateSerializer(data=request.data)
        serializer = SellerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        

@api_view()
def seller_single_view(request, pk):
    if request.method == 'GET':
        seller = Seller.objects.get(pk=pk)
        serializer = SellerSerializer(seller, context={'request': request})
        return Response(serializer.data)