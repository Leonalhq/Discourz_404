from django.shortcuts import render
from discourz_app.models import Account, PollTopic, Debates, PastDebates, Chat
from discourz_app.forms import CreatePoll, CreateDebate, whichVote

from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.utils import timezone

from django import forms
from discourz.forms import SignUpForm
from discourz.forms import EditProfileForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from django.views.decorators.csrf import csrf_exempt,csrf_protect

def index(request):
    topics = PollTopic.objects.order_by("-date")[:5]
    titles = []
    images = [] 
    owners = []
    numVotes = []
    uuids = []
    for topic in topics:
        titles.append(topic.title)
        images.append(topic.img)
        owners.append(topic.owner.user.username)
        uuids.append(topic.id)
        numVotes.append(len(topic.voters.split(',')) - 1)

    polls = zip(uuids, titles, numVotes)
    polls1 = zip(images, titles, owners)
    polls2 = uuids

    context = {
        'polls': polls,
        'polls1': polls1,
        'polls2': polls2
    }
    return render(request, 'index.html', context=context)

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
        voters = topic.voters
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

    voters += request.user.username + ":" + str(index) + ","
    topic.voters = voters
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

def poll_deleting(request, uuid):
    topic = PollTopic.objects.get(id=uuid)
    topic.delete()
    return redirect('poll_home')

def poll(request, uuid):
    #topic = PollTopic.objects.all()
    #options = topic[0].options.split(',')
    #votes = topic[0].votes.split(',')
    try:
        topic = PollTopic.objects.get(id=uuid)
        options = topic.options.split(',')
        votes = topic.votes.split(',')
        voters = topic.voters.split(',')
    except PollTopic.DoesNotExist:
        raise Http404('Topic does not exist')

    voted = False
    voters = voters[:-1]
    for voter in voters:
        if request.user.username == voter.split(':')[0]:
            voted = True
            break

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
        'voted': voted,
    }

    return render(request, 'poll.html', context=context)

def edit_profile(request, username):
    account = request.user.account
    context = {
        'username': account.user.username,
        'email': account.user.email,
        'bio' : account.bio,
        'img' : account.img,
    }
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user = account.user
            user.first_name = form.cleaned_data.get('firstName')
            user.last_name = form.cleaned_data.get('lastName')
            user.account.bio = form.cleaned_data.get('userBio')
            myTags = ((form.cleaned_data.get('userTags')).lower()).replace(" ","")
            myTags = myTags.split(",")
            user.account.set_tags(myTags)
            if 'profile_img' in request.FILES:
                form.profile_img = request.FILES['profile_img']
                user.account.img = form.cleaned_data.get('profile_img')
            if form.cleaned_data.get('email') != "":
                user.email = form.cleaned_data.get('email')
            user.save()
            return redirect('profile')
        else:
            print(form.errors)
    else:
        user = account.user
        initialValues={
        'username':user.username,
        'firstName':user.first_name,
        'lastName':user.last_name,
        'userBio':user.account.bio,
        'email':user.email,
        'userTags':user.account.get_tags()
        }
        form = EditProfileForm(initial=initialValues)
    context.update({"form":form})
    return render(request, 'edit_profile.html', context=context)
    
def aboutus(request):
    return render(request, 'about_us.html',)

def discussion(request):
    return render(request, 'discussion.html')

def debate(request):
    debates = Debates.objects.order_by('-date')[:10]
    uuids = []
    positions = []
    categories = []
    topics = []
    initialUsers = []
    isDebateOpen = []

    for debate in debates:
        uuids.append(debate.id)
        positions.append(debate.position)
        categories.append(debate.category)
        topics.append(debate.topic)
        initialUsers.append(debate.initial_user)
        isDebateOpen.append(debate.isOpen)

    viewDebates = zip(uuids, positions, categories, topics, initialUsers, isDebateOpen)

    context = {
        'viewDebates' : viewDebates
    }

    pastDebates = PastDebates.objects.order_by('-date')[:10]
    pastUuids = []
    pastUser1 = []
    pastUser2 = []
    pastUser1Position = []
    pastUser2Position = []
    pastUser1Votes = []
    pastUser2Votes = []
    pastCategories = []
    pastTopics = []

    for pastDebate in pastDebates:
        pastUuids.append(pastDebate.id)
        pastUser1.append(pastDebate.user1)
        pastUser2.append(pastDebate.user2)
        pastUser1Position.append(pastDebate.user1Position)
        pastUser2Position.append(pastDebate.user2Position)
        pastUser1Votes.append(pastDebate.user1votes)
        pastUser2Votes.append(pastDebate.user2votes)
        pastCategories.append(pastDebate.category)
        pastTopics.append(pastDebate.topic)
    
    viewPast = zip(pastUuids, pastUser1, pastUser2, pastUser1Position, pastUser2Position, pastUser1Votes, pastUser2Votes, pastCategories, pastTopics)

    context = {
        'viewDebates' : viewDebates,
        'viewPast': viewPast
    }

    return render(request, 'debate_home.html', context=context)


def debateChat(request, uuid):
    otherUsername = ''
    topic = ''
    try:
        debateTopic = Debates.objects.get(id=uuid)
        otherUsername = debateTopic.initial_user
        topic = debateTopic.topic
    except Debates.DoesNotExist:
        raise Http404('Topic does not exist')

    context = {
        'otherUsername': otherUsername,
        'topic': topic
    }

    return render(request, 'debate.html', context=context)

@csrf_exempt #This skips csrf validation. Use csrf_protect to have validationxs
def debate_create(request):
    if request.method == 'POST':
        debate_form = CreateDebate(request.POST, request.FILES)
        title = debate_form.data['title']
        category = debate_form.data['category']
        position = debate_form.data['position']
        user1 = request.user.username
        newDebate = Debates(topic=title, isOpen=True, position=position, category=category, initial_user=user1)
        newDebate.save()
        return HttpResponseRedirect("/discourz/debate")
    else:
        return render(request, 'debate_create.html')

@csrf_exempt
def pastChat(request, uuid):
    if request.method == 'POST':
        vote_form = whichVote(request.POST, request.FILES)
        pastDebate = PastDebates.objects.get(id=uuid)
        numUser = vote_form.data['vote']
        numUser = numUser[:1]
        if numUser == '1':
            pastDebate.user1votes = pastDebate.user1votes + 1
            pastDebate.save()
        else:
            pastDebate.user2votes = pastDebate.user2votes + 1
            pastDebate.save()
        return HttpResponseRedirect("/discourz/debate")
    else:
        pastDebate = []
        otherUsername = ''
        topic = ''
        user1 = ''
        user2 = ''
        user1votes = 0
        user2votes = 0
        category = ''
        try:
            pastDebate = PastDebates.objects.get(id=uuid)
            topic = pastDebate.topic
            user1 = pastDebate.user1
            user2 = pastDebate.user2
            user1votes = pastDebate.user1votes
            user2votes = pastDebate.user2votes
            category = pastDebate.category 
        except PastDebates.DoesNotExist:
            raise Http404('Topic does not exist')
        
        chatList = Chat.objects.filter(debates=pastDebate)

        usernames = []
        messages = []

        for chat in chatList:
            usernames.append(chat.username)
            messages.append(chat.message)

        chats = zip(usernames, messages)

        context = {
            'chats': chats,
            'topic': topic,
            'user1': user1,
            'user2': user2,
            'user1votes': user1votes,
            'user2votes': user2votes,
            'category': category,
            'uuid': uuid
        }
        return render(request, 'pastChatTemplate.html', context=context)

def getBestOptionPoll(topic):
    votes = topic.votes.split(',')
    options = topic.options.split(',')

    total = 0
    for vote in votes:
        total += int(vote)

    if (total == 0):
        return [], 0
    
    max_val = max(votes)
    percentage = int(round(int(max_val)/total*100))

    # case more than one option have same votes
    option = []
    i = 0
    for val in votes:
        if val == max_val:
            option.append(options[i])
        i = i + 1
    return option, percentage

def profile(request):
    account = request.user.account
    topics = PollTopic.objects.filter(owner=account).order_by("-date")[:10]
    num_own_polls = topics.count()
    
    titles = []
    images = [] 
    owners = []
    uuids = []
    voters =[]
    dates = []
    bestPerc = []
    bestOpt = []
    
    for topic in topics:
        titles.append(topic.title)
        images.append(topic.img)
        owners.append(topic.owner.user.username)
        uuids.append(topic.id)
        voters.append(len(topic.voters.split(','))-1)
        dates.append(topic.date)
        option, percentage= getBestOptionPoll(topic)
        bestOpt.append(option)
        bestPerc.append(percentage)
        

    polls = zip(uuids, titles, images, owners, voters, dates,bestOpt,bestPerc)
    context = {
        'username': account.user.username,
        'firstname': account.user.first_name,
        'lastname': account.user.last_name,
        'email': account.user.email,
        'bio' : account.bio,
        'img' : account.img,
        'polls': polls,
        'num_own_polls': num_own_polls,
        'now': timezone.now(),
        'tagList':account.get_tag_list(),
    }

    return render(request, 'profile.html', context=context)

def registration(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            num_results = User.objects.filter(email = form.cleaned_data.get('email')).count()
            if num_results == 0:
                user = form.save()
                user.refresh_from_db()  # load the profile instance created by the signal
                user.email = form.cleaned_data.get('email')
                user.account.img = 'static/avatar/man1.png'
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
    