import random

from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse

from config import settings
from users.forms import UserRegisterForm, UserProfileForm
from django.views.generic import CreateView, UpdateView

from users.models import User


# Create your views here.
class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    # success_url = reverse_lazy('users:verification')

    def get_success_url(self):
        return reverse_lazy('users:verification', kwargs={'email': self.object.email})

    def form_valid(self, form):
        new_user = form.save()
        send_mail(
            subject="Поздравляем с регистрацией",
            message=f"Вы зарегистрировались на сайте, ура ура ура !!! \n"
                    f"Ваш код верификации:   {new_user.verification_code}\n",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email],
        )

        return super().form_valid(form)




class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def generate_new_password(request):

    word_list = list("Password12345")
    new_password = "".join(random.sample(word_list, len(word_list)))

    send_mail(
        subject="Вы сменили пароль",
        message=f"Ваш новый пароль: {new_password}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email],
    )
    request.user.set_password(new_password)
    request.user.save()
    return redirect(reverse_lazy('users:register'))


def verification(request, email):
    if request.method == 'POST':
        user_code = request.POST.get('code')
        user = User.objects.get(email=email)
        if user_code == user.verification_code:
            user.is_active = True
            user.save()
            return redirect(reverse("users:login"))

    return render(request, 'users/verification.html')
