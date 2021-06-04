from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import DateInput

from frontend_app.models import MessageUs, EventBook


class EventBookForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'text'}
        )
    )

    class Meta:
        model = EventBook
        fields = (
            'id',
            'my_venue',
            'date',
            'time',
            'message',
            'package',
            'user',
            'package_food',
            'people',
        )
        # widgets = {
        #     'date': DateInput(attrs={'class': 'datepicker'}),
        # }

    def clean(self):
        date = self.cleaned_data['date']
        time = self.cleaned_data['time']
        if EventBook.objects.filter(date=date, time=time, finished=False).count() > 0:
            raise ValidationError(
                "Sorry!! we will organize a event at that moment."
            )


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
        ]


class MessageUsForm(forms.ModelForm):
    class Meta:
        model = MessageUs
        fields = (
            'name',
            'email',
            'subject',
            'message',
        )
