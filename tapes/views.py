from django.shortcuts import render, get_object_or_404
from django.views import generic
from tapes.models import post,comment
from tapes.forms import Form,Form_post
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic.edit import FormMixin,FormView
from django.urls import reverse,reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class MainListView(generic.ListView):
    
    model = post
    template_name = '1.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super(MainListView, self).get_context_data(**kwargs)
        num_visits=self.request.session.get('num_visits', 0)
        self.request.session['num_visits'] = num_visits+1
        context['visits'] = self.request.session['num_visits']
        return context

class ListPageView(FormMixin,generic.DetailView):
    form_class = Form
    model = post
    template_name = '2.html'

    def get_success_url(self,**kwargs):
        return reverse("tapes:detail",args=[self.object.pk])

    def get_context_data(self,*args, **kwargs):
        context = super(ListPageView, self).get_context_data(**kwargs)
        context['comment'] = comment.objects.all()
        context['form'] = self.get_form()
        pk = self.kwargs.get('pk')
        Post_default = get_object_or_404(post,pk = pk)
        context['post'] = Post_default
        return context

    def post(self, request, *args,pk, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            Post = get_object_or_404(post,pk = pk)
            new_comment = form.save(commit=False)
            new_comment.post = Post
            new_comment.nickname = request.user.username
            new_comment.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def form_valid(self, form):
        return super().form_valid(form)
        
    def get_initial(self):
        return {"post": self.get_object() }

class PostFormCreate(View):
    
    def get(self,request):
        user_form = Form_post()
        return render(request, 'reg.html',context={'form':user_form})

    def post(self,request):
        user_form = Form_post(request.POST)
        if user_form.is_valid():
            post.objects.create(**user_form.cleaned_data)
            return HttpResponseRedirect('/list/create_post/')
        return render(request, 'reg.html',context={'form':user_form})


class RegisterView(FormView):
    form_class = UserCreationForm
    # success_url = reverse_lazy('accounts/login/')
    success_url = 'login/'
    template_name = 'user_registration.html'
    def form_valid(self, form):
        form.save()
        return super(RegisterView, self).form_valid(form)