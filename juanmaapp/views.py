from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import loader
from .models import Question,Formup
#from .forms import PostForm
#from .models import DyndbModel
#from .forms import DyndbModelForm
#from django.views.generic.edit import FormView

# Create your views here.
def index(request):
    return HttpResponse("Hello, JUANMA. You're at the juanmaapp index.")



#   def index(request):
#   latest_question_list = Question.objects.order_by('-pub_date')[:5]
#   template = loader.get_template('juanmaapp/index.html')
#   context = {
#       'latest_question_list': latest_question_list,
#   }
#   return HttpResponse(template.render(context, request))


#  def upload_detail(request, pk):
#          post = get_object_or_404(Formup, pk=pk)
#          return render(request, 'juanmaapp/uploadform_detail.html', {'post': post})





def upload(request):
#  latest_question_list = Question.objects.order_by('-pub_date')[:5]
#  template = loader.get_template('juanmaapp/uploadform.html')
#    form = PostForm() 
#  context = {
#      'latest_question_list': latest_question_list,
#  }
#    return render(request, 'juanmaapp/uploadform.html', {'form':form})
    return render(request, 'juanmaapp/uploadform.html')

#   if request.method == "POST":
#       form = PostForm(request.POST)
#       if form.is_valid():
#           post = form.save(commit=False)
#           post.author = request.user
#           post.published_date = timezone.now()
#           post.save()
#           return redirect('juanmaapp.views.upload_detail', pk=upload.pk)
#   else:
#       form = PostForm()
#   return render(request, 'juanmaapp/uploadform.html', {'form':form})

#def index(request):
#    latest_question_list = Question.objects.order_by('-pub_date')[:5]
#    output = ', '.join([q.question_text for q in latest_question_list])
#    return HttpResponse(output)


#def detail(request, question_id):
#    return HttpResponse("You're looking at question %s." % question_id)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'juanmaapp/detail.html', {'question': question})
#def results(request, question_id):
#    response = "You're looking at the results of question %s."
#    return HttpResponse(response % question_id)

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'juanmaapp/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'juanmaapp/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('juanmaapp:results', args=(question.id,)))

