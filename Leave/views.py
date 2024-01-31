from django.shortcuts import render,redirect
from Leave.models import*
from Leave.forms import*
from django.http import HttpResponse
from django.contrib.auth import logout
from django.views.generic import CreateView,ListView,UpdateView,DetailView
from django.urls import reverse_lazy,reverse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.http import Http404





def index(request):
    return render(request,'index.html')

def ad_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        email =request.POST.get('email')

        if username:  
            a = Employee(username=username, password=password, role=role, email=email)
            a.save()
            return redirect("ad-login")
        else:
            return HttpResponse('Username cannot be empty')
    return render(request, 'adregister.html')

def ad_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        for employee in Employee.objects.all():
            if employee.username == username and employee.password == password:
                request.session['id1'] = employee.id
                found_user = True  
                break  
        
        if found_user:
            return redirect("admin")

        else:
            return HttpResponse("invalid credentials")

    return render(request, 'ad_login.html')

def usr_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        email =request.POST.get('email')

        if username:  
            a = Employee(username=username, password=password, role=role, email=email)
            a.save()
            return redirect("usr-login")
        else:
            return HttpResponse('Username cannot be empty')
    return render(request, 'usr_reg.html')

def usr_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        for employee in Employee.objects.all():
            if employee.username == username and employee.password == password:
                request.session['id2'] = employee.id
                found_user = True  
                break  
        
        if found_user:
            return redirect("user")

        else:
            return HttpResponse("invalid credentials")

    return render(request, 'usr_login.html')

    success_url = reverse_lazy("user")

class SessionRequiredAd:
    def dispatch(self, request, *args, **kwargs):
        if 'id1' not in request.session:
            return HttpResponse("Unauthorized", status=401)
        return super().dispatch(request, *args, **kwargs)


class SessionRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if 'id2' not in request.session:
            return HttpResponse("Unauthorized", status=401)
        return super().dispatch(request, *args, **kwargs)

class EmployeeLeaveCreateView(SessionRequiredMixin, CreateView):
    template_name = "uleave_add.html"
    model = LeaveRequest
    form_class = UserLeaveUpdateForm
    success_url = reverse_lazy("user")

    def form_valid(self, form):
        employee_id = self.request.session['id2']
        employee = Employee.objects.get(id=employee_id)
        form.instance.employee = employee
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employee_id = self.request.session['id2']
        context['employee_id'] = employee_id
        return context

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['employee'].queryset = Employee.objects.filter(id=self.request.session['id2'])
        return form

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            leave_request_employee_id = form.cleaned_data['employee'].id
            logged_in_employee_id = request.session['id2']
            if leave_request_employee_id == logged_in_employee_id:
                return self.form_valid(form)
            else:
                return HttpResponse("Unauthorized", status=401)
        else:
            return self.form_invalid(form)

class AdLeaveListView(ListView,SessionRequiredAd):
    template_name="admin.html"
    model=LeaveRequest
    context_object_name="leaves"
    success_url=reverse_lazy("admin")


class ALeaveUpdateView(UpdateView):
    template_name="adleave_edit.html"
    model=LeaveRequest
    form_class=AdminLeaveEditForm
    success_url=reverse_lazy("admin")



class ULeaveListView(ListView):
    template_name="usr.html"
    model=LeaveRequest
    context_object_name="leaves"
    success_url=reverse_lazy("user")






class EmployeeLeaveUpdateView(UpdateView):
    template_name="uleave_edit.html"
    model=LeaveRequest
    form_class=UserLeaveUpdateForm
    success_url=reverse_lazy("user")


class LeaveDetailView(SessionRequiredMixin,DetailView):
    template_name="leave_detail.html"
    model=LeaveRequest
    context_object_name="leave"
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        logged_in_employee_id = self.request.session.get('id2')
        if obj.employee_id != logged_in_employee_id:
            raise Http404("Leave request does not exist or you do not have permission to access it.")
        return obj



def remove_leaveview(request,*args,**kwargs):
    id=kwargs.get("pk")
    LeaveRequest.objects.filter(id=id).delete()
    return redirect("user")



def sign_outview(request,*args,**kwargs):
    logout(request)
    return redirect("index")










