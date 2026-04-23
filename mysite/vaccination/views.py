from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import transaction
from django.db.models import F
from campaign.models import Campaign, Slot
from center.models import Storage
from vaccination.models import Vaccination


@login_required
@require_POST
def book_slot(request, slot_id):
    slot = get_object_or_404(Slot.objects.select_related("campaign__center", "campaign__vaccine"), id=slot_id)
    campaign = slot.campaign

    # Prevent duplicate booking for the same campaign
    if Vaccination.objects.filter(patient=request.user, campaign=campaign).exists():
        messages.error(request, "You have already booked a slot for this campaign.")
        return HttpResponseRedirect(reverse("campaign:detail", kwargs={"id": campaign.id}))

    try:
        with transaction.atomic():
            # Lock the slot row and re-check capacity
            locked_slot = (
                Slot.objects
                .select_for_update()
                .get(id=slot.id)
            )
            if locked_slot.reserved >= locked_slot.max_capacity:
                messages.error(request, "Sorry, this slot is already full.")
                return HttpResponseRedirect(reverse("campaign:detail", kwargs={"id": campaign.id}))

            # Lock the storage row and check vaccine stock
            try:
                storage = (
                    Storage.objects
                    .select_for_update()
                    .get(center=campaign.center, vaccine=campaign.vaccine)
                )
            except Storage.DoesNotExist:
                messages.error(request, "This center has no stock of the required vaccine.")
                return HttpResponseRedirect(reverse("campaign:detail", kwargs={"id": campaign.id}))

            if storage.booked_quantity >= storage.total_quantity:
                messages.error(request, "This center has no remaining vaccine doses available.")
                return HttpResponseRedirect(reverse("campaign:detail", kwargs={"id": campaign.id}))

            # All checks passed — atomically update counters
            Slot.objects.filter(id=locked_slot.id).update(reserved=F("reserved") + 1)
            Storage.objects.filter(id=storage.id).update(booked_quantity=F("booked_quantity") + 1)

            # Create the vaccination record
            Vaccination.objects.create(
                patient=request.user,
                campaign=campaign,
                slot=locked_slot,
                date=locked_slot.date,
            )

    except Exception:
        messages.error(request, "An error occurred while processing your booking. Please try again.")
        return HttpResponseRedirect(reverse("campaign:detail", kwargs={"id": campaign.id}))

    messages.success(request, "Slot booked successfully!")
    return HttpResponseRedirect(reverse("vaccination:booking-success", kwargs={"slot_id": slot.id}))


@login_required
def booking_success(request, slot_id):
    slot = get_object_or_404(Slot.objects.select_related("campaign__vaccine", "campaign__center"), id=slot_id)
    vaccination = get_object_or_404(Vaccination, patient=request.user, slot=slot)

    context = {
        "vaccination": vaccination,
        "slot": slot,
        "campaign": slot.campaign,
    }
    return render(request, "vaccination/booking-success.html", context)
