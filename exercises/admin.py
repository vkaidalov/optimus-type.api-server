from django import forms
from django.contrib import admin

from .models import Exercise


class ExerciseModelForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Exercise
        fields = '__all__'


class ExerciseAdmin(admin.ModelAdmin):
    form = ExerciseModelForm


admin.site.register(Exercise, ExerciseAdmin)
