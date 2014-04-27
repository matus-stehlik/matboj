from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView
from django import forms
from matboje.models import Matboj, MatbojCompetitors
import math

class IndexView(ListView):
    template_name = 'matboje/index.html'
    context_object_name = 'matboje_list'

    def get_queryset(self):
        """Return the last five published polls."""
        return Matboj.objects.order_by('-date').all()

class MatbojDetailView(DetailView):
    model = Matboj
    template_name = 'matboje/detail.html'
    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        matboj = get_object_or_404(Matboj, id=self.kwargs['pk'])
        context['form']=MatchForm(matboj)
 
class MatchForm(forms.Form,MatbojDetailView):
        
        def get_competitors_list(self):
            matboj = Matboj.objects.filter(id=self.kwargs['pk'])
            competitors_list = sorted(list(matboj.matbojcompetitors_set.all()),
                key=lambda x: x.ranking, reverse=True)
            return competitors_list
        
        winner = forms.ChoiceField(
            competitors_list=get_competitors_list(self) )
        loser = forms.ChoiceField(
            competitors_list=get_competitors_list(self) )
            


def SubmitMatch(request):

    if request.method == 'POST':
        form = MatchForm(request.POST) 
        if form.is_valid():
            winner = form.cleaned_data['winner']
            loser = form.cleaned_data['loser']
            winner.rank = w.rank - math.floor(0.1*l.rank)
            loser.rank = l.rank - math.floor(0.1*l.rank)
            winner.save()
            loser.save()
    else:
        form = MatchForm() # An unbound form

    return render(request, 'detail.html', {
        'form': form,})
    #return HttpResponseRedirect(reverse('polls:detail', args=(w.matboj.id)))
    

class ResultsView(DetailView):
    model = Matboj
    template_name = 'matboje/results.html'


