from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseServerError, HttpResponseRedirect
from .generation.Generator import Generator
from django.shortcuts import render
import yaml
from django.conf import settings
from .models import *
from django import views
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required

def register(request):
    registered = False
    if request.method == "POST":
        # TODO: stop using the default django form
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()

            profile = UserProfile(user=user, creation_time=timezone.now())
            profile.save()

            registered = True

            """
            # currently no email authentication, just login the user and redirect to index
            raw_pass = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_pass)
            login(request, user)

            return redirect('/')
            """
        else:
            pass # fall through to rerendering register html but now form.errors should be filled
            """
            for error in form.errors:
                print(error)
            """
    else:
        form = UserCreationForm()
    return render(request, 'survey/register.html', {'form': form, 'registered': registered})

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user:
            # TODO: check if user.is_active after setting up email confirmation
            login(request, user)
            
            # redirect to previous page if sent from @login_required
            # else redirect to index
            print(request.GET.get('next'))
            if request.GET.get('next', False):
                # TODO: fix, this redirecting doesn't seem to ever work
                redirect(request.GET.get('next'))
            else:
                return redirect('/')
        else:
            return render(request, 'survey/login.html', {'error': 'Invalid login details.'})
    else:
        return render(request, 'survey/login.html', {})

def user_logout(request):
    logout(request)

    return redirect('/')

def rules_view(request):
    # if request.method == "POST":
    #     print(request.POST.getlist('rule_name'))
    #     print(request.POST.getlist('rule_type'))
    #     rule_names = request.POST.getlist('rule_name')
    #     rule_types = request.POST.getlist('rule_type')
    #     for i,rule_name in enumerate(rule_names):
    #         RuleForm.objects.create(rule=rule_name,type=rule_types[i])
    #     # rule_name = request.POST.get('rule_name')
    #     # rule_type = request.POST.get('rule_type')
    #     # RuleForm.objects.create(rule=rule_name,type=rule_type)

    context = {}
    return render(request, "survey/rules.html", context)

class IndexView(views.generic.ListView):
    """
    Define homepage view, inheriting ListView class, which specifies a context variable.
    
    Note that login is required to view the items on the page.
    """
    
    template_name = 'survey/index.html'
    context_object_name = 'question_list'
    def get_queryset(self):
        """Override function in parent class and return all questions."""
        return Survey.objects.all().order_by('-pub_date')

# Start survey

# Collect user input from survey

# page for user survey creation <-- ??
    # get user defined rules back <-- ??


# Function to grab new scenario
    # start survey
    # collect user input from survey
    # page for user survey creation
    # get user defined rules back
    # function to grab new scenario
def load_survey(request,parent_id):
    # empty for now
    survey_info = {'parent_id':parent_id}

    # check = SurveyGenerator.objects.filter(rule_id = parent_id)
    # if not check: build_generator(RuleSet.objects.get(id=parent_id))
    
    
    
    # hardcoded!!!!!
    # grabbing default rule
    rule = RuleSet.objects.all()[0]
    check = SurveyGenerator.objects.filter(rule_id = rule.id)
    if not check: build_generator(rule)

    # survey_info.update(csrf(request))
    return render(request,'survey/survey-page.html',survey_info)

def get_scenario(request,parent_id):
    combos = 3

    if request.method == "POST":
        combos = request.POST['combo_count']

    # grabbing the sample json
    # story_gen = SurveyGenerator.objects.get(rule_id=parent_id)

    story_gen = SurveyGenerator.objects.get(rule_id=RuleSet.objects.all()[0].id)

    ss = story_gen.get_scenario()
    survey_information = json.dumps(ss)
    # For frontend, check the html to
    # see how the object is grabbed.
    return HttpResponse(content=survey_information)

    # once you navigate to http://127.0.0.1:8000/survey/loadsurvey
    # and press ctrl+shift+i and switch to console tab,
    # you can see the json object printed on the console

# @csrf_exempt
def submit_survey(request):
    if request.method == 'POST':
        # for now not storing scores
        print('scenario:',request.body[0])
        print('scores:',request.body[1])

        #Submits the json
        json_to_survey(request.body[0])
        # print(json.load(request.body))
        return redirect("survey:surveyresult")


def rules_explain(request):
    return render(request,'survey/rules_explain.html')
    
def survey_result(request):
    return render(request, 'survey/surveyresult.html')

# Django view to handle unknown paths
def unknown_path(request, random):
    return render(request, 'survey/unknownpath.html')

# Django endpoint to save rule to database from json post request body


def rules_save(request):

    if request.method != 'POST':
        return HttpResponse(status=400)
    json_data = json.loads(request.body)
    json_rules_string = ''
    try:
        json_rules_string = json.dumps(json_data['rules'])
    except KeyError:
        HttpResponseServerError('`rules` field not found in request body.')

    json_to_ruleset(json_rules_string)
    HttpResponse(status=201)
