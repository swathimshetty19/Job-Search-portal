from django.test import TestCase
from django.test import Client
from .forms import *   # import all forms
from .models import *
from django.urls import resolve
from django.urls import path
from freelancerapp import views
from django.urls import reverse

class Setup_Class(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = Login.objects.create(name="swara",password="shetty")
        self.user1=Users.objects.create(name ="swara",
    firstname="swara",
    lastname="shetty",
    email = "swara@gmail.com",
    phone = 7337697531,
    experience="intermediate",
    skills="html")
        self.project = Projects.objects.create(project_id="20",name="swaras project",desc="its my project",skills="php,html",leader="swara",members="shruthi,abhijith",applied="swathi-1500,sarva-1700",max_payment="2500",days="20")

    def tearDown(self):
        self.user.delete()
        self.user1.delete()
        self.user2.delete()
        self.user3.delete()
        self.project.delete()


class model_Test(TestCase):
    def test_skills(self):
        entry = Skills(skill="django")
        self.assertEqual(str(entry),"django")

    


class Form_Test(TestCase):

    # Valid Form Data
    def test_signupForm_valid(self):
        form = signupForm(data={'name':"swathi",'password':"shetty"})
        self.assertTrue(form.is_valid())

    # Invalid Form Data
    def test_signupForm_invalid(self):
        form = signupForm(data={'name': "", 'password':4567})
        self.assertFalse(form.is_valid())


class url_Test(Setup_Class):
    def test_invalid_views_url(self):
        url = reverse('invalidview')
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, 'invalidview')

    def test_addskill_url(self):
        url = reverse('add_skill',kwargs={'pk':self.user1.name,'skill':"php"})
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, 'add_skill')

    

class Views_Test(Setup_Class):

    def test_profile_view(self):
        url = reverse('profile',kwargs={'pk':self.user1.name})
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, 'profile')
        response_get = self.client.get(url)
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, "profile.html")

    def test_add_skill(self):
        url = reverse('add_skill',kwargs={'pk':self.user1.name,'skill':"php"})
        response_get = self.client.get(url,follow=True)
        last_url, status_code = response_get.redirect_chain[-1]
        #print(last_url)
        self.assertEqual(status_code, 302)
        self.assertEqual(last_url,reverse('skills',kwargs={'pk':self.user1.name}))

    def test_skills_view(self):
        url = reverse('skills',kwargs={'pk':self.user1.name})
        response_get = self.client.get(url)
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, "skills.html")



    def test_search_titles(self):
        response_get = self.client.get('/skills/{0}/search/'.format(self.user1.name))
        #print(response_get)
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, "ajax_search.html")


    

    def test_post_project(self):
        url = reverse('post_project',kwargs={'pk':self.user1.name})
        response_get = self.client.get(url)
        #print(response_get)
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, "post_project.html")

        response_post=self.client.post(url,data={'name':"swaras project",'desc':"its my project",'skills':"php,html",'max_payment':"2500",'days':"20"},follow=True)
        last_url, status_code = response_post.redirect_chain[-1]
        self.assertEqual(status_code, 302)
        self.assertEqual(last_url,reverse('profile',kwargs={'pk':self.user1.name}))
        
    def test_myprojects(self):
        url = reverse('myprojects',kwargs={'pk':self.user1.name})
        response_get = self.client.get(url)
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, "myprojects.html")
         
    def test_browse(self):
        url = reverse('browse',kwargs={'user':self.user1.name})
        response_get = self.client.get(url)
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, "browse.html")

    
