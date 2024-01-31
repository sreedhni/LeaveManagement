from django import forms
from Leave.models import LeaveRequest,Employee

class UserLeaveUpdateForm(forms.ModelForm):
    class Meta:
          model=LeaveRequest
          exclude=("username","status")
          widgets={
            "leave_from":forms.DateInput(attrs={"type":"date"}),
            "leave_to":forms.DateInput(attrs={"type":"date"}),
        }
class AdminLeaveEditForm(forms.ModelForm):
    class Meta:
          model=LeaveRequest
          exclude=("employee","reason","leave_from","leave_to","username")
