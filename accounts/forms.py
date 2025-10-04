from django import forms
from .models import User

# ------------------------------
# User Registration Form
# ------------------------------
class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter password',
            'autocomplete': 'new-password'
        }),
        label="Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm password',
            'autocomplete': 'new-password'
        }),
        label="Confirm Password"
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'email', 'blood_group', 'phone', 'address']
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Enter username',
                'autocomplete': 'off',
                'pattern': '^[A-Za-z0-9_]+$',
                'title': 'Only letters, numbers, and underscores are allowed. No spaces.'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter email',
                'autocomplete': 'off'
            }),
            'blood_group': forms.Select(attrs={'class': 'form-select'}),
            'phone': forms.TextInput(attrs={
                'placeholder': '+91XXXXXXXXXX',
                'pattern': '^[0-9]{10,15}$',
                'title': 'Enter a valid phone number (10–15 digits)',
                'autocomplete': 'off'
            }),
            'address': forms.Textarea(attrs={
                'placeholder': 'Enter your address',
                'rows': 3,
                'autocomplete': 'off'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Clear initial values for fresh form
        for field in self.fields.values():
            field.initial = ''
            if isinstance(field.widget, (forms.TextInput, forms.PasswordInput)):
                field.widget.attrs['value'] = ''

    def clean_username(self):
        username = self.cleaned_data.get("username", "")
        if " " in username:
            raise forms.ValidationError("Username cannot contain spaces.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


# ------------------------------
# OTP Verification Form
# ------------------------------
class OTPForm(forms.Form):
    otp1 = forms.CharField(
        max_length=1,
        required=True,
        widget=forms.TextInput(attrs={'autocomplete':'off', 'class':'otp-box'})
    )
    otp2 = forms.CharField(
        max_length=1,
        required=True,
        widget=forms.TextInput(attrs={'autocomplete':'off', 'class':'otp-box'})
    )
    otp3 = forms.CharField(
        max_length=1,
        required=True,
        widget=forms.TextInput(attrs={'autocomplete':'off', 'class':'otp-box'})
    )
    otp4 = forms.CharField(
        max_length=1,
        required=True,
        widget=forms.TextInput(attrs={'autocomplete':'off', 'class':'otp-box'})
    )

    def clean(self):
        cleaned_data = super().clean()
        otp = ''.join([
            cleaned_data.get('otp1', ''),
            cleaned_data.get('otp2', ''),
            cleaned_data.get('otp3', ''),
            cleaned_data.get('otp4', ''),
        ])
        if len(otp) != 4 or not otp.isdigit():
            raise forms.ValidationError("Please enter a valid 4-digit OTP.")
        cleaned_data['otp'] = otp  # Full OTP stored for easy access
        return cleaned_data
