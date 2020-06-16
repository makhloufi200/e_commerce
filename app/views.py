from django.shortcuts import render
from .models import Category, Items
# Create your views here.



def home(request):

    context = {
        "name": "Home"
    }

    return render(request, 'items/list_items.html', context)
	
def all_items(request):
	categs = Category.objects.all()
	objs = Items.objects.all()
	return render(request, 'items/list_items.html', {'items': objs,'categs':categs})