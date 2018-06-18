from django import forms
from myapp.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('product', 'client', 'num_unit')
        widgets = {
            'client': forms.RadioSelect(attrs={'class': 'radio'}),
        }
        labels = {
            'client': "Client Name",
            'num_unit': "Quantity",
        }


class InterestForm(forms.Form):

    CHOICES = (('1', 'Yes',), ('0', 'No',))
    interested = forms.CharField(widget=forms.RadioSelect(choices=CHOICES))
    quantity = forms.IntegerField(initial=1)
    comments = forms.CharField(widget=forms.Textarea(), required=False, label="Additional Comments")

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'required': True, 'class': 'validate', 'placeholder': 'Username'}), label="")
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'required': True, 'class': 'validate input-field', 'placeholder': 'Password'}),
        label="")

class UploadImageForm(forms.Form):
    title = forms.CharField( max_length=100)
    imgfile = forms.ImageField()
