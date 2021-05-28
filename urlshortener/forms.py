from django.forms import ModelForm

from urlshortener.models import Link


class LinkForm(ModelForm):
    class Meta:
        model = Link
        fields = ('full_path',)

    def save(self, commit=True):
        full_path = self.cleaned_data['full_path']
        link = Link.objects.filter(full_path=full_path)
        if link:
            return
        else:
            super().save(commit)
