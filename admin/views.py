import json
from datetime import datetime, timedelta
from django.shortcuts import render
from django.contrib.auth import get_user_model
from collections import Counter
from dashboard.models import Content
from dashboard.forms import ContentForm
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Count
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import ListView
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model



def get_total_users_excluding_superusers():
    User = get_user_model()
    total_users = User.objects.filter(is_superuser=False).count()
    return total_users

def get_active_and_inactive_users():
    User = get_user_model()
    now = datetime.now()
    last_week = now - timedelta(days=7)
    
    # Active users (logged in within the last 7 days)
    active_users = User.objects.filter(last_login__gte=last_week, is_superuser=False).count()
    
    # Inactive users (not logged in within the last 7 days)
    inactive_users = User.objects.filter(last_login__lt=last_week, is_superuser=False).count()
    
    return active_users, inactive_users

def get_user_creation_last_7_days():
    User = get_user_model()
    now = datetime.now().date()
    week_ago = now - timedelta(days=6)  # 7 days ago from today

    user_creation_counts = (
        User.objects.filter(date_joined__date__gte=week_ago)
        .filter(date_joined__date__lte=now)
        .extra({'date_joined_day': "date(date_joined)"})
        .values('date_joined_day')
        .annotate(count=Count('id'))
        .order_by('date_joined_day')
    )

    user_creation_data = {}
    for entry in user_creation_counts:
        # Convert date_joined_day to string
        date_str = entry['date_joined_day'].strftime('%Y-%m-%d')
        user_creation_data[date_str] = entry['count']

    return user_creation_data

def index(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            total_users = get_total_users_excluding_superusers()
            active_users, inactive_users = get_active_and_inactive_users()

            # Query all genres from database
            all_genres = Content.objects.values_list('genre', flat=True)

            # Flatten all genres into a single list
            all_genres_list = [genre.strip() for genres in all_genres for genre in genres.split(',')]

            # Count occurrences of each genre
            genre_counts = Counter(all_genres_list)

            # Get top 7 genres by count
            top_genres = dict(sorted(genre_counts.items(), key=lambda item: item[1], reverse=True)[:7])

            # Query all languages from database
            all_languages = Content.objects.values_list('language', flat=True)

            # Flatten all languages into a single list
            all_languages_list = [language.strip() for languages in all_languages for language in languages.split(',')]

            # Count occurrences of each language
            language_counts = Counter(all_languages_list)

            # Get top 7 languages by count
            top_languages = dict(sorted(language_counts.items(), key=lambda item: item[1], reverse=True)[:7])

            # Query all years from database
            all_years = Content.objects.values_list('year', flat=True)

            # Calculate min and max years
            min_year = min(all_years) if all_years else None
            max_year = max(all_years) if all_years else None

            # Create year batches of 10 years
            year_batches = {}
            if min_year is not None and max_year is not None:
                for start_year in range(min_year, max_year + 1, 10):
                    end_year = start_year + 9
                    batch_label = f"{start_year}-{end_year}"
                    year_batches[batch_label] = len([year for year in all_years if start_year <= year <= end_year])

            # Get top 7 year batches by count
            top_year_batches = dict(sorted(year_batches.items(), key=lambda item: item[1], reverse=True)[:7])

            user_creation_data = get_user_creation_last_7_days()
          
            context = {
                'user_info': request.user,
                'total_users': total_users,
                'active_users': active_users,
                'inactive_users': inactive_users,
                'top_genres_json': json.dumps(top_genres),
                'top_languages_json': json.dumps(top_languages),
                'top_year_batches_json': json.dumps(top_year_batches),
                'user_creation_data_json': json.dumps(user_creation_data)
            }
            
            return render(request, 'index.html', context)
        else:
            return render(request, 'not_allowed.html')
    else:
        return render(request, 'login.html')


class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return render(self.request, 'not_valid.html')

class ContentListView(SuperuserRequiredMixin, ListView):
    model = Content
    template_name = 'content_list.html'
    context_object_name = 'contents'
    paginate_by = 10  # Display 10 results per page

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Content.objects.filter(Q(title__icontains=query) | Q(imdbid__icontains=query))[:10]
        return Content.objects.all()[:10]

class ContentCreateView(SuperuserRequiredMixin, CreateView):
    model = Content
    form_class = ContentForm
    template_name = 'content_form.html'  # Template for creating new content
    success_url = reverse_lazy('content-list')  # Redirect URL after successful creation

class ContentUpdateView(SuperuserRequiredMixin, UpdateView):
    model = Content
    form_class = ContentForm
    template_name = 'content_form.html'  # Template for updating existing content
    success_url = reverse_lazy('content-list')  # Redirect URL after successful update

class ContentDeleteView(SuperuserRequiredMixin, DeleteView):
    model = Content
    template_name = 'content_confirm_delete.html'  # Template for confirming deletion
    success_url = reverse_lazy('content-list')


def users(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            User = get_user_model()
            # get all the users and all the column details from the database
            users = User.objects.values()

            return render(request, 'users.html', {'users': users})
        else:
            return render(request, 'not_allowed.html')
    else:
        return render(request, 'login.html')
    
@login_required
@csrf_exempt
def delete_user(request):
    if request.method == 'POST':
        # Check if the user is authenticated and is a superuser
        if request.user.is_authenticated and request.user.is_superuser:
            user_id = request.POST.get('user_id')
            
            if user_id:
                try:
                    # Get the user object or return 404 if not found
                    User = get_user_model()
                    user = get_object_or_404(User, id=user_id)
                    
                    # Ensure the superuser is not deleting themselves (optional)
                    if user != request.user:
                        user.delete()
                        return JsonResponse({'success': True, 'message': 'User deleted successfully.'})
                    else:
                        return JsonResponse({'success': False, 'message': 'Cannot delete yourself.'}, status=403)
                except Exception as e:
                    return JsonResponse({'success': False, 'message': str(e)}, status=400)
            else:
                return JsonResponse({'success': False, 'message': 'User ID not provided.'}, status=400)
        else:
            return JsonResponse({'success': False, 'message': 'Unauthorized.'}, status=403)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=405)
    

@login_required
@csrf_exempt
def toggle_user_enabled(request):
    if request.method == 'POST':
        # Check if the user is authenticated and is a superuser
        if request.user.is_authenticated and request.user.is_superuser:
            user_id = request.POST.get('user_id')
            
            if user_id:
                try:
                    # Get the user object or return 404 if not found
                    User = get_user_model()
                    user = get_object_or_404(User, id=user_id)
                    
                    # Ensure the superuser is not toggling their own status (optional)
                    if user != request.user:
                        user.is_active = not user.is_active
                        user.save()
                        return JsonResponse({'success': True, 'message': 'User status toggled successfully.'})
                    else:
                        return JsonResponse({'success': False, 'message': 'Cannot toggle your own status.'}, status=403)
                except Exception as e:
                    return JsonResponse({'success': False, 'message': str(e)}, status=400)
            else:
                return JsonResponse({'success': False, 'message': 'User ID not provided.'}, status=400)
        else:
            return JsonResponse({'success': False, 'message': 'Unauthorized.'}, status=403)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=405)