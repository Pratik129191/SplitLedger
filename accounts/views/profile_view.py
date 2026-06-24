from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from accounts.forms import ProfileForm


@login_required
def profile_view(request):
    form = ProfileForm(
        request.POST or None,
        instance=request.user,
    )

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Profile updated successfully.'
            )
    return render(
        request,
        'accounts/profile.html',
        {
            'form': form,
        }
    )
