from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .models import Leader, Profile, Tag,Rating
from .forms import LeaderForm, TagForm,RateForm


# index page
def index(request):
    all_leaders=Leader.objects.all()
    print(len(all_leaders))
    return render(request, 'index.html',{'leaders':all_leaders})

# project


@login_required(login_url='/accounts/login')
def submit_leader(request):
    user = request.user

    new_leader_form = LeaderForm(request.POST, request.FILES)
    new_tag_form = TagForm(request.POST)
    if user.is_authenticated and new_leader_form.is_valid():
        leader = new_leader_form.save(commit=False)
        leader.user_id = user.id
        leader.save()
        new_leader_form.save_m2m()
        return redirect(index)
    else:
        new_leader_form = LeaderForm(request.POST)
        new_tag_form = TagForm(request.POST)

    return render(request, 'new_leader.html', {"new_leader_form": new_leader_form, "new_tag_form": new_tag_form})


@login_required(login_url="/accounts/login")
def create_leader_tag(request):
    user = request.user
    new_tag_form = TagForm(request.POST)

    if user.is_authenticated and new_tag_form.is_valid():
        tag = new_tag_form.save(commit=False)
        tag.user = user
        tag.save()
        return redirect(submit_leader)
    else:
        new_tag_form = TagForm(request.POST)
    return render(request, 'new_tag.html', {"new_tag_form": new_tag_form})


@login_required(login_url="/accounts/login")
def create_tag(request):
    user = request.user
    new_tag_form = TagForm(request.POST)

    if user.is_authenticated and new_tag_form.is_valid():
        tag = new_tag_form.save(commit=False)
        tag.user = user
        tag.save()
        return redirect(index)
    else:
        new_tag_form = TagForm(request.POST)
    return render(request, 'new_tag.html', {"new_tag_form": new_tag_form})

@login_required(login_url='/accounts/login')
def leader(request,leader_id):
    leader=Leader.get_single_leader(leader_id)
    print(leader)
    form=RateForm()
    if request.method == 'POST':
        form=RateForm(request.POST)
        if form.is_valid():
            print ("hkkkjkj")
            data = form.cleaned_data
            new_rating=Rating(user=request.user,leader=leader,leadership=data['leadership'],publicity=data['publicity'],integrity=data['integrity'])
            new_rating.save_rating()
            # print(data['content'])
    average_ratings = Rating.get_average_rating(leader_id)
    print(average_ratings)
    if average_ratings==[]:
        av_leadership=0
        av_publicity=0
        av_integrity=0
    else:
        av_leadership = average_ratings[0]
        av_publicity = average_ratings[1]
        av_integrity = average_ratings[2]
    return render(request,'leader.html',{'leader':leader,'form':form,'av_leadership':av_leadership, 'av_publicity':av_publicity, 'av_integrity':av_integrity })
def search(request):
    if 'search' in request.GET and not request.GET['search']==None:
        print('<><><><><><.jhjhhjhj')
        search_term = request.GET['search']
        print(search_term)
        leaders = Leader.objects.filter(title__icontains=search_term)
        print(projects)
    return render(request,'search.html',{"leaders":leaders})
