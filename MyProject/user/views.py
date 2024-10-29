from django.shortcuts import render
from django.http import HttpResponse
from . models import *
from datetime import datetime
from django.db import connection
# Create your views here.
def index(request):
    data=category.objects.all().order_by('-id') [0:12]
    sliderdata=slider.objects.all().order_by('-id')[0:3]
    pdata=myproduct.objects.all().order_by('-id')[0:18]
    opdata=myproduct.objects.filter(total_discount__gte=30)
    md = {"cdata": data,"sdata":sliderdata,"pdata":pdata,"odata":opdata}
    return render(request,'user/index.html',md)
def about(request):
    return render(request,'user/aboutus.html')


def product(request):
   subcatid=request.GET.get('sid')
   catid=request.GET.get('cid')
   sdata=subcategory.objects.all().order_by('-id')
   if subcatid is not None:
    pdata=myproduct.objects.all().filter(product_subcategory=subcatid)
   elif catid is not None:
       pdata=myproduct.objects.all().filter(product_category=catid)
   else:
    pdata = myproduct.objects.all().order_by('-id')
   md={
   'subcat':sdata,
   'pdata':pdata,
   }
   return render(request,'user/product.html',md)
def contact(request):
    if request.method=="POST":
      a1 = request.POST.get('name')
      a2 = request.POST.get('email')
      a3 = request.POST.get('mobile')
      a4 = request.POST.get('message')
      #print(a1,a2,a3,a4)
      x= contactus(Name=a1,Email=a2,Mobile=a3,Message=a4).save()
      return HttpResponse("<script> alert('Thank you! for contacting with us....');window.location.href='/user/contact/'</script>")


    return render(request,'user/contactus.html')
def signin(request):
    if request.method=="POST":
        email=request.POST.get('email')
        passwd=request.POST.get('passwd')
        x=register.objects.filter(email=email,passwd=passwd).count()
        if x==1:
            y=register.objects.all().filter(email=email,passwd=passwd)
            request.session['user']=email
            request.session['userpic']=str(y[0].profile)
            request.session['username']=str(y[0].name)
            user=request.session.get('user')
            cartitems=cart.objects.all().filter(userid=user).count()
            request.session['cartitems'] = cartitems
            return HttpResponse("<script>location.href='/user/signin/'</script>")

        else:
            return HttpResponse("<script> alert ('Your username or password is incorrect!');location.href='/user/signin/'</script>")
    return render(request,'user/signin.html')
def signup(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        mobile=request.POST.get('mobile')
        passwd=request.POST.get('passwd')
        address=request.POST.get('address')
        pic =request.FILES['fu']
        x=register.objects.all().filter(email=email).count()
        if x==1:
            return HttpResponse("<script> alert('You are already registered!....');location.href='/user/signup/'</script>")
        else:
             register(name=name, email=email, address=address, mobile=mobile, passwd=passwd, profile=pic).save()
             return HttpResponse("<script> alert ('You are registered successfully!....');location.href='/user/signup/'</script>")
    return render(request,'user/signup.html')

def signout(request):
    if request.session.get('user'):
        del request.session['user']
        del request.session['userpic']
        return HttpResponse("<script>location.href='/user/index/'</script>")
    return render(request,'user/signout.html')

def myprofile(request):
    user=request.session.get('user')
    if request.method=="POST":
        name=request.POST.get('name')
        mobile=request.POST.get('mobile')
        passwd=request.POST.get('passwd')
        address=request.POST.get('address')
        pic =request.FILES['fu']
        register(name=name,email=user,mobile=mobile,passwd=passwd,address=address,profile=pic)
        return HttpResponse("<script>alert('Your profile has been updated successfully!');location.href='/user/myprofile/'</script>")
    rdata=""
    if user:
     rdata=register.objects.filter(email=user)

    md={"rdata":rdata}
    return render(request,'user/myprofile.html',md)

def mycart(request):
    user=request.session.get('user')
    if user:
      pname=request.GET.get('pname')
      qt=int(request.GET.get('qt'))
      ppic=request.GET.get('ppic')
      pw=request.GET.get('pw')
      price=int(request.GET.get('price'))
      total_price=qt*price
      if qt>0:
       cart(userid=user,product_name=pname,quantity=qt,price=price,total_price=total_price,product_picture=ppic,pw=pw,added_date=datetime.now().date()).save()
       cartitems=cart.objects.all().filter(userid=user).count()
       request.session['cartitems']=cartitems
       return HttpResponse("<script>alert('Your item is added to cart!');location.href='/user/product/'</script>")
      else:
          return HttpResponse("<script> alert('Please increase your cart items!');location.href='/user/product/'</script>")
    return render(request,'user/mycart.html')

def cartitems(request):
    user=request.session.get('user')
    cid=request.GET.get('cid')
    cartdata="";
    if user:
        cartdata=cart.objects.filter(userid=user)
        if cid is not None:
            cart.objects.filter(id=cid).Delete()
            cartitems = cart.objects.all().filter(userid=user).count()
            request.session['cartitems'] = cartitems
            return HttpResponse("<script> alert('Your cart item is placed successfully!');location.href='/user/cartitems/'</script>")
    md={"cartdata":cartdata}
    return render(request,'user/cartitems.html',md)

def morder(request):
    msg=request.GET.get('msg')
    user=request.session.get('user')
    if msg is not None:
        cursor=connection.cursor()
        cursor.execute("insert into user_myorders (product_name,quantity,price,total_price,product_picture,pw,userid,status,order_date) select product_name,quantity,price,total_price,product_picture,pw,'"+str(user)+"','Pending','"+str(datetime.now().date())+"' from user_cart where userid='"+str(user)+"'")
        cart.objects.filter(userid=user).delete()
        cartitems = cart.objects.all().filter(userid=user).count()
        request.session['cartitems'] = cartitems
        return HttpResponse ("<script>alert('Your order has been placed successfully!');location.href='/user/orderslist/'</script>")
    return render(request,'user/order.html')

def indexcart(request):
    user = request.session.get('user')
    if user:
        pname = request.GET.get('pname')
        qt = int(request.GET.get('qt'))
        ppic = request.GET.get('ppic')
        pw = request.GET.get('pw')
        price = int(request.GET.get('price'))
        total_price = qt * price
        if qt > 0:
            cart(userid=user, product_name=pname, quantity=qt, price=price, total_price=total_price,product_picture=ppic, pw=pw, added_date=datetime.now().date()).save()
            cartitems = cart.objects.all().filter(userid=user).count()
            request.session['cartitems'] = cartitems
            return HttpResponse("<script> alert('Your item is added to cart!');location.href='/user/index/'</script>")
        else:
          return HttpResponse ("<script> alert('Please increase your cart items!');location.href='/user/index/'</script>")

    return render(request,'user/indexcart.html')

def mprofile(request):
    return render(request,'mprofile.html')
def orderslist(request):
    oid=request.GET.get('oid')
    user=request.session.get('user')
    pdata=myorders.objects.filter(userid=user,status="Pending")
    adata=myorders.objects.filter(userid=user,status="Accepted")
    ddata=myorders.objects.filter(userid=user,status="Delivered")
    if oid is not None:
        myorders.objects.filter(id=oid).delete()
        return HttpResponse("<script> alert('Your order has been cancelled!....');location.href='/user/orderslist/'</script>")
    mydict={"pdata":pdata,"adata":adata,"ddata":ddata}
    return render(request,'user/orderslist.html',mydict)