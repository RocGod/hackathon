from django import forms


class QueryClassifier(forms.Form):
    account_id = forms.CharField(required=True)
