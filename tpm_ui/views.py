# views.py
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test

def _login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if settings.AUTH_ENABLED:
            return login_required(view_func)(request, *args, **kwargs)
        else:
            return view_func(request, *args, **kwargs)
    return wrapper

def user_in_tpm_group(user):
    print(user)
    # return True
    return user.groups.filter(name='tpm')

@user_passes_test(user_in_tpm_group)
@_login_required
def display_page(request, page_name=None):
    print(request)
    return render(request, 'tpm.html')

@_login_required
def home(request, page_name=None):
    if settings.AUTH_ENABLED is True:
        user_groups = get_user_groups(request.user) # Function to get user's groups
        print(user_groups)
        accessible_paths = {value for key in user_groups if key in settings.TPM_PERMISSIONS for value in settings.TPM_PERMISSIONS[key]}
        accessible_pages = [page for page in settings.TPM_PAGES if page['path'] in accessible_paths]
    else:
        accessible_pages = settings.TPM_PAGES

    return render(request, 'home.html', {'pages': accessible_pages, "LOGOUT_URL":settings.LOGOUT_URL})

def index(request):
    return render(request, 'index.html', {"LOGIN_URL":settings.LOGIN_URL})

def get_user_groups(user):
    # Logic to retrieve the user's groups; this might vary based on how groups are managed in your application.
    print(user)
    return ['lavlab-brain']