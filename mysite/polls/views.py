import json

from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(
            publish_date__lte=timezone.now()
        ).order_by('-publish_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Question.objects.filter(publish_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        if not request.POST['name']:
            context = {'question': question, 'error_message': "You didn't enter your name."}
            return render(request, 'polls/detail.html', context)
    except(KeyError, Choice.DoesNotExist):
        context = {'question': question, 'error_message': "You didn't select a choice."}
        return render(request, 'polls/detail.html', context)
    else:
        selected_choice.votes = F('votes') + 1
        selected_choice.voter_set.create(voter_name=request.POST['name'])
        selected_choice.save()
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def get_voters(request):
    choice_id = request.GET.get('choice_id', None)
    choice = Choice.objects.get(pk=choice_id)
    voters = json.dumps(list(choice.voter_set.all()), default=convert_to_dict, indent=4)
    data = {
        'voters_list': voters,
    }
    return JsonResponse(data)


def convert_to_dict(obj):
    obj_dict = {
        "voter_name": obj.voter_name
    }
    return obj_dict
