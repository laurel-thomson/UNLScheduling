from django import forms
from django.forms import ModelForm
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
import logging

from .models import User, Room, RoomTerm, TimeSlot, StudentType, Student

logger = logging.getLogger(__name__)

class SignUpForm(ModelForm):
    first_name = forms.CharField(required=True, max_length=20, help_text='20 characters max.')
    last_name = forms.CharField(required=True, max_length=20, help_text='20 characters max.')
    student_type = forms.ModelChoiceField(
        queryset=StudentType.objects.all(),
        required=True
    )

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'student_type')

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        setattr(user, 'backend', 'cas.backends.CASBackend')
        user.save()
        s_type = self.cleaned_data.get('student_type')
        student = Student.objects.create(user_id=user, student_type = s_type)
        return user

class RoomForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(RoomForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = True

    class Meta:
        model = Room
        fields = ('name',)

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.DateInput):
    input_type = 'time'

class TermForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(TermForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = True

    class Meta:
        model = RoomTerm
        fields = ('name', 'available_until')
        widgets = {
            'available_until': DateInput(),
        }

class TimeSlotForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(TimeSlotForm, self).__init__(*args, **kwargs)
        self.fields['day'].required = True
    class Meta:
        model = TimeSlot
        fields = ('day', 'start_time', 'end_time',)
        widgets = {
            'start_time': TimeInput(),
            'end_time': TimeInput(),
        }

class UploadTimeSlotsForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={'accept':'text/csv'}))