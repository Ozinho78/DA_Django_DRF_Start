from django.urls import path, include
from .views import markets_view, MarketsView, MarketSingleView, market_single_view, sellers_view, seller_single_view, MarketSellerView, ProductViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'products', ProductViewSet)


urlpatterns = [
    path('', include(router.urls)),
    # path('market/', markets_view),
    path('market/', MarketsView.as_view()),
    # path('market/<int:pk>/', market_single_view, name='market-detail'),
    path('market/<int:pk>/', MarketSingleView.as_view(), name='market-detail'),
    path('market/<int:pk>/sellers/', MarketSellerView.as_view(), name='market-sellers'),
    path('seller/', sellers_view),
    path('seller/<int:pk>/', seller_single_view, name='seller_single_view'),
]