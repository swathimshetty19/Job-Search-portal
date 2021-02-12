from django.shortcuts import render
from django.shortcuts import render, redirect
from django.template import loader
from .forms import signupForm,loginForm,post_project_form
from .models import Login,Skills,Users,Projects
from django.template import RequestContext
from django.http import HttpResponse
import random

# Create your views here.
def home(request):
    return render(request, 'home.html', {})

def signup(request):
    if request.method == "POST": 
        form = signupForm(request.POST) 
        user=request.POST.get("name")
        ptype=request.POST.get("ptype")
        if form.is_valid() and ptype=="search": 
            form.save() 
            return redirect('skills',pk=user)
        elif form.is_valid() and ptype=="hire":
            form.save() 
            return redirect('post_project',pk=user)
    form = signupForm() 
    return render(request, 'signup.html', {'form': form})

def login(request):
    if request.method == "POST": 
        user=request.POST.get("name")
        password=request.POST.get("password")
        ptype=request.POST.get("ptype")
        user_list=Login.objects.values_list('name', 'password')
        if((user,password) in user_list and ptype=="hire"):
            print("yes")
            return redirect('post_project',pk=user)
        elif((user,password) in user_list and ptype=="search"):
            print("yes")
            return redirect('profile',pk=user)
        else:
            print("no")
            return render(request, 'invalid.html', {})
    form = loginForm() 
    return render(request, 'login.html', {'form': form})

def invalidview(request):
    return render(request, 'invalid.html', {})

def profile(request,pk):
    if(request.method=="POST"):
        #print("inside profile redirecting to post_project")
        return redirect('post_project')
    user_details=Users.objects.get(name=pk)
    sk=user_details.skills.split(',')
    return render(request, 'profile.html', {'user':pk,'user_details':user_details,'skills':sk})

def skills(request,pk):
    u=Users.objects.all().filter(name=pk)
    if(len(u)!=0):
        usr=Users.objects.get(name=pk)
        skills_so_far=usr.skills
        skills=skills_so_far.split(",")
    else:
        skills=[]
    return render(request, 'skills.html', {'pk': pk,'skills':skills})

def search_titles(request,pk):
    #print("inside search_titles")
    if(request.method=="POST"):
        search_text=request.POST.get('search_text')
        #print(search_text)
    else:
        search_text=''
    valid=Skills.objects.filter(skill__contains=search_text)
    #print(valid)
    return render(request,'ajax_search.html',{'skills':valid,'pk':pk})

def add_skill(request,pk,skill):
    #print("inside addskill")
    u=Users.objects.all().filter(name=pk)
    #print(u)
    if(len(u)==0):
        usr=Users(name=pk,experience=0,skills=skill)
        usr.save()
        #return render(request, 'skills.html', {'user': pk})
        return redirect('skills',pk=pk)
    else:
        usr=Users.objects.get(name=pk)
        skills_so_far=Users.objects.filter(name=pk).values('skills')
        #print(skills_so_far[0]['skills'])
        new_skill=skills_so_far[0]['skills']+","+skill
        #print(new_skill)
        usr.skills=new_skill
        #print("done")
        usr.save()
        #return render(request, 'skills.html', {'user': pk})
        return redirect('skills',pk=pk)

def post_project(request,pk):
    if request.method == "POST": 
            name = request.POST.get("name")
            #project_id=request.POST.get("project_id")
            project_id=random.randint(1,10000000)
            desc=request.POST.get("desc")
            #status=request.POST.get("status")
            skills=request.POST.get("skills")
           # mem_needed=request.POST.get("mem_needed")
            #min_payment=request.POST.get("min_payment")
            max_payment=request.POST.get("max_payment")
            days=request.POST.get("days")
            form=Projects(project_id=project_id,name=name,desc=desc,skills=skills,max_payment=max_payment,days=days,leader=pk)
            form.save()
    form = post_project_form()
    return render(request,'post_project.html',{'form': form,'pk':pk})

def other_details(request,pk):
    if request.method == "POST": 
        firstname=request.POST.get("firstname")
        lastname=request.POST.get("lastname")
        email=request.POST.get("email")
        phone=request.POST.get("phone")
        exp=request.POST.get("experience")
        usr=Users.objects.get(name=pk)
        usr.experience=exp
        usr.firstname=firstname
        usr.lastname=lastname
        usr.email=email
        usr.phone=phone
        usr.save()
        return redirect('profile',pk=pk)
    return render(request, 'other_details.html', {'pk': pk})

def myprojects(request,pk):
    #get the details of projects created by the user
    projects_own=Projects.objects.all().filter(leader=pk)
    user=Login.objects.get(name=pk)
    ptype=user.ptype
    #get the details of projects user is a member of 
    projects_c=Projects.objects.exclude(leader=pk)
    proj_part=[]
    for i in projects_c:
        if(pk in i.members.split(",")):
            proj_part.append(i)
    #get the details of projects user has applied for 
    projects_c=Projects.objects.exclude(leader=pk)
    proj_applied=[]
    for i in projects_c:
        temp=i.applied.split(",")
        temp1=[i.split("-") for i in temp]
        temp3=[i[0] for i in temp1]
        if(pk in temp3):
            proj_applied.append(i)
    #print("own projects:",projects_own)
    #print("member:",proj_part)
    #print("applied",proj_applied)
    if(ptype=="hire"):
        return render(request, 'myprojectsh.html', {'pk': pk,'projects_own':projects_own,'proj_part':proj_part,'proj_applied':proj_applied})
    return render(request, 'myprojects.html', {'pk': pk,'projects_own':projects_own,'proj_part':proj_part,'proj_applied':proj_applied})


def myproj(request,pk,proj):
    pr=Projects.objects.get(name=proj)
    print(pr.applied.split(","),pr.members.split(","))
    applied=[]
    for i in pr.applied.split(","):
        print(i)
        if(i!=''):
            name_bid=i.split('-')
            u=Users.objects.get(name=name_bid[0])
            applied.append([name_bid[0],name_bid[1],u,u.skills.split(',')])
    pr_skills=set(pr.skills.split(','))
    #Recommendation filtering Part
    for i in applied:
        i.append(len(pr_skills.intersection(i[3])))
    applied=sorted(applied, key=lambda x: x[4],reverse=True)
    #############################
    members=[]
    for i in pr.members.split(","):
        print(i)
        if(i!=''):
            u=Users.objects.get(name=i)
            members.append((i,u,u.skills.split(',')))
    return render(request, 'myprojh.html', {'pk':pk,'proj':pr,'applied':applied,"participants":members})

def hire(request,pk,proj,name):
    pr=Projects.objects.get(name=proj)
    participants_so_far=pr.members
    new_participants=participants_so_far+","+name
    pr.members=new_participants
    pr.save()
    applied=pr.applied.split(",")
    new_applied=[]
    for i in applied:
        if(i.split("-")[0]!=name):
            new_applied.append(i)
    pr.applied=",".join(new_applied)
    pr.save()
    return redirect('myproj',pk=pk,proj=proj)


def proj_applied(request,pk,proj):
    pr=Projects.objects.get(name=proj)
    participants=[]
    for i in pr.members.split(","):
        if(i!=''):
            u=Users.objects.get(name=i)
            participants.append((i,u,u.skills.split(',')))
    return render(request, 'proj_applied.html', {'pk':pk,'proj':pr,"participants":participants})

def browse(request,user):
    skills = Users.objects.all().filter(name=user).values('skills')
    l1=[i for i in skills]
    d=l1[0]
    d2 = {'skills':list(d['skills'].split(','))}
    projects = Projects.objects.all().values('name','skills','max_payment','desc','project_id','leader','members','applied')
    l2=[]
    #select those projects that the user did not create, that the user has not applied or has been selected for
    for i in projects:
        if(i['applied']==''):
            applied=[]
        else:
            temp=i['applied'].split(",")
            temp2=[i.split("-") for i in temp]
            applied=[i[0] for i in temp2]
        if(i['members']==''):
            participants=[]
        else:
            participants=i['members'].split(",")
        if(user not in participants and user not in applied and user!=i['leader']):
            l2.append(i)
    for i in l2:
        i['skills'] = list(i['skills'].split(','))
    for j in l2:
        j['len']=len(list(set(j['skills']) & set(d2['skills'])))
    f_order = sorted(l2,key = lambda i : (i['len']),reverse=True)
    mp=[]
    for i in f_order:
        mp1 = []
        mp1.append(i['name'])
        mp1.append(i['desc'])
        mp1.append(i['max_payment'])
        mp1.append(i['project_id'])
        mp.append(mp1)
    return render(request,'browse.html',{'user':user,'pro':mp})

def browse_pro_desc(request,pid,pk):
	if request.method=="POST":
		bid = request.POST.get("bid")
		pro = Projects.objects.get(project_id=pid)
		s1 = str(pk)
		s2 = str(bid)
		s3 = s1+'-'+s2
		pro.applied = pro.applied + ','+s3
		pro.save()
		return redirect('profile',pk=pk)
	d = Projects.objects.all().filter(project_id=pid).values()
	l1=[i for i in d]
	l2=[]
	d=l1[0]
	l2.append(d['name'])
	l2.append(d['desc'])
	l2.append(d['max_payment'])
	l2.append(d['skills'])
	l2.append(d['days'])
	l2.append(d['leader'])
	l2.append(d['members'])
	return render(request,'browse_pro_desc.html',{'user':pk,'d':l2})


