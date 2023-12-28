from django.shortcuts import render, redirect
from .models import Chatbox, Message
from django.views.generic.edit import CreateView
from .forms import ChatBoxCreateForm, MessageCreateForm, MessageInfoForm
from django.urls import reverse_lazy, reverse
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseForbidden
from django.views.generic.edit import FormMixin
from .consumers import ChatConsumer


@login_required
def index(request):
    owned_chatbox_list = request.user.owned_chatbox.all()
    guest_chatbox_list = request.user.guest_chatbox.all()

    context = {
        'owned_chatbox_list': owned_chatbox_list,
        'guest_chatbox_list': guest_chatbox_list,
    }
    return render(request, 'chatroom/index.html', context)


@method_decorator(login_required, name="dispatch")
class CreateChatBoxView(CreateView):
    template_name = 'chatroom/create_chat_box.html'
    form_class = ChatBoxCreateForm
    model = Chatbox
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class DetailChatBoxView(FormMixin, DetailView):
    template_name = 'chatroom/detail_chat_box.html'
    model = Chatbox
    form_class = MessageInfoForm

    def get(self, request, *args, **kwargs):
        chatbox = self.get_object()
        if request.user == chatbox.author or request.user == chatbox.guest:
            messages = Message.objects.filter(chatbox=chatbox)
            return render(request, self.template_name, {'messages': messages, 'object': chatbox})
        else:
            return render(request, 'chatroom/unauthorized_acces.html')

    def get_success_url(self):
        return reverse('chat_box_detail', kwargs={'pk': self.object.pk})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            content = form.cleaned_data['content']
            Message.objects.create(chatbox=self.object, author=request.user, content=content)
            chat_consumer = ChatConsumer()
            chat_consumer.send_group_message(content, self.object.pk)
            return redirect('chat_box_detail', pk=self.object.pk)
        else:
            context = self.get_context_data(object=self.object)
            messages = Message.objects.filter(chatbox=self.object)
            context['messages'] = messages
            context['form'] = form
            return self.render_to_response(context)

    def form_valid(self, form):
        # Here, we would record the user's interest using the message
        # passed in form.cleaned_data['message']
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class CreateMessageView(CreateView):
    template_name = 'chatroom/create_message.html'
    model = Message
    form_class = MessageCreateForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        chatbox_pk = self.kwargs.get('pk')
        chatbox = Chatbox.objects.get(pk=chatbox_pk)
        form.instance.chatbox = chatbox
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('chat_box_detail', kwargs={'pk': self.kwargs.get('pk')})


class CreateUserView(CreateView):
    template_name = 'chatroom/create_user.html'
    model = Chatbox
    form_class = UserCreationForm
    success_url = reverse_lazy('index')


def logout_view(request):
    logout(request)
    return redirect(reverse('login'))
    # Redirect to a success page.


