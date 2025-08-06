from django.shortcuts import render
from center.models import Center
from center.forms import CenterForm
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.
def center_list(request):
    objects = Center.objects.all()
    context = {
        "center": objects, 
    }
    return render(request, "center/center-list.html", context)

def center_detail(request, id):
    objects = Center.objects.get(id=id)
    context = {
        "center": object,
    }
    return render(request, "center/center-detail.html", context)

def create_center(request):
    if request.method == "POST":
        form = CenterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("center:list"))

        else:
            render(request, "center/create-center.html", {"form": form})
        
    #GET
    context={
        "form": CenterForm()

    }
    return render(request, "center/create-center.html", context)
    