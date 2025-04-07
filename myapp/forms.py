# myapp/forms.py
from django import forms
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
from .models import User, Patient, Doctor, Appointment, MedicalRecord, NutritionLog


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


class PatientSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_patient = True
        if commit:
            user.save()
        return user


class DoctorSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_doctor = True
        if commit:
            user.save()
        return user


class PatientProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )

    class Meta:
        model = Patient
        fields = [
            'phone_number',
            'address',
            'date_of_birth',
            'emergency_contact_name',
            'emergency_contact_phone',
            'due_date',
            'blood_group'
        ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }


class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = [
            'phone_number',
            'specialization',
            'license_number',
            'years_of_experience'
        ]


# forms.py - update AppointmentForm
class AppointmentForm(forms.ModelForm):
    # Split date and time for better UX
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )
    time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        required=True
    )

    class Meta:
        model = Appointment
        fields = ['doctor', 'appointment_type', 'is_virtual', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter doctors to show only verified ones
        self.fields['doctor'].queryset = Doctor.objects.filter(is_verified=True)

        # If we're editing an existing appointment, set the initial date and time
        if self.instance.pk:
            self.fields['date'].initial = self.instance.appointment_date.date()
            self.fields['time'].initial = self.instance.appointment_date.time()

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')

        # Debug print statements (you can remove these later)
        print(f"Date: {date}, Time: {time}")

        # Combine date and time into appointment_date
        if date and time:
            try:
                # Explicitly combine and assign to appointment_date
                appointment_date = datetime.combine(date, time)
                cleaned_data['appointment_date'] = appointment_date
                print(f"Combined datetime: {appointment_date}")
            except Exception as e:
                print(f"Error combining date and time: {e}")
                raise forms.ValidationError("There was an error processing the date and time.")
        else:
            raise forms.ValidationError("Both date and time are required.")

        return cleaned_data


class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['weight', 'blood_pressure', 'symptoms', 'diagnosis', 'treatment', 'notes']
        widgets = {
            'symptoms': forms.Textarea(attrs={'rows': 3}),
            'diagnosis': forms.Textarea(attrs={'rows': 3}),
            'treatment': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class NutritionLogForm(forms.ModelForm):
    class Meta:
        model = NutritionLog
        fields = ['calories', 'protein', 'carbs', 'fats', 'iron', 'calcium', 'folate']
        widgets = {
            'calories': forms.NumberInput(attrs={'class': 'form-control'}),
            'protein': forms.NumberInput(attrs={'class': 'form-control'}),
            'carbs': forms.NumberInput(attrs={'class': 'form-control'}),
            'fats': forms.NumberInput(attrs={'class': 'form-control'}),
            'iron': forms.NumberInput(attrs={'class': 'form-control'}),
            'calcium': forms.NumberInput(attrs={'class': 'form-control'}),
            'folate': forms.NumberInput(attrs={'class': 'form-control'}),
        }