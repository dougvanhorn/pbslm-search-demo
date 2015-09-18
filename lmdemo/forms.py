from django import forms



class SearchForm(forms.Form):
    query = forms.CharField(max_length=300)
    facet_grades = forms.CharField(required=False)
    facet_language = forms.CharField(required=False)
    facet_subject = forms.CharField(required=False)



class LoginBypassForm(forms.Form):
    """Capture login bypass values.
    """
    lm_url = forms.CharField(max_length=300)
    user_id = forms.CharField(max_length=100)
    email = forms.CharField(max_length=300)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    postal_code = forms.CharField(max_length=10, required=False)
    key = forms.CharField(max_length=300, required=False)
    endpoint = forms.CharField(max_length=300, required=False)

