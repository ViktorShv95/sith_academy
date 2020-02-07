from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, FormView
from django.views.generic.edit import FormMixin
from django.shortcuts import get_object_or_404

from .forms import RecruitForm, ChallengeForm, SithSelectForm, AddRecruit
from .models import Challenge, Recruit, Sith


class NewRecruitView(CreateView):
    form_class = RecruitForm
    template_name = 'new_recruit.html'

    def get_success_url(self):
        return reverse('challenge', kwargs={'recruit_id': self.object.pk,
                                                'order_id': self.object.planet_id})


class ChallengeView(FormView):
    form_class = ChallengeForm
    template_name = 'challenge.html'
    success_url = reverse_lazy('passed')

    def get_form_kwargs(self):
        recruit_id = self.kwargs.get('recruit_id', None)
        recruit = get_object_or_404(Recruit, id=recruit_id)
        order_id = self.kwargs.get('order_id', None)
        questions = get_object_or_404(Challenge, order_id=order_id).question.all()
        form_kwargs = super(ChallengeView, self).get_form_kwargs()
        form_kwargs['recruit'] = recruit
        form_kwargs['questions'] = [(q.id, q.text) for q in questions]
        return form_kwargs

    def form_valid(self, form):
        form.save()
        return super(ChallengeView, self).form_valid(form)


class SithSelectView(FormView):
    form_class = SithSelectForm
    template_name = 'select_sith.html'

    def form_valid(self, form):
        return redirect(reverse('sith', kwargs={'sith_id': form.cleaned_data['sith'].id}))


class SithView(ListView):
    template_name = 'sith_candidates.html'
    context_object_name = 'recruits'

    def get_queryset(self):
        sith_id = self.kwargs.get('sith_id', None)
        sith = get_object_or_404(Sith, id=sith_id)
        return Recruit.objects.filter(planet=sith.planet)

    def get_context_data(self, **kwargs):
        context = super(SithView, self).get_context_data(**kwargs)
        context['sith_id'] = self.kwargs['sith_id']
        return context


class RecruitToHandView(DetailView, FormMixin):
    model = Recruit
    template_name = 'recruit_detail.html'
    pk_url_kwarg = 'recruit_id'
    form_class = AddRecruit
    success_url = '/'

    def get_initial(self):
        recruit_id = self.kwargs.get('recruit_id', None)
        recruit = get_object_or_404(Recruit, id=recruit_id)
        sith_id = self.kwargs.get('sith_id', None)
        sith = get_object_or_404(Sith, id=sith_id)
        return {'recruit': recruit,
                'sith': sith}

    def form_valid(self, form):
        form.save()
        return super(RecruitToHandView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class SithListView(ListView):
    queryset = Sith.with_recruits.all()
    template_name = 'list_sith.html'
    context_object_name = 'siths'


class SithListMoreThanOneView(SithListView):
    queryset = Sith.with_recruits.more_than_one()
