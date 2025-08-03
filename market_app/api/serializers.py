from rest_framework import serializers
from market_app.models import Market, Seller, Product


def validate_no_x(value):
    errors = []
    if 'X' in value:
        # raise serializers.ValidationError('no X in location')
        errors.append('no X in location')
    if 'Y' in value:
        errors.append('no Y in location')
    if errors:
        raise serializers.ValidationError(errors)
    return value


class MarketHyperlinkedSerializer(serializers.HyperlinkedModelSerializer):
    sellers = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='seller_single_view')
    
    class Meta:
        model = Market
        exclude = ['net_worth', 'location']




class MarketSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=True)
    # name = serializers.CharField(max_length=255)
    # # location = serializers.CharField(max_length=255, validators=[validate_no_x])
    # location = serializers.CharField(max_length=255)
    # description = serializers.CharField()
    # net_worth = serializers.DecimalField(max_digits=100, decimal_places=2)

    # def create(self, validated_data):
    #     return Market.objects.create(**validated_data)
    
    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.location = validated_data.get('location', instance.location)
    #     instance.description = validated_data.get('description', instance.description)
    #     instance.net_worth = validated_data.get('net_worth', instance.net_worth)
    #     instance.save()
    #     return instance

    # sellers = serializers.StringRelatedField(many=True, read_only=True)
    sellers = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='seller_single_view')
    
    class Meta:
        model = Market
        fields = ['id', 'name', 'location', 'description', 'net_worth', 'sellers'] # Felder, die angezeigt werden
        # field = '__all__'
    
    # def validate_location(self, value):
    #     if 'X' in value:
    #         raise serializers.ValidationError('no X in location')
    #     return value


class SellerSerializer(serializers.ModelSerializer):
    # markets = MarketSerializer(many=True, read_only=True)
    markets = MarketSerializer(many=True, read_only=True)
    market_ids = serializers.PrimaryKeyRelatedField(
        queryset = Market.objects.all(),
        many = True,
        write_only = True,
        source = 'markets'
    )

    market_count = serializers.SerializerMethodField()
    class Meta:
        model = Seller
        fields = ['id', 'name', 'market_count', 'markets', 'market_ids', 'contact_info']
        # exclude = []

    def get_market_count(self, obj):
        return obj.markets.count()  # Markets werden gezählt


class SellerDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    contact_info = serializers.CharField()
    # markets = MarketSerializer(many=True, read_only=True)
    markets = MarketSerializer(many=True, read_only=True)


class SellerCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    contact_info = serializers.CharField()
    # markets = serializers.ListField(child=serializers.IntegerField(), write_only=True) # Liste mit den PKs der Märkte
    # markets = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    markets = serializers.StringRelatedField(many=True) # Liste mit den Namen der Märkte

    def validate_markets(self, value):
        markets = Market.objects.filter(id__in=value)   # Märkte werden anhand des value (Liste mit PKs) aus der DB geholt
        if len(markets) != len(value):
            # serializer = MarketSerializer(markets, many=True)
            raise serializers.ValidationError('One or more market ids not found!')
            # raise serializers.ValidationError(serializer.data)
            # raise serializers.ValidationError({"message": len(value)})
        return value
    
    def create(self, validated_data):
        market_ids = validated_data.pop('markets')
        seller = Seller.objects.create(**validated_data)
        markets = Market.objects.filter(id__in=market_ids)
        seller.markets.set(markets) # Zuordnung von Seller zu den Märkten
        return seller


class SellerListSerializer(SellerSerializer):
    class Meta:
        model = Seller
        fields = ['id', 'name', 'market_count', 'contact_info']
        
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'