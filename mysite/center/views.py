from django.shortcuts import render
from center.models import Center, Storage
from center.forms import CenterForm, StorageForm
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.views import generic
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

# Create your views here.
@login_required
def center_list(request):
    objects = Center.objects.all().order_by("name")
    paginator = Paginator(objects, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)


    context = {
        "page_obj": page_obj, 
    }
    return render(request, "center/center-list.html", context)

@login_required
def center_detail(request, id):
    objects = Center.objects.get(id=id)
    context = {
        "center": objects,
    }
    return render(request, "center/center-detail.html", context)

@staff_member_required
def create_center(request):
    if request.method == "POST":
        form = CenterForm(request.POST)
        if form.is_valid():
            form.save()
            #message
            messages.success(request, "Vaccination Center Created Successfully")
            return HttpResponseRedirect(reverse("center:list"))
        messages.error(request, "Please Enter a Valid Data")
        return render(request, "center/create-center.html", {"form": form})

        # else:
        #     render(request, "center/create-center.html", {"form": form})
        
    #GET
    context={
        "form": CenterForm()

    }
    return render(request, "center/create-center.html", context)
    
@staff_member_required
def update_center(request, id):
    try:
        center = Center.objects.get(id=id)
    except Center.DoesNotExist:
        raise Http404("Center instance is not found")
    if request.method == "POST":
        form = CenterForm(request.POST, instance = center)
        if form.is_valid():
            form.save()
            messages.success(request, "Vaccinaiton Center Updated Successfully")
            return HttpResponseRedirect(reverse("center:detail", kwargs={"id": center.id}))
        messages.error(request, "Please Enter a Valid Data")
        return render (request, "center/update-center.html", {"form": form})


    #GEt
    context = {
        "form": CenterForm(instance = center)
    }
    return render (request, "center/update-center.html", context)

@staff_member_required
def delete_center(request, id):
    try:
        center = Center.objects.get(id=id)
    except Center.DoesNotExist:
        raise Http404("Center instance not found")
    if request.method == "POST":
        center.delete()
        messages.success(request, "Vaccination Center Deleted Succesfully")
        return HttpResponseRedirect(reverse("center:list"))
    #get
    context = {
        "center": center,
    }
    return render(request, "center/delete-center.html", context)


#generic views

class StorageList(LoginRequiredMixin, generic.ListView):
    queryset = Storage.objects.all()
    template_name = "storage/storage-list.html"
    ordering = ["id"]
    paginate_by = 2

    def get_queryset(self):
        return super().get_queryset().filter(center_id = self.kwargs["center_id"])
    def get_context_data(self, **kwargs):

        context =  super().get_context_data(**kwargs)
        context["center_id"] = self.kwargs["center_id"]
        return context



class StorageDetail(LoginRequiredMixin, generic.DetailView):
    model= Storage
    template_name = "storage/storage-detail.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["available_quantity"]= self.object.total_quantity - self.object.booked_quantity
        return context


class CreateStorage(StaffRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model= Storage
    form_class = StorageForm
    template_name = "storage/storage-create.html"
    success_message = "Storage Created Successfully"


    def get_form_kwargs(self):
        kwargs =  super().get_form_kwargs()
        kwargs["center_id"] = self.kwargs["center_id"]
        return kwargs
    

    #to chose the  center by default
    def get_initial(self):
        intial =  super().get_initial()
        intial["center"] = Center.objects.get(id=self.kwargs["center_id"])
        return intial
    def get_success_url(self):
        return reverse("center:storage-list", kwargs={"center_id": self.kwargs["center_id"]}) 
    


class StorageUpdate(StaffRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Storage
    form_class = StorageForm
    template_name = "storage/storage-update.html"
    success_message = "Storage Updated Successfully"


    def get_form_kwargs(self):
        kwargs =  super().get_form_kwargs()
        kwargs["center_id"] = self.get_object().center.id
        return kwargs
    

    def get_success_url(self):
        return reverse("center:storage-list", kwargs={"center_id": self.get_object().center.id})



class StorageDelete(StaffRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    model = Storage
    template_name = "storage/storage-delete.html"
    success_message = "Storage Deleted Successfully"

    def get_success_url(self):
        return reverse("center:storage-list", kwargs={"center_id": self.get_object().center.id})