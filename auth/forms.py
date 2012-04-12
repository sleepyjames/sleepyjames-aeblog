from django import forms


class UserForm(forms.Form):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    username = forms.CharField()

    password = forms.CharField(widget=forms.widgets.PasswordInput)
    password2 = forms.CharField(widget=forms.widgets.PasswordInput,
        help_text="Confirm Password")

    def clean(self):

        p1 = self.cleaned_data.get('password', None)
        p2 = self.cleaned_data.get('password2', None)

        if (p1 or p2) and p1 != p2:
            raise forms.ValidationError(u"Your passwords don't match")

        return self.cleaned_data


class UserEditForm(UserForm):
    password = forms.CharField(widget=forms.widgets.PasswordInput, required=False)
    password2 = forms.CharField(widget=forms.widgets.PasswordInput, required=False,
        help_text="Confirm Password")

