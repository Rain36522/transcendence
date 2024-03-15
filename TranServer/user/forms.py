from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')


class InvitationForm(forms.Form):
    username = forms.CharField(max_length=255)
    action = forms.CharField(widget=forms.HiddenInput(), initial='invite')

    def __init__(self, current_user, *args, **kwargs):
        self.current_user = current_user
        super(InvitationForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data['username']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("User with this username does not exist.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        if username and User.objects.filter(username=username).exists():
            invited_user = User.objects.get(username=username)
            if invited_user in self.current_user.invites.all():
                raise forms.ValidationError(f'User {username} is already invited.')
            elif invited_user in self.current_user.friends.all():
                raise forms.ValidationError(f'User {username} is already a friend.')
        if username == self.current_user.username:
            raise forms.ValidationError('You can not invite yourself')

        return cleaned_data

class AcceptInviteForm(forms.Form):
    accept_from = forms.ModelChoiceField(queryset=None)
    action = forms.CharField(widget=forms.HiddenInput(), initial='accept')

    class Meta:
        model = User
        fields = ['invites']
    def __init__(self, current_user, *args, **kwargs):
        super(AcceptInviteForm, self).__init__(*args, **kwargs)
        self.fields['accept_from'].queryset = current_user.invited_by.all()