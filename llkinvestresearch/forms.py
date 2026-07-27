from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=120)
    email = forms.EmailField()
    phone = forms.CharField(max_length=40, required=False)
    message = forms.CharField(
        min_length=10,
        max_length=3000,
        widget=forms.Textarea(attrs={"rows": 6}),
    )
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    def clean_website(self):
        website = self.cleaned_data.get("website")
        if website:
            raise forms.ValidationError("Invalid submission.")
        return website
