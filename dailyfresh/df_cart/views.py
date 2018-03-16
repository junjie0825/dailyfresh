from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from df_user import user_decorator
from .models import *


@user_decorator.login
def cart(request):
    uid = request.session.get('user_id')
    carts = CartInfo.objects.filter(user_id=uid)
    context = {
        'title': '购物车',
        'carts': carts,
    }
    # context = {}
    print(context)
    return render(request, 'df_cart/cart.html', context)


@user_decorator.login
def add(request, gid, count):
    uid = request.session['user_id']
    gid = int(gid)
    count = int(count)
    carts = CartInfo.objects.filter(user_id=uid, goods_id=gid)
    if len(carts) >= 1:
        cart = carts[0]
        cart.count = cart.count + count
    else:
        cart = CartInfo()
        cart.count = count
        cart.user_id = uid
        cart.goods_id = gid
    cart.save()
    # 如果是ajax请求则返回json，否则转向购物车
    if request.is_ajax():
        count = CartInfo.objects.filter(user_id=request.session['user_id']).count()
        print(count)
        return JsonResponse({'count': count})
    else:
        return redirect('/cart/')


@user_decorator.login
def edit(request, cart_id, count):
    try:
        cart = CartInfo.objects.get(pk=int(cart_id))
        cart.count = int(count)
        cart.save()
        data = {'ok': 0}
    except Exception as e:
        data = {'ok': int(count)}
    return JsonResponse(data)


@user_decorator.login
def delete(request, cart_id):
    try:
        cart = CartInfo.objects.get(pk=int(cart_id))
        cart.delete()
        data = {'ok': 1}
        print(data)
    except Exception as e:
        data = {'ok': 0}
        print(e)
        print(data)
    return JsonResponse(data)




