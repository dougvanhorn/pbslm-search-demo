from django import forms



class SearchForm(forms.Form):
    query = forms.CharField(max_length=300)
    facet_grades = forms.CharField(required=False)
    facet_language = forms.CharField(required=False)
    facet_subject = forms.CharField(required=False)
