from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Business, Advertisement
import africastalking

# Create your views here.
@csrf_exempt
def ussd_callback(request):
    session_id = request.POST.get("sessionId", "")
    phone_number = request.POST.get("phoneNumber", "")
    service_code = request.POST.get("serviceCode", "")
    text = request.POST.get("text", "")

    response = ""

    if text == "":
        response = "CON Welcome to BonyezaDeals!\n1. Browse Deals\n2. Post an Ad\n3. Contact Support"
    
    elif text == "1":
        response = "CON Select Category:\n1. Fashion\n2. Food\n3. Electronics"
    
    elif text in ["1*1", "1*2", "1*3"]:
        category_map = {"1*1": "fashion", "1*2": "food", "1*3": "electronics"}
        category = category_map[text]
        ads = Advertisement.objects.filter(category=category)
        
        if ads.exists():
            response = "CON Available Deals:\n"
            for i, ad in enumerate(ads, 1):
                response += f"{i}. {ad.text}\n"
            response += "Select a deal number to receive details via SMS."
        else:
            response = "END No deals available in this category."
    
    elif text.startswith("1*1*") or text.startswith("1*2*") or text.startswith("1*3*"):
        ad_number = int(text.split("*")[-1]) - 1
        category = text.split("*")[1]
        ad_list = Advertisement.objects.filter(category=category)

        if 0 <= ad_number < len(ad_list):
            ad = ad_list[ad_number]
            send_sms(phone_number, f"More details: {ad.text}")
            response = "END Details sent via SMS!"
        else:
            response = "END Invalid selection."
    
    elif text == "2":
        response = "CON Enter Ad Text (160 chars max):"
    
    elif text.startswith("2*"):
        ad_text = text.split("*", 1)[1]
        business, created = Business.objects.get_or_create(phone_number=phone_number)
        Advertisement.objects.create(business=business, text=ad_text, category="miscellaneous")
        response = "END Ad posted successfully!"

    elif text == "3":
        response = "END Contact Support at 0792-895-970."

    return HttpResponse(response, content_type="text/plain")


# Initialize Africa's Talking
username = "sandbox" 
api_key = "atsk_789a74e781c2d1f5dd34b928537db324c419fec8b9e6f5135d96dd67806ec5ff13cbd107"
africastalking.initialize(username, api_key)
sms = africastalking.SMS

def send_sms(phone_number, message):
    sms.send(message, [phone_number])

