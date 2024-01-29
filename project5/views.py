from datetime import datetime
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Q
from django.utils import timezone


from .models import Event, Project, User
from .forms import ProjectForm

import json

def login_view(request):
    if request.method == "POST":
        # Retrieve form data
        username = request.POST["username"]
        password = request.POST["password"]

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        # Check if authentication is successful
        if user is not None:
            # Log in the user
            login(request, user)
            # Redirect to projects page
            return HttpResponseRedirect(reverse("projects"))
        else:
            # Handle invalid username or password error
            return render(
                request,
                "timeline/login.html",
                {"error_message": "Invalid username or password."},
            )
    else:
        # Render the login form 
        return render(request, "timeline/login.html")


def logout_view(request):
    # Logout request
    logout(request)
    # Redirect to index page
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":

        # Retrieve form data
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        # Check if passwords match
        if password != confirmation:
            return render(
                request, "timeline/register.html", {"error_message": "Passwords must match."}
            )

        try:
            # Create a new user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            # Log in the user
            login(request, user)

            # Redirect to projects
            return HttpResponseRedirect(reverse("projects"))
        except IntegrityError:

            # Handle username already taken
            return render(
                request, "timeline/register.html", {"error_message": "Username already taken."}
            )
    else:
        # Render registration form
        return render(request, "timeline/register.html")

def index(request):

    # Render index page
    return render(request, "timeline/index.html")


@login_required
def projects(request):
    # Get the search term from the query string
    search_term = request.GET.get("search")
    # Get the field to order by from the query string
    order_by = request.GET.get("order_by")
    # Get the user
    user = request.user
    # Retrieve projects for the current user that are not archived
    projects = Project.objects.filter(user=user, archived=False)
    
    # Apply search filter if search term is provided
    if search_term:
        projects = projects.filter(
            Q(name__icontains=search_term) | Q(description__icontains=search_term)
        )
    
    # Apply order by if field is provided
    if order_by:
        projects = projects.order_by(order_by)

    # Create a list of ordered objects
    ordered_projects = list(projects)
    
    # Create a paginator with 10 projects per page
    paginator = Paginator(ordered_projects, 10)
    # Get the current page number
    page = request.GET.get("page")
    try:
        # Get the projects for current page
        projects = paginator.page(page)
    except PageNotAnInteger:
        # If page parameter is not an integer, display the first page
        projects = paginator.page(1)
    except EmptyPage:
        # If the page is out of range, display the last page
        projects = paginator.page(paginator.num_pages)
    # Create a new instance of the NewProjectForm
    form = ProjectForm()
    # Render template
    return render(
        request,
        "timeline/projects.html",
        {
            "projects": projects,
            "form": form,
            "search_term": search_term,
            "order_by": order_by,
        },
    )

@login_required
def create_project(request):
    if request.method == "POST":
        # Create form instance
        form = ProjectForm(request.POST)
        if form.is_valid():
            # Extract content from form data
            name = form.cleaned_data["name"]
            description = form.cleaned_data["description"]
            start_date = form.cleaned_data["start_date"]
            end_date = form.cleaned_data["end_date"]
            # Check if end date is before start date
            if end_date < start_date:
                # End date starts before start date                
                return redirect("projects")
            else:
                # Set user as current user
                user = request.user
                # Create project
                project = Project.objects.create(user=user, name=name, description=description, start_date=start_date, end_date=end_date)
                # Redirect to projects page after successful creation
                return redirect("projects")
    else:
        # Create new form instance
        form = ProjectForm()
    # Render template
    return render(request, "timeline/projects.html", {"form": form})


@login_required
def update_project(request, project_id):
    try:
        # Get project object
        project = Project.objects.get(id=project_id)
        
        if request.method == 'POST':
            # Get data load from request body
            data = json.loads(request.body)
            name = data.get('name')
            description = data.get('description')
            start_date = data.get('start_date')
            end_date = data.get('end_date')
            
            if name and description and start_date and end_date:
                # Check if the user is the owner of the project
                if project.user == request.user:
                    # Validating date range
                    start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
                    end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()

                    if start_date >= end_date or (end_date - start_date).days < 1:
                        raise ValidationError("Invalid date range")

                    project.name = name
                    project.description = description
                    project.start_date = start_date
                    project.end_date = end_date
                    project.archived = False
                    project.save()

                    # Handle responses
                    return JsonResponse({'message': 'Project updated successfully!'})
                else:
                    return JsonResponse({'error': 'Unauthorized'}, status=403)
            else:
                return JsonResponse({'error': 'Invalid data'}, status=400)
        else:
            return JsonResponse({'error': 'Invalid request method'}, status=400)
    except Project.DoesNotExist:
        return JsonResponse({'error': 'Project not found'}, status=404)

@login_required
def delete_project(request, project_id):
    # Check if the request method is delete
    if request.method == 'DELETE':
        try:
            # Get de project object 
            project = get_object_or_404(Project, id=project_id)
            # Check if user is owner
            if project.user == request.user:
                # Delete project
                project.delete()

                # Return responses
                return JsonResponse({'message': 'Project deleted successfully!'})
            else:
                return JsonResponse({'error': 'Unauthorized'}, status=403)
        except Project.DoesNotExist:
            return JsonResponse({'error': 'Project not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required    
def archive_project(request, project_id):
    try:
        # Get the project object
        project = Project.objects.get(id=project_id)

        if request.method == 'POST':
            # Check if user is owner
            if project.user == request.user:
                # Archive project and save change
                project.archived = True
                project.save()

                # Return responses
                return JsonResponse({'message': 'Project archived successfully!'})
            else:
                return JsonResponse({'error': 'Unauthorized'}, status=403)
        else:
            return JsonResponse({'error': 'Invalid request method'}, status=400)
    except Project.DoesNotExist:
        return JsonResponse({'error': 'Project not found'}, status=404)
    
@login_required
def unarchive_project(request, project_id):
    try:
        # Get project object
        project = Project.objects.get(id=project_id)

        # Check if user is owner
        if request.method == 'POST':
            if project.user == request.user:
                # Unarchive project and save change
                project.archived = False  
                project.save()

                # Handle responses
                return JsonResponse({'message': 'Project unarchived successfully!'})
            else:
                return JsonResponse({'error': 'Unauthorized'}, status=403)
        else:
            return JsonResponse({'error': 'Invalid request method'}, status=400)
    except Project.DoesNotExist:
        return JsonResponse({'error': 'Project not found'}, status=404)


@login_required
def manage_project(request, project_id):
    # Get project object
    project = get_object_or_404(Project, pk=project_id)
    # Format dates for fullcalendar
    current_datetime = datetime.now().strftime('%Y-%m-%dT%H:%M')
    # Check if user is owner
    if project.user != request.user:
        raise Http404("You don't have permission to access this project.")
    # Get events for project
    events = Event.objects.filter(project_id=project_id).values('id', 'title', 'start', 'end', 'description', 'color')
    # Context 
    context = {
        "project": project,
        "events": events,
        "project_start_date": project.start_date.strftime('%Y-%m-%d'),
        "project_end_date": project.end_date.strftime('%Y-%m-%d'),
        "current_datetime": current_datetime
    }
    # Render manage project page
    return render(request, 'timeline/manage_project.html', context)


@login_required
def archived(request):
    # Get the user
    user = request.user
    archived_projects = Project.objects.filter(user=user, archived=True)
    # Get the search term from the query string
    search_term = request.GET.get("search")
    # Get the field to order by from the query string
    order_by = request.GET.get("order_by")
 
    
    # Apply search filter if search term is provided
    if search_term:
        archived_projects = archived_projects.filter(
            Q(name__icontains=search_term) | Q(description__icontains=search_term)
        )
    
    # Apply order by if field is provided
    if order_by:
        archived_projects = archived_projects.order_by(order_by)

    # Create a list of ordered objects
    ordered_projects = list(archived_projects)
    
    # Create a paginator with 10 projects per page
    paginator = Paginator(ordered_projects, 10)
    # Get the current page number
    page = request.GET.get("page")
    try:
        # Get the projects for current page
        archived_projects = paginator.page(page)
    except PageNotAnInteger:
        # If page parameter is not an integer, display the first page
        archived_projects = paginator.page(1)
    except EmptyPage:
        # If the page is out of range, display the last page
        archived_projects = paginator.page(paginator.num_pages)
    # Render template
    return render(
        request,
        "timeline/archived.html",
        {
            "search_term": search_term,
            "order_by": order_by,
            "archived_projects": archived_projects,
        },
    )

@login_required
def get_events(request, project_id):
    # Get start and end dates
    project = Project.objects.get(id=project_id)
    start_date = project.start_date
    end_date = project.end_date

    # Get events filter with project
    events = Event.objects.filter(project_id=project_id, start__gte=start_date, end__lte=end_date)

    # Conver events to JSON
    events_data = []
    for event in events:
        events_data.append({
            "id": event.id,
            "title": event.title,
            "start": event.start,
            "end": event.end,
            "description": event.description,
            "color": event.color,
        })

    # Response Json data event
    return JsonResponse(events_data, safe=False)


@login_required
def create_event(request, project_id):
    # Load body data from request
    data = json.loads(request.body)  

    # Check structure of data
    if 'title' in data and 'start' in data and 'end' in data:
        # Get project for event
        project = Project.objects.get(pk=project_id)

        # Create new event
        new_event = Event.objects.create(
            title=data['title'],
            start=data['start'],
            end=data['end'],
            project=project
        )

        # Save new event
        new_event.save()
        # Return response data
        return JsonResponse({"id": new_event.id})
    else:
        # Handle error
        return JsonResponse({"error": "Incomplete data"}, status=400)
    

@login_required
def update_event(request, project_id, event_id):
    try:
        # Get event object
        event = get_object_or_404(Event, project_id=project_id, id=event_id)
    
        # Get event data from request body
        data = json.loads(request.body) 

        # Update fields
        if 'title' in data:
            event.title = data['title']
        if 'start' in data:
            event.start = data['start']
        if 'end' in data:
            event.end = data['end']
        if 'description' in data:
            event.description = data['description']
        if 'color' in data:
            event.color = data['color']

        # Save changes
        event.save()

        # Handle responses
        return JsonResponse({"message": "Event updated successfully"})
    except Event.DoesNotExist:
        return JsonResponse({"error": "Event not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@login_required
def delete_event(request, project_id, event_id):
    if request.method == 'DELETE':
        # Get event from project
        event = get_object_or_404(Event, project_id=project_id, id=event_id)

        # Delete event
        event.delete()

        # Return succes response
        return JsonResponse({"message": "Event deleted successfully"})
    else:
        # Return error response
        return JsonResponse({"error": "Method not allowed"}, status=405)