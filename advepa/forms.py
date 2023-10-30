from django import forms
from users.models import *

# EXHIBITION FORMS
class ExhibitionForm(forms.ModelForm):
    name = forms.CharField(required=True)
    pavilions = forms.ModelMultipleChoiceField(queryset=Pavilion.objects.all(), required=False)

    class Meta:
        model = Exhibition
        fields = ('name',
                  'pavilions',
                  'info',
                  )

    def save(self, commit=True):
        exhibition = super().save(commit=False)
        if commit:
            exhibition.save()
        return exhibition


class EditExhibitionForm(forms.ModelForm):
    name = forms.CharField(required=True)
    pavilions = forms.ModelMultipleChoiceField(queryset=Pavilion.objects.all(), required=False)

    class Meta:
        model = Exhibition
        fields = ('name',
                  'pavilions',
                  'info',
                  )

    def save(self, commit=True):
        exhibition = super().save()
        return exhibition


# PAVILIONS FORMS
class PavilionForm(forms.ModelForm):
    name = forms.CharField(required=True)
    stands = forms.ModelMultipleChoiceField(queryset=Stand.objects.all(), required=False)

    class Meta:
        model = Pavilion
        fields = ('name',
                  'stands',
                  'info',
                  )

    def save(self, commit=True):
        pavilion = super().save(commit=False)
        if commit:
            pavilion.save()
        return pavilion


class EditPavilionForm(forms.ModelForm):
    name = forms.CharField(required=True)
    stands = forms.ModelMultipleChoiceField(queryset=Stand.objects.all(), required=False)

    class Meta:
        model = Pavilion
        fields = ('name',
                  'stands',
                  'info',
                  )

    def save(self, commit=True):
        pavilion = super().save()
        return pavilion


# STANDS FORMS
class StandForm(forms.ModelForm):
    name = forms.CharField(required=True)

    class Meta:
        model = Stand
        fields = ('name',
                  'info',
                  )

    def save(self, commit=True):
        stand = super().save(commit=False)
        if commit:
            stand.save()
        return stand


class EditStandForm(forms.ModelForm):
    name = forms.CharField(required=True)

    class Meta:
        model = Stand
        fields = ('name',
                  'info',
                  )

    def save(self, commit=True):
        stand = super().save()
        return stand
