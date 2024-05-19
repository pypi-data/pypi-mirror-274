import random
from typing import Any
from colour import Color
from django.views.generic import ListView
from django.core.paginator import Paginator
from colorfield.fields import ColorField
from django.db import models
from django.urls import path
import inspect

def listrand(min,max,kol):
    a=[]
    otch = 0
    while otch<kol:
        a.append(random.randint(min,max))
        otch+=1
    return a

def IsKeyInDict(data, key):
    return key in data
def stepen(number,stepan):
	if stepan==0:
		return 1
	
	else :
		return number * stepen(number,stepan-1)
	
def faktorial(number):
	
	if number==0 or number == 1:
		return 1
	

	else:
		return number * faktorial(number-1)
	
def chibo(number):
	
	if number==0:
		return 1
	
	elif number==1:
		return 0
	
	else:
		return chibo(number-1) + chibo(number-2)
	
def summa(number):
	if number<1:
		return 0
	
	else:
	    return int(number%10) + summa(number/10)
	
def find(lst,sim,n = 0):
	if (n==lst.length()):
		return 0
	
	else:
		if lst[n]==sim:
			return  1+find(lst,sim,n+1)
		else:
			return find(lst,sim,n+1)
	
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def brightness(rgb):
    return (rgb[0]*299 + rgb[1]*587 + rgb[2]*114) / 1000

def isdarker(color, porog):
    color1 = Color(color)
    color2 = Color(porog)
    return color1.luminance < color2.luminance

def iswhiter(color, porog):
    color1 = Color(color)
    color2 = Color(porog)
    return color1.luminance > color2.luminance


def proverka_set(dct,key,newper=None):
	if dct.get(key)==None:
		dct[key]=newper


def adder(dct,**kwargs):
	for i in kwargs.keys():
		dct[i] = kwargs[i]
	return dct


def sejango(form,key,var):
	if form.cleaned_data.get(key)==None:
		return var
	else :
		return form.cleaned_data.get(key,0)
	


def call_methods_by_partial_name(class_instance, partial_name, *args, **kwargs):
    a = []
    for name, method in inspect.getmembers(class_instance, inspect.ismethod):
        if name.startswith(partial_name):
            result = method(*args, **kwargs)
            a.append(result)
    return a


CFBPN=call_methods_by_partial_name
Mcall=call_methods_by_partial_name

def call_functions_by_partial_name(partial_name, *args, **kwargs):
    a = []
    for name, obj in inspect.getmembers(inspect.currentframe().f_back):
        if inspect.isfunction(obj) and name.startswith(partial_name):
            a.append(obj(*args, **kwargs))
    return a

CFBPN=call_functions_by_partial_name
Fcall=call_functions_by_partial_name

# function django

def allpath(route: str, view, name: str):
    a = []
    if route[-1] == "/":
        a.append(path(route, view, name=name))
        a.append(path(route[:-1], view, name=name))
    else:
        a.append(path(route, view, name=name))
        a.append(path(route + "/", view, name=name))
    return a


# class django



class LBASE(ListView):
	context_paginator_name = "page"
	page_n=0

	def get_paginate_by(self, queryset) -> int | None:
		if len(queryset) >= self.page_n and self.page_n>0:
			return int(len(queryset) / self.page_n)
		else:
			return super().get_paginate_by(queryset)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		if self.paginate_by!=None:
			paginator = Paginator(self.object_list, self.paginate_by)
			page_obj = self.request.GET.get('page')
			paginator = paginator.get_page(page_obj)
			context[self.context_paginator_name]=paginator.paginator.page_range
		return context

# class BModels:
class Color(models.Model):
    color=ColorField(verbose_name="цвет",default='#FF0000')
    
    class Meta:
        abstract = True
    def isdarker(self, porog):
        return isdarker(color=self.color,porog=porog)
    def iswhite(self,porog):
        return iswhiter(color=self.color,porog=porog)
    def hexrgb(self,HEX):
        return hex_to_rgb(HEX)
    def rgbtofloat(self,rgb):
        return brightness(rgb)
