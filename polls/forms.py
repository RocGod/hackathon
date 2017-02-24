from django import forms


class QueryClassifier(forms.Form):
    account_id = forms.CharField(label="Account", required=True,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    tags = forms.CharField(label="Tags", required=True,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'tokenfield'}))
