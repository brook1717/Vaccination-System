from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import F
from django.contrib.auth.decorators import login_required
from campaign.models import Campaign, Slot


@login_required
def campaign_list(request):
    today = timezone.now().date()
    campaigns = (
        Campaign.objects
        .filter(start_date__lte=today, end_date__gte=today)
        .select_related("vaccine", "center")
        .order_by("end_date")
    )
    paginator = Paginator(campaigns, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
    }
    return render(request, "campaign/campaign-list.html", context)


@login_required
def campaign_detail(request, id):
    campaign = get_object_or_404(
        Campaign.objects.select_related("vaccine", "center"), id=id
    )
    available_slots = (
        Slot.objects
        .filter(campaign=campaign, reserved__lt=F("max_capacity"))
        .order_by("date", "start_time")
    )

    context = {
        "campaign": campaign,
        "available_slots": available_slots,
    }
    return render(request, "campaign/campaign-detail.html", context)
