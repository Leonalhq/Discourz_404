from django.shortcuts import render
from discourz_app.models import Account, PollTopic
from discourz_app.forms import CreatePoll

from django.http import HttpResponseRedirect
from django.shortcuts import redirect

from django import forms
from discourz.forms import SignUpForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

def index(request):
    return render(request, 'index.html')

def poll_home(request):
    topics = PollTopic.objects.order_by("-date")[:10]
    titles = []
    images = [] 
    owners = []
    uuids = []
    for topic in topics:
        titles.append(topic.title)
        images.append(topic.img)
        owners.append(topic.owner.user.username)
        uuids.append(topic.id)

    polls = zip(uuids, titles, images, owners)

    context = {
        'polls': polls
    }

    return render(request, 'poll_home.html', context=context)



def poll_create(request):

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        poll_form = CreatePoll(request.POST, request.FILES)

        # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
        title = poll_form.data['poll_title']
        options = []
        for i in range(1, 13):
            if poll_form.data['poll_op' + str(i)] == ' ':
                break
            options.append(poll_form.data['poll_op' + str(i)].strip())
        string = ""
        votes = ""
        for op in options:
            string += op + ","
            votes += "0,"

        string = string[:-1]
        votes = votes[:-1]

        #img = poll_form.data['poll_img']
        owner = request.user.account

        newPoll = PollTopic(title=title, options=string, votes=votes, owner=owner)
        newPoll.save()
        addedPoll = PollTopic.objects.order_by('-date')[0]
        addedPoll.img = request.FILES['poll_img']
        addedPoll.save()

        # redirect to a new URL:
        return redirect('poll_home')

    else:
        poll_form = CreatePoll(initial={'poll_op1':' ', 'poll_op2':' ', 'poll_op3':' ', 'poll_op4':' ', 'poll_op5':' ', 'poll_op6':' ',
        'poll_op7':' ', 'poll_op8':' ', 'poll_op9':' ', 'poll_op10':' ', 'poll_op11':' ', 'poll_op12':' '})

    context = {
        'form': poll_form,
    }

    return render(request, 'poll_create.html', context)
    
def poll_voting(request, uuid, vote):
    try:
        topic = PollTopic.objects.get(id=uuid)
        options = topic.options.split(',')
        votes = topic.votes.split(',')
    except PollTopic.DoesNotExist:
        raise Http404('Topic does not exist')

    
    vote = vote.replace("_", " ")
    index = -1
    i = -1
    for option in options:
        i += 1
        if option == vote:
            index = i
            break

    print(index)
    votes[index] = str(int(votes[index]) + 1)
    print(votes[index])
    string = ""
    i = 0
    for vote in votes:
        string += vote[i] + ","

    print(string)
    string = string[:-1]
    topic.votes = string
    topic.save()

    return redirect('poll', uuid=uuid)

def poll(request, uuid):
    #topic = PollTopic.objects.all()
    #options = topic[0].options.split(',')
    #votes = topic[0].votes.split(',')
    try:
        topic = PollTopic.objects.get(id=uuid)
        options = topic.options.split(',')
        votes = topic.votes.split(',')
    except PollTopic.DoesNotExist:
        raise Http404('Topic does not exist')

    votesPercentage = []
    total = 0
    for vote in votes:
        total += int(vote)
    
    if (total != 0):
        for vote in votes:
            votesPercentage.append(int(round(int(vote)/total*100)))
    else:
        for vote in votes:
            votesPercentage.append(0)
    

    #owner = topic[0].owner.username
    owner = topic.owner.user.username
    poll_info = zip(options, votesPercentage)

    context = {
        'title': topic.title,
        'owner': owner,
        'options': options,
        'votes': poll_info,
        'uuid': uuid,
    }

    return render(request, 'poll.html', context=context)

    
def discussion(request):
    return render(request, 'discussion.html')

def debate(request):
    return render(request, 'debate.html')


def profile(request):
    account = request.user.account

    context = {
        'username': account.user.username,
        'email': account.user.email,
        'bio' : account.bio,
        'img' : account.img,
    }

    return render(request, 'profile.html', context=context)

def registration(request):
    print('yo')
    if request.method == 'POST':
        print('yo')
        form = SignUpForm(request.POST, request.FILES)
        print('yo')
        print(form.data['email'])

        if form.is_valid():
            print('yo')
            num_results = User.objects.filter(email = form.cleaned_data.get('email')).count()
            if num_results == 0:
                user = form.save()
                user.refresh_from_db()  # load the profile instance created by the signal
                user.email = form.cleaned_data.get('email')
                user.account.img = form.cleaned_data.get('profile_img')
                user.account.bio = form.cleaned_data.get('userBio')
                user.save()
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=user.username, password=raw_password, )
                login(request, user)
            else: 
                raise forms.ValidationError("This email address is in use.")
            return redirect('profile')
        else:
            print(form.errors)
    else:
        form = SignUpForm()
    return render(request, 'registration/registration.html', {'form': form})
    