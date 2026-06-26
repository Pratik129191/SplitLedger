from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render


@login_required
def change_password_view(request):
    form = PasswordChangeForm(
        request.user,
        request.POST or None,
    )

    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(
                request,
                user
            )
            messages.success(
                request,
                'Your password was successfully updated!'
            )
        else:
            messages.error(
                request,
                "Please correct the errors below."
            )
    return render(
        request,
        'accounts/change_password.html',
        {
            'form': form,
        }
    )
