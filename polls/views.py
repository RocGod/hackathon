from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question
from .forms import QueryClassifier
import tweepy
import time
from classifier.TweetClassifier import TweetClassifier


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self, **kwargs):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


def index_view(request):
    form = QueryClassifier()
    if request.method == 'GET':
        return render(request, 'polls/index.html', {
            'form': form,
        })
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = QueryClassifier(request.POST)
        if form.is_valid():
            account_id = form.cleaned_data['account_id']
            tweet_classifier = TweetClassifier()
            result = tweet_classifier.classify_account(account_id)
            try:
                return render(request, 'polls/index.html', {
                    'tweets': result,
                    'form': form
                })
            except:
                print "error"



def ResultClasifyView(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = QueryClassifier(request.POST)
        # if form.is_valid():
        #     account_id = form.cleaned_data['account_id']
        #     try:
        #         user_timeline = api.user_timeline(account_id, count=100)
        #         return render(request, 'polls/resultclassifier.html', {'tweets': user_timeline})
        #     except:
        #         user_timeline = "broken"
        #     return HttpResponse("You're looking at question1<br> %s" % (account_id))
    return HttpResponse("You're looking at question2<br>")


    # return HttpResponse("You're looking at question %s. <br> %s" % (user_id, string_tweets))

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]
