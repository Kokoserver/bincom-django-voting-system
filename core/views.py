import datetime
from django.shortcuts import render
from .models import AnnouncedPuResults, Lga, Party, PollingUnit, Ward
from django.db.models import Sum
from django.contrib.messages import success, error
poll = PollingUnit.objects.all()

def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def index(request):
    polling_units = PollingUnit.objects.all()
    local_govs = Lga.objects.all()
    return render(
        request=request,
        template_name="pages/index.html",
        context={"polling_units": polling_units, "local_govs": local_govs},
    )


def addVote(request):
    try:
        if request.method == "POST":
            last_polling_unit = PollingUnit.objects.all().last()
            lga_id = request.POST.get("lga")
            ward = Ward.objects.filter(ward_id=request.POST.get("ward")).first()
            polling_unit_number = request.POST.get("polling_unit_number")
            pollingdesc = request.POST.get("pollingdesc")
            polling_unit_name = request.POST.get("polling_unit_name")
            longitude = request.POST.get("longitude")
            latitude = request.POST.get("latitude")
            enter_by = request.POST.get("enter_by")
            parties = [
                {
                    "id": party.partyid,
                    "name": party.partyname,
                    "score": request.POST.get(f"{party.partyname}"),
                }
                for party in Party.objects.all()
            ]

            new_polling_unit = PollingUnit.objects.create(
                ward_id=ward.ward_id,
                lga_id=lga_id,
                polling_unit_id=last_polling_unit.polling_unit_id + 1,
                uniquewardid=ward.uniqueid,
                polling_unit_number=polling_unit_number,
                polling_unit_name=polling_unit_name,
                polling_unit_description=pollingdesc,
                entered_by_user=enter_by,
                date_entered=datetime.datetime.now(),
                user_ip_address=get_client_ip(request),
                lat=latitude,
                long=longitude,
            )
            for party in parties:
                AnnouncedPuResults.objects.create(
                    polling_unit_uniqueid=new_polling_unit.uniquewardid,
                    party_abbreviation=party["name"],
                    party_score=party["score"],
                    entered_by_user=enter_by,
                    date_entered=datetime.datetime.now(),
                    user_ip_address=get_client_ip(request),
                )
            success(request, "Success: polling unit was successfully created")
    except:
        error(request, "Danger: polling unit could not be created")

    local_govs = Lga.objects.all()
    wards = Ward.objects.all()
    parties = Party.objects.all()

    return render(
        request=request,
        template_name="pages/addvote.html",
        context={"local_govs": local_govs, "wards": wards, "parties": parties},
    )


def polling_result(request, pul_id):
    results = AnnouncedPuResults.objects.filter(polling_unit_uniqueid=pul_id).all()
    polling_unit = PollingUnit.objects.filter(uniqueid=pul_id).first()

    return render(
        request=request,
        template_name="pages/polling_result.html",
        context={"results": results, "polling_unit": polling_unit},
    )


def total_result(request, lga_id):
    polling_unit = PollingUnit.objects.filter(lga_id=lga_id).values_list(
        "uniqueid", flat=True
    )
    score = AnnouncedPuResults.objects.filter(
        polling_unit_uniqueid__in=list(polling_unit)
    ).aggregate(Sum("party_score"))

    local_gov = Lga.objects.filter(lga_id=lga_id).first()

    return render(
        request=request,
        template_name="pages/total_result.html",
        context={"score": score, "local_gov": local_gov},
    )
