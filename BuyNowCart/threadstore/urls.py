"""
URL configuration for threadstore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from store import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',views.RegistrationView.as_view(),name="register"),
    path("",views.LoginView.as_view(),name="signin"),
    path('index/',views.IndexView.as_view(),name="index"),
    path('products/<int:pk>/',views.ProductDetailView.as_view(),name="product-detail"),
    path('products/<int:pk>/cart/add/',views.AddToCartView.as_view(),name="addto-cart"),
    path('carts/all/',views.CartSummaryView.as_view(),name='cart-summary'),
    path("basketitem/<int:pk>/remove",views.CartItemDestroyView.as_view(),name="cart-remove"),
    path('signout/',views.SignOutView.as_view(),name="signout"),
    path("basketitems/quantity/<int:pk>/change",views.CartQuantityUpdateView.as_view(),name="quantity-update"),
    path("order/add/",views.PlaceOrderView.as_view(),name="place-order"),
    path("order/summary/",views.OrderSummaryView.as_view(),name="order-summary"),
    path('samsung/',views.SamsungMobView.as_view(),name="samsung-mobs"),
    path('apple/',views.AppleMobView.as_view(),name="apple-mobs"),
    path('oneplus/',views.OnePlusMobView.as_view(),name="oneplus-mobs"),
    path('realme/',views.RealmeMobView.as_view(),name="realme-mobs"),
    path('moto/',views.MotoMobView.as_view(),name="moto-mobs"),
    path('mi/',views.MITvView.as_view(),name="mi-tv"),
    path('dell/',views.DellLapView.as_view(),name="dell-lap"),
    path('boat/',views.BoatWatchView.as_view(),name="boat-watch"),
    path('jbl/',views.JBLSpeakerView.as_view(),name="jbl-speakers"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

