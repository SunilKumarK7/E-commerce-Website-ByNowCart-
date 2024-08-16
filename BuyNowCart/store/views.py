from django.shortcuts import render,redirect

# Create your views here.
from store.forms import SignUpForm,SignInForm
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from store.models import Product,Basket,BasketItems,order
class RegistrationView(View):
    def get(self,request,*args, **kwargs):
        form_instance=SignUpForm()
        return render(request,"register.html",{"form":form_instance})
    
    def post(self,request,*args, **kwargs):
        form_instance=SignUpForm(request.POST)
        
        if form_instance.is_valid():
            form_instance.save()
            #data=form_instance.cleaned_data
            #User.objects.create_user(**data)
            print("account created")
            return redirect('signin')
        print("acount not created")
        return render(request,"register.html",{"form":form_instance})
    
    
class LoginView(View):
    def get(self,request,*args, **kwargs):
        form_instance=SignInForm()
        return render(request,"signin.html",{"form":form_instance})
    
    def post(self,request,*args, **kwargs):
        form_instance=SignInForm(request.POST)
        
        if form_instance.is_valid():
            data=form_instance.cleaned_data
            uname=data.get("username")
            pwd=data.get("password")
            user_object=authenticate(request,username=uname,password=pwd)
            if user_object:
                login(request,user_object)
                print("Successfully login")
                return redirect('index')
            
        print("login failed")
        return render(request,"register.html",{"form":form_instance})    
        
class IndexView(View):
    def get(self,request,*args, **kwargs):
        qs=Product.objects.all()
        return render(request,"index.html",{"data":qs}) 
    
class ProductDetailView(View):
    def get(self,request,*args, **kwargs):
        id=kwargs.get("pk")
        qs=Product.objects.get(id=id)
        print(qs)
        return render(request,"product_detail.html",{"data":qs})
    
    
#localhost:8000/products/{id}/carts/add/
class AddToCartView(View):
    def post(self,request,*args, **kwargs):
        id=kwargs.get("pk")
        product_obj=Product.objects.get(id=id)
        basket_obj=request.user.cart #parent referencing
        #size_name=request.POST.get("size")
        #size_obj=Size.objects.get(name=size_name)
        qty=request.POST.get("qty")
        #basket item_obj
        basket_item_obj=BasketItems.objects.filter(basket_object=basket_obj,product_object=product_obj,is_order_placed=False)
        
        if basket_item_obj:
            basket_item_obj[0].quantity+=int(qty)
            basket_item_obj[0].save()
        else:
            BasketItems.objects.create(
                basket_object=basket_obj,
                product_object=product_obj,
                #size_object=size_obj,
                quantity=qty
            
           )
        print(qty)
        
        print("item added to cart") 
        return redirect("index")
    
class CartSummaryView(View):
    def get(self,request,*args, **kwargs):
        qs=request.user.cart.cartitems.filter(is_order_placed=False)#.order_by("-created_date")
        return render(request,"cart_list.html",{"data":qs})
        
        
#url=localhost:8000/basketitem/{id}

class CartItemDestroyView(View):
    def get(self,request,*args, **kwargs):
        id=kwargs.get("pk")
        BasketItems.objects.get(id=id).delete()
        return redirect("cart-summary")

class SignOutView(View):
    def get(self,request,*args, **kwargs):
        logout(request)
        return redirect("signin")
    
class CartQuantityUpdateView(View):
    def post(self,request,*args, **kwargs):
        id=kwargs.get("pk")
        basket_item_obj=BasketItems.objects.get(id=id)
        action=request.POST.get("action")
        
        if action=='increment':
            basket_item_obj.quantity+=1
        else:
            basket_item_obj.quantity-=1
        basket_item_obj.save()
        return redirect("cart-summary")  
    
    
class PlaceOrderView(View):
    def get(self,request,*args, **kwargs):
        return render(request,"place_order.html")
    
    def post(self,request,*args, **kwargs):
        email=request.POST.get("email")
        phone=request.POST.get("phone")
        address=request.POST.get("address")
        payment_mode=request.POST.get("payment_mode")
        pin=request.POST.get("pin")
        
        user_obj=request.user
        
        cart_item_objects=request.user.cart.cartitems.filter(is_order_placed=False)
        print("jjjjjcart",cart_item_objects)
        print(email,"kk",payment_mode)
        if payment_mode=="cod":
            order_obj=order.objects.create(
                user_object=user_obj,
                delivery_address=address,
                phone=phone,
                pin=pin,
                email=email,
                payment_mode=payment_mode
            )
            print(order_obj)
        print(order_obj)
           
        for bi in cart_item_objects:
            print("ll",bi)
            order_obj.basket_item_objects.add(bi)
            bi.is_order_placed=True
            bi.save()
            
        order_obj.save()
        
        print(email,phone,address,payment_mode,pin)
        return redirect("index")
    
    
class OrderSummaryView(View):
    def get(self,request,*args, **kwargs):
        qs=order.objects.filter(user_object=request.user).order_by("-created_date")
        print(qs)
        return render(request,"order_summary.html",{'data':qs})
    

class SamsungMobView(View):
    def get(self,request,*args, **kwargs):
        qs=Product.objects.all()
        k=[]
        for i in qs:
           print(i.brand_object)
          
          
           k.append(i.brand_object)
        print(k[2])
        j=k[2]
        for i in qs:
            if i.brand_object==j:
               js=Product.objects.filter(brand_object=j)
               print('fffffff',js)
                
        print(i.brand_object)
            
        return render(request,"index.html",{"data":js,"sams":j})

'''class SamsungMobView(View):
    def get(self, request, *args, **kwargs):
        # Filter the products directly in the query
        qs = Product.objects.filter(brand_object='Samsung')
        
        # Debug print statement (optional, for debugging purposes)
        for product in qs:
            print(product.brand_object)
        
        # Render the template with the filtered data
        return render(request, "samsung_mob.html", {"data": qs})'''
        
class AppleMobView(View):
    def get(self,request,*args, **kwargs):
        qs=Product.objects.all()
        k=[]
        for i in qs:          
           k.append(i.brand_object)
        print(k[0])
        j=k[0]
        for i in qs:
            if i.brand_object==j:
               js=Product.objects.filter(brand_object=j)
               print('fffffff',js)
                
        print(i.brand_object)
            
        return render(request,"index.html",{"data":js})
    
class OnePlusMobView(View):
    def get(self,request,*args, **kwargs):
        qs=Product.objects.all()
        k=[]
        for i in qs:          
           k.append(i.brand_object)
        print(k[0])
        j=k[1]
        for i in qs:
            if i.brand_object==j:
               js=Product.objects.filter(brand_object=j)
               print('fffffff',js)
                
        print(i.brand_object)
            
        return render(request,"index.html",{"data":js})
    
class RealmeMobView(View):
    def get(self,request,*args, **kwargs):
        qs=Product.objects.all()
        k=[]
        for i in qs:          
           k.append(i.brand_object)
        print(k[4])
        j=k[4]
        for i in qs:
            if i.brand_object==j:
               js=Product.objects.filter(brand_object=j)                
            
        return render(request,"index.html",{"data":js})
    
class MotoMobView(View):
    def get(self,request,*args, **kwargs):
        qs=Product.objects.all()
        k=[]
        for i in qs:          
           k.append(i.brand_object)
        print(k[5])
        j=k[5]
        for i in qs:
            if i.brand_object==j:
               js=Product.objects.filter(brand_object=j)                
            
        return render(request,"index.html",{"data":js})
    
class MITvView(View):
    def get(self,request,*args, **kwargs):
        qs=Product.objects.all()
        k=[]
        for i in qs:          
           k.append(i.brand_object)
        print(k[6])
        j=k[6]
        for i in qs:
            if i.brand_object==j:
               js=Product.objects.filter(brand_object=j)                
            
        return render(request,"tv.html",{"data":js})
    
    
class DellLapView(View):
    def get(self,request,*args, **kwargs):
        qs=Product.objects.all()
        k=[]
        for i in qs:          
           k.append(i.brand_object)
        print(k[7])
        j=k[7]
        for i in qs:
            if i.brand_object==j:
               js=Product.objects.filter(brand_object=j)                
            
        return render(request,"lap.html",{"data":js})
    
class BoatWatchView(View):
    def get(self,request,*args, **kwargs):
        qs=Product.objects.all()
        k=[]
        for i in qs:          
           k.append(i.brand_object)
        print(k[8])
        j=k[8]
        for i in qs:
            if i.brand_object==j:
               js=Product.objects.filter(brand_object=j)                
            
        return render(request,"watch.html",{"data":js})
    
class JBLSpeakerView(View):
    def get(self,request,*args, **kwargs):
        qs=Product.objects.all()
        k=[]
        for i in qs:          
           k.append(i.brand_object)
        print(k[9])
        j=k[9]
        for i in qs:
            if i.brand_object==j:
               js=Product.objects.filter(brand_object=j)                
            
        return render(request,"speakers.html",{"data":js})
    