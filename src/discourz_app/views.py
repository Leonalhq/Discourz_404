from django.shortcuts import render
from discourz_app.models import Account, PollTopic, Debates, PastDebates, Chat, Comment, Discussion
from discourz_app.forms import CreatePoll, CreateDebate, whichVote, CommentForm, CreateDiscussion
from django.views.generic import TemplateView
from django.utils.safestring import mark_safe
from itertools import chain
import json

from django.http import HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import redirect
from django.utils import timezone
from datetime import datetime

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
    tags = []
    for topic in topics:
        titles.append(topic.title)
        images.append(topic.img)
        owners.append(topic.owner.user.username)
        uuids.append(topic.id)
        tags.append(topic.get_tag_list())
    polls = zip(uuids, titles, images, owners, tags)

    topics_popular = PollTopic.objects.extra(select={'length':'Length(voters)'}).order_by('-length')[:10]
    titles2 = []
    images2 = [] 
    owners2 = []
    uuids2 = []
    tags2 = []
    #length2 = []
    for topic in topics_popular:
        titles2.append(topic.title)
        images2.append(topic.img)
        owners2.append(topic.owner.user.username)
        uuids2.append(topic.id)
        tags2.append(topic.get_tag_list())
        #length2.append(len(topic.voters))
    polls2 = zip(uuids2, titles2, images2, owners2, tags2)


    context = {
        'polls': polls,
        'polls2': polls2
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
        PollTags = (((poll_form.data['poll_tags']).lower()).replace(" ","")).split("#")
        #img = poll_form.data['poll_img']
        owner = request.user.account

        newPoll = PollTopic(title=title, options=string, votes=votes, owner=owner)
        newPoll.save()
        addedPoll = PollTopic.objects.order_by('-date')[0]
        addedPoll.img = request.FILES['poll_img']
        addedPoll.set_tags(PollTags)
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
        CommentList = Comment.objects.filter(Poll=topic)
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
        'CommentList':CommentList,
        'form':CommentForm(),
        'tags': topic.get_tags(),
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
            myTags = myTags.split("#")
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

def discussion_home(request):
    topics = Discussion.objects.order_by("-date")
    titles = []
    images = [] 
    owners = []
    uuids = []
    tags = []
    for topic in topics:
        titles.append(topic.title)
        images.append(topic.img)
        owners.append(topic.initial_user.username)
        uuids.append(topic.id)
        tags.append(topic.get_tag_list())

    discussions = zip(uuids, titles, images, owners, tags)

    context = {
        'discussions': discussions
    }


    return render(request, 'discussion_home.html', context=context)

def discussion_create(request):
    if request.method == 'POST':
        discussion_form = CreateDiscussion(request.POST, request.FILES)
        title = discussion_form.data['title']
        DiscussionTags = (((discussion_form.data['tags']).lower()).replace(" ","")).split("#")
        user1 = request.user
        newDiscussion = Discussion(title=title, isOpen=True, initial_user=user1)
        newDiscussion.set_tags(DiscussionTags)
        newDiscussion.img = request.FILES['dis_img']
        newDiscussion.save()
        uuid = str(newDiscussion.id)
        return render(request, 'discussion_home.html')
    else:
        form = CreateDiscussion()
        context={
            'form':form,
        }
        return render(request, 'discussion_create.html',context=context)

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
        categories.append(debate.get_tags())
        topics.append(debate.topic)
        initialUsers.append(debate.initial_user)
        isDebateOpen.append(debate.isOpen)

    viewDebates = zip(uuids, categories, topics, initialUsers, isDebateOpen)

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
        pastUser1Votes.append(pastDebate.user1votes)
        pastUser2Votes.append(pastDebate.user2votes)
        pastCategories.append(pastDebate.get_tag_list())
        pastTopics.append(pastDebate.topic)
    
    viewPast = zip(pastUuids, pastUser1, pastUser2, pastUser1Votes, pastUser2Votes, pastCategories, pastTopics)

    context = {
        'viewDebates' : viewDebates,
        'viewPast': viewPast
    }

    return render(request, 'debate_home.html', context=context)

def joinChat(request, uuid):
    try:
        debateTopic = Debates.objects.get(id=uuid) 
        if debateTopic.other_user != '' or request.user.username == debateTopic.initial_user:
            return HttpResponseRedirect("/discourz/debate")
        debateTopic.other_user = request.user.username
        debateTopic.isOpen = False
        debateTopic.save()
    except Debates.DoesNotExist as x:
        print(x)
    context = { 'id' : uuid }
    return render(request, 'joinChat.html', context=context)


def debateChat(request, uuid):
    try:
        debateTopic = Debates.objects.get(id=uuid)
        myUser = ''
        otherUser = ''
        if request.user.username == debateTopic.initial_user:
            myUser = debateTopic.initial_user
            otherUser = debateTopic.other_user
        else:
            myUser = debateTopic.other_user
            otherUser = debateTopic.initial_user
        topic = debateTopic.topic
        tagList = debateTopic.get_tag_list()
        context = {
            'id' : uuid,
            'myUser' : myUser,  
            'otherUsername' : otherUser,
            'topic' : topic,
            'tagList':tagList,
        }
        return render(request, 'debate.html', context=context)
    except Debates.DoesNotExist as x:
        print(x)
    return HttpResponseRedirect("/debate")

@csrf_exempt #This skips csrf validation. Use csrf_protect to have validationxs
def debate_create(request):
    if request.method == 'POST':
        debate_form = CreateDebate(request.POST, request.FILES)
        title = debate_form.data['title']
        if debate_form.data['category'] != "": DebateTags = (((debate_form.data['category']).lower()).replace(" ","")).split("#")
        else: DebateTags = ["General"]
        position = debate_form.data['position']
        user1 = request.user.username
        newDebate = Debates(topic=title, isOpen=True, initial_user=user1)
        newDebate.set_tags(DebateTags)
        newDebate.save()
        uuid = str(newDebate.id)
        return HttpResponseRedirect("/discourz/waitLobby/" + uuid)
    else:
        return render(request, 'debate_create.html')

def waitLobby(request, id):
    context = {
        'id' : id    
    }
    return render(request, 'waitLobby.html', context=context)

@csrf_exempt
def pastChat(request, uuid):
    if Debates.objects.filter(id=uuid):
        Debates.objects.filter(id=uuid).delete()
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
            tags = pastDebate.get_tag_list() 
        except PastDebates.DoesNotExist:
            raise Http404('Topic does not exist')
        

        usernames = []
        messages = []


        commentList = Comment.getDebateComments(pastDebate)

        context = {
            'topic': topic,
            'user1': user1,
            'user2': user2,
            'user1votes': user1votes,
            'user2votes': user2votes,
            'tags': tags,
            'uuid': uuid,
            'firebaseKey':pastDebate.firebaseKey,
            'CommentList':commentList,
            'form':CommentForm(),
        }

        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.cleaned_data['text']
                PollId = form.cleaned_data['PollId']
                Debate = (PastDebates.objects.filter(id = uuid))[0]
                newComment = Comment(text = comment, debate = Debate, user = request.user)
                newComment.save()
                return redirect('pastChat',uuid)

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
    commentListList=[]
    commentNums = []
    colorsPoll = []
    color = False

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
        commentListList.append(Comment.getPollComments(topic))
        commentNums.append(len(Comment.objects.filter(Poll=topic)))
        colorsPoll.append(color)
        if color:
            color = False
        else: color=True
        print(color)
        
    polls = zip(uuids, titles, images, owners, voters, dates,bestOpt,bestPerc,commentListList,commentNums,colorsPoll)

    discussionTopics = Discussion.objects.filter(initial_user=account.user).order_by("-date")
    num_own_discussion = discussionTopics.count()

    pastDebates = PastDebates.objects.filter(user1=account).order_by("-date")[:10]
    pastUuids = []
    pastUser1 = []
    pastUser2 = []
    pastUser1Position = []
    pastUser2Position = []
    pastUser1Votes = []
    pastUser2Votes = []
    pastCategories = []
    pastTopics = []
    pastDates = []
    colorsDebate = []
    count_winning = 0
    count_loss = 0
    
    for pastDebate in pastDebates:
        pastUuids.append(pastDebate.id)
        pastUser1.append(User.objects.filter(username=pastDebate.user1)[0])
        pastUser2.append(User.objects.filter(username=pastDebate.user2)[0])        
        pastUser1Votes.append(pastDebate.user1votes)
        pastUser2Votes.append(pastDebate.user2votes)
        if (pastDebate.user1votes > pastDebate.user2votes ):
            count_winning+=1
        else: count_loss+=1

        pastCategories.append(pastDebate.get_tag_list())
        pastTopics.append(pastDebate.topic)
        pastDates.append(pastDebate.date)
        colorsDebate.append(color)
        if color:
            color = False
        else: color = True
    
    viewPast = zip(pastUuids, pastUser1, pastUser2, pastUser1Votes, pastUser2Votes, pastCategories, pastTopics,pastDates,colorsDebate)
    
    context = {
        'username': account.user.username,
        'firstname': account.user.first_name,
        'lastname': account.user.last_name,
        'email': account.user.email,
        'bio' : account.bio,
        'img' : account.img,
        'polls': polls,
        'num_own_polls': num_own_polls,
        'num_own_discussion':num_own_discussion,
        'now': timezone.now(),
        'tagList':account.get_tag_list(),
        'form':CommentForm(),
        'count_winning':count_winning,
        'viewPast':viewPast,
        'count_loss':count_loss,
    }
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data['text']
            PollId = form.cleaned_data['PollId']
            Poll = (PollTopic.objects.filter(id = PollId))[0]
            newComment = Comment(text = comment, Poll = Poll, user = request.user)
            newComment.save()
            return redirect('profile')

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
    
class SearchView(TemplateView):
    template_name = 'search.html'

    def get(self, request, *args, **kwargs):
        q = request.GET.get('q', '')
        self.pollResults = PollTopic.objects.filter(tags__icontains=q)
        self.debateResults = PastDebates.objects.filter(tags__icontains=q)
        self.discussionResults = Discussion.objects.filter(tags__icontains=q)
        self.results = chain(self.debateResults, self.pollResults, self.discussionResults)
        self.key = q
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return super().get_context_data(results=self.results, key = self.key,discussionResults=self.discussionResults,
         debateResults=self.debateResults,pollResults=self.pollResults, **kwargs)

def create_past_debate(request):
    debateId = request.GET.get('id', None)
    firebaseKey = request.GET.get('firebaseKey', None)
    closedDebate = Debates.objects.filter(id=debateId)[0]
    pastDebate = closedDebate.closeDebate(firebaseKey)
    pastDebate.save()
    return JsonResponse({'dummyResponse':debateId})
    
def room(request, uuid,):
    discussion = Discussion.objects.filter(id=uuid)[0]
    context = {
        'room_name_json': mark_safe(json.dumps(uuid)),
        'user':request.user,
        'discussion':discussion,
        'tagList':discussion.get_tag_list(),
        'chatList':Chat.objects.filter(discussion=discussion),
    }
    return render(request, 'chat/room.html', context)

def post_comment(request):
    comment = request.GET.get('comment',None)
    userId = request.GET.get('user',None)
    user = User.objects.filter(id=userId)[0]
    Id = request.GET.get('id',None)
    data_type = request.GET.get('data_type',None)
    if(data_type == "PollTopic"): new_comment = Comment(user=user,Poll=(PollTopic.objects.filter(id=Id)[0]),text=comment)
    else: new_comment = Comment(user=user,debate=PastDebates.objects.filter(id=Id)[0],text=comment)
    date = datetime.now()
    formatedDate = date.strftime("%b. %d, %Y, %I:%M %p")
    new_comment.save()
    print(datetime.now())
    return JsonResponse({'username':user.username,'url':user.account.img.url,'date':formatedDate})

def new_message(request):
    message = request.GET.get('message',None)
    user = request.GET.get('user',None)
    user= User.objects.filter(username=user)[0]
    Id = request.GET.get('id',None)
    new_message = Chat(user=user,message=message,discussion=Discussion.objects.filter(id=Id)[0])
    new_message.save()
    return JsonResponse({'dummyResponse':Id})