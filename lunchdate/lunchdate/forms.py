from django import forms

class FriendForm(forms.Form):
    your_name = forms.IntegerField(label='Friend ID Number')