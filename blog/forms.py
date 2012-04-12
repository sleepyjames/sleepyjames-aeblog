from django import forms

from models import Post

class PostForm(forms.Form):
    title = forms.CharField()
    is_published = forms.BooleanField(required=False)
    content = forms.CharField(widget=forms.widgets.Textarea)
    post_date = forms.DateField()

    class Media:
        css = {
            'all': ('js/jqueryui/jquery-ui-1.8.18.custom.css',),
        }
        js = (
            'js/forms.js',
            'js/tiny_mce/tiny_mce.js',
            'js/tiny_mce_config.js',
        )

    def clean(self):
        data = self.cleaned_data
        slug = data.get('slug', '')
        return data


