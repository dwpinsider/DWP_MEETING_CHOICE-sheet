from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.core.mail import send_mail
from .forms import VendorMeetingForm
from .models import VendorPlanner, VendorMeetingRegister

def vendor_meeting_register(request):
    vendors = VendorPlanner.objects.filter(is_active=True)
    if request.method == 'POST':
        form = VendorMeetingForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            company_name = form.cleaned_data['company_name']
            email = form.cleaned_data['email']
            vendors = form.cleaned_data['vendors']
            # Save the form data to the database
            meeting_register = VendorMeetingRegister(
                first_name=first_name,
                last_name=last_name,
                company_name=company_name,
                email=email
            )
            meeting_register.save()
            meeting_register.vendors.set(vendors)
            # # Send email to user
            # user_subject = 'Thank you for registering for the vendor meeting'
            # user_message = f'Dear {first_name},\n\nThank you for registering for the vendor meeting. Your selected vendors are: {", ".join([vendor.company_name for vendor in vendors])}.'
            # send_mail(user_subject, user_message, 'bhavya@qna-global.com', ['bhavya@qna-global.com'])
            # Send email to admin
            # admin_subject = 'New vendor meeting registration'
            # admin_message = f'A new vendor meeting registration has been submitted:\n\nFirst name: {first_name}\nLast name: {last_name}\nCompany name: {company_name}\nEmail: {email}\nSelected vendors: {", ".join([vendor.company_name for vendor in vendors])}'
            # send_mail(admin_subject, admin_message, 'bhavya@qna-global.com', ['bhavya@qna-global.com'])
            return render(request, 'success.html', {'selected_vendors': vendors})
    else:
        form = VendorMeetingForm()
    return render(request, 'vendor/vendor_meeting_register.html', {'form': form, 'vendors': vendors})
