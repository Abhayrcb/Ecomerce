from django.shortcuts import render,redirect
from .forms import RegistrationForm,LoginForm,ForgotPageForm,ResetPasswordForm
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.urls import reverse

from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import  force_str
from .models import Account
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.views.generic import FormView,TemplateView
from django.views import View


# from django.views.
from django.urls import reverse_lazy

# step-1 register and genrate a activation link for specific user and send
# for registration view
class RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = RegistrationForm
    success_url =reverse_lazy('login')
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
         # registration user is not yet active until he activates his account using email link
       
        self.make_user_activation_link_content_and_send(self.request,user)
        messages.success(self.request, 'Registration successful!')
        return super().form_valid(form)
    
    
    
    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)
    
    
    def make_user_activation_link_content_and_send(self,request,obj):
        uid64 = urlsafe_base64_encode(force_bytes(obj.pk))
        token = default_token_generator.make_token(obj)
        reverse_link = reverse('activate', kwargs={'uid64': uid64, 'token': token})
        activation_url = f"{request.scheme}://{request.get_host()}{reverse_link}"   
        subject = 'Activate your account'
        html_content = render_to_string('accounts/MailContent/activation_email.html', {'activation_url': activation_url})
        text_content = strip_tags(html_content)
        mail(subject, text_content,  html_content,obj.email)
        


class ActivationAccountPage(View):
    def get(self,request,uid64, token):
        user_id = force_str(urlsafe_base64_decode(uid64))
       
        try:
            user = Account.objects.get(pk=user_id)
            print(user)
        except Account.DoesNotExist:
            return redirect('register')
        new_token = default_token_generator.check_token(user=user, token=token)
        if new_token:
            user.is_active = True
            user.save()
            messages.success(request, 'Account activated successfully! You can now log in.')
            return render(request, 'accounts/activate_success.html')
        else:
            messages.error(request, 'Activation link is invalid or has expired.')
            return redirect('register')


# step -3 login
# for login view and user is not able to login until he activates his account using email link
class LoginView(FormView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    success_url =reverse_lazy('home')
    
    def form_valid(self, form):
        user = authenticate(self.request,email=form.cleaned_data['email'],password=form.cleaned_data['password'])
        if user is not None:
            assign_user_to_cartitems(self.request,user)
            auth_login(self.request,user)
            messages.success(self.request, 'Login successful!')
            return super().form_valid(form)
        return self.form_invalid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid email or password. or may be your account is not activated yet.')
        
        return super().form_invalid(form)
    
    

# step-4 logout
# for logout view
def logout(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')




# step-5 forgot password if the user do not remember his password using email
# forgt password page view
# this view first brings email from template and after that it checks if email is present in database or not
# if email is present then it creates a password reset link and send it to user email
# ye page user user website pe hi dikhega jaha se wo apna password reset kar sakta hai

class ForgotPasswordPage(FormView):
    template_name ='accounts/FogrotPasword.html'
    form_class = ForgotPageForm
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        email = form.cleaned_data['email']
        try:
            user = Account.objects.get(email=email)
            # Here you would typically send a password reset email
            
            
            # Creating password reset link
            uid64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reverse_link = reverse('resetpass', kwargs={'uid64': uid64, 'token': token})
            
            # actual link jo reset password page tak le jayega user ko
            activation_url = f"{self.request.scheme}://{self.request.get_host()}{reverse_link}"   
            subject = 'Reset Password'
            # ye html page email ke andar hoga jisme password reset link hoga 
            # for these page we dont have to create any view and url because ye page sirf email ke andar hi dikhana hai
            # activation_url:-ye link hoga jisme uid64 and token hoga and view ka url hai reset password page ka
            html_content = render_to_string('accounts/MailContent/EmailForResetPasword.html', {'activation_url': activation_url,'user': user})
            text_content = strip_tags(html_content)
            mail(subject, text_content,  html_content,user.email)
            
            messages.success(self.request, 'Password reset link has been sent to your email.')
            
        except:
            messages.error(self.request, 'No account found with that email address.')
            self.form_invalid(form)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return super().form_invalid(form)
        
    
    

class ResetPasswordPage(FormView):
    template_name = 'accounts/reset_password.html'
    form_class = ResetPasswordForm
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        uid64 = self.kwargs.get('uid64')
        token = self.kwargs.get('token') 
        try:
            user_id = force_str(urlsafe_base64_decode(uid64))
            user = Account.objects.get(pk=user_id)
        except (Account.DoesNotExist, ValueError, TypeError, OverflowError):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            user.set_password(form.cleaned_data['password'])
            user.is_active = True  # Optionally activate the user if not already active
            user.save()
            messages.success(self.request, 'Your password has been reset successfully. You can now log in.')
            return super().form_valid(form)
        # otherwise always anythink wrong with the link
        messages.error(self.request, 'The reset link is invalid or has expired.')
        return redirect('forgot-password')
        
        
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request,form.errors)
        return response
    
    
    
 

# ................................................................. MAIN COMPONENTS................................................. 
# these function is actually for sending email
def mail(subject=None,text_content=None,html_content=None,to_email=None):
    
    if subject and text_content and html_content and to_email:
        
        msg =  EmailMultiAlternatives(subject, text_content, 'abhayrnj197@gmail.com', [to_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()





def assign_user_to_cartitems(request,user):
    from cart.models import Cart,CartItem
    from cart.views import _cart_id
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart)
        for item in cart_items:
            item.user = user
            item.save()
    except Cart.DoesNotExist:
        pass



    
    
    



class DashboardView(LoginRequiredMixin,TemplateView):
    template_name = 'accounts/dashboard/dashboard.html'