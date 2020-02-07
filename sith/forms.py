from django import forms
from django.core.exceptions import PermissionDenied
from .models import Recruit, Answer, Sith
from django.db import IntegrityError


class RecruitForm(forms.ModelForm):
    class Meta:
        model = Recruit
        exclude = ('sith',)


class ChallengeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        recruit = kwargs.pop('recruit', None)
        questions = kwargs.pop('questions', None)
        super(ChallengeForm, self).__init__(*args, **kwargs)
        self.recruit = recruit
        for q in questions:
            self.fields[str(q[0])] = forms.BooleanField(label=q[1], required=False)

    def save(self):
        try:
            for k, v in self.cleaned_data.items():
                Answer.objects.create(question_id=k, recruit=self.recruit, answer=v)
        except IntegrityError:
            raise PermissionDenied


class SithSelectForm(forms.Form):
    sith = forms.ModelChoiceField(queryset=Sith.with_recruits.can_teach())


class AddRecruit(forms.Form):
    take = forms.BooleanField(label='Зачислить к себе Рукой Тени?', required=False)

    def save(self):
        if self.cleaned_data['take']:
            sith = self.initial['sith']
            recruit = self.initial['recruit']
            recruit.sith = sith
            recruit.save()
