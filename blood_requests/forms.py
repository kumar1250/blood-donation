from django import forms
from .models import BloodRequest, DonorLocation

# ------------------------
# Blood Request Form
# ------------------------
class BloodRequestForm(forms.ModelForm):
    class Meta:
        model = BloodRequest
        fields = [
            "name", "email", "phone", "address",
            "blood_group", "emergency", "reason",
            "requester_lat", "requester_lng"
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "blood_group": forms.Select(attrs={"class": "form-select"}),
            "emergency": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "reason": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            # Lat/Lng hidden, will be set by JS
            "requester_lat": forms.HiddenInput(),
            "requester_lng": forms.HiddenInput(),
        }

# ------------------------
# OTP Form
# ------------------------
class OTPForm(forms.Form):
    otp = forms.CharField(
        max_length=6,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter OTP"
        })
    )

# ------------------------
# Share Donor Location Form
# ------------------------
class ShareLocationForm(forms.ModelForm):
    class Meta:
        model = DonorLocation
        fields = ["lat", "lng"]
        widgets = {
            "lat": forms.HiddenInput(),  # hidden, updated by JS
            "lng": forms.HiddenInput(),
        }
