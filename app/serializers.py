from django import forms
from .models import Department, Post, PostImage
import datetime
from django.core.exceptions import ValidationError
from django.db import models
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'is_active',' created_by']

    # widgets = {
    #     'images': forms.ClearableFileInput(attrs={'multiple': True}),
    # }

class PostForm(forms.ModelForm):
    def clean_schedule_date(self):
        schedule_date = self.cleaned_data.get('schedule_date')
        if schedule_date and schedule_date < datetime.datetime.now():
            raise ValidationError("The date cannot be in the past!")
        return schedule_date

    class Meta:
        model = Post
        fields = ['title', 'description', 'image', 'schedule_date',  'processed_date', 'is_promoted','department']


class PostImageForm(forms.ModelForm):
    class Meta:
        model = PostImage
        fields = ['image']


