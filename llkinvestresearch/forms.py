from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=120)
    email = forms.EmailField()
    phone = forms.CharField(max_length=40, required=False)
    message = forms.CharField(widget=forms.Textarea(attrs={"rows": 6}))
