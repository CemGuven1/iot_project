from django.shortcuts import redirect, render, get_object_or_404
from .models import Device, DataEntry, Project
from django.contrib.auth.decorators import login_required
from .models import Device, DataEntry
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from .forms import CustomUserCreationForm  # Import custom form
from .forms import DeviceForm  # We'll create this form
from datetime import datetime
from .forms import ProjectForm
from django.http import HttpResponse
from django.urls import reverse
 
@login_required
def dashboard(request, project_id):

    project = Project.objects.get(id=project_id, user=request.user)     # Fetch the selected project
    devices = project.devices.all()     # Fetch devices related to the project

    # For each device, get the latest data entry
    devices_with_data = []
    for device in devices:
        latest_data = DataEntry.objects.filter(device=device).order_by('-timestamp').first()
        devices_with_data.append({
            'device': device,
            'latest_data': latest_data,
        })

    # Paginate the devices
    paginator = Paginator(devices_with_data, 5)  # Show 5 devices per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'devices.html', {'page_obj': page_obj, 'project': project})



@login_required
def device_detail(request, device_id):
    user = request.user  # Use the User model instead of Customer
    device = Device.objects.get(device_id=device_id, user=user)  # Ensure it's the user's device
    project = device.project  # Access the project associated with the device
    
    return render(request, 'device_chart.html', {'device': device, 'project':project})



@login_required
def project_list(request):
    # Fetch all projects associated with the current user
    projects = Project.objects.filter(user=request.user)
    return render(request, 'project_list.html', {'projects': projects})


@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user  # Associate the project with the logged-in user
            project.save()
            return redirect('project-list')  # Redirect to the project list after creation
    else:
        form = ProjectForm()

    return render(request, 'create_project.html', {'form': form})



@csrf_exempt  # Exempt from CSRF verification for simplicity (not recommended for production)
def receive_data(request):
    if request.method == 'POST':
        try:
            # Expecting a list of entries
            data_entries = json.loads(request.body)  # This should be a list of dictionaries
            data_objects = []  # List to hold DataEntry objects for bulk creation

            for data in data_entries:  # Loop through each entry
                packetID = data.get('packetID', 0.0)
                device_id = data.get('device_id')

                unix_time = data.get('unix_time')  # Get Unix timestamp
                millisecond = data.get('millisecond')  # Get milliseconds

                # Convert Unix time and milliseconds to a datetime object
                timestamp = datetime.fromtimestamp(unix_time + millisecond / 1000.0)

                acceleration_x = data.get('acceleration_x', 0.0)
                acceleration_y = data.get('acceleration_y', 0.0)
                acceleration_z = data.get('acceleration_z', 0.0)
                gyro_x = data.get('gyro_x', 0.0)
                gyro_y = data.get('gyro_y', 0.0)
                gyro_z = data.get('gyro_z', 0.0)
                temperature = data.get('temperature', 0.0)
                battery = data.get('battery', 100.0)

                # Find the device
                device = Device.objects.get(device_id=device_id)
                
                # Create a new DataEntry object
                data_objects.append(DataEntry(
                    packetID=packetID,
                    device=device,
                    timestamp=timestamp,
                    acceleration_x=acceleration_x,
                    acceleration_y=acceleration_y,
                    acceleration_z=acceleration_z,
                    gyro_x=gyro_x,
                    gyro_y=gyro_y,
                    gyro_z=gyro_z,
                    temperature=temperature,
                    battery=battery
                ))

            # Bulk create DataEntry objects in the database
            DataEntry.objects.bulk_create(data_objects)

            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)



@require_GET
def fetch_latest_data(request, device_id):
    try:
        device = Device.objects.get(device_id=device_id, user=request.user)
        last_timestamp = request.GET.get('lastUpdateTimestamp')
        
        # If no last timestamp is provided, return all data (for initialization)
        if last_timestamp:
            last_timestamp = datetime.strptime(last_timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
            new_data = DataEntry.objects.filter(device=device, timestamp__gt=last_timestamp).order_by('timestamp').values()  #filter out already printed data
        else:
            new_data = DataEntry.objects.filter(device=device).order_by('timestamp').values()  # Return all data if no timestamp

        if new_data:
            return JsonResponse({'new_data': list(new_data)})
        else:
            return JsonResponse({'message': 'No new data to update'}, status=200)  # Change 404 to 200

    except Device.DoesNotExist:
        return JsonResponse({'error': 'Device not found'}, status=404)

    


# Registration view
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


# Login view (optional if you use Django's built-in auth views, see below)
def login_view(request):
    return auth_views.LoginView.as_view(template_name='login.html', authentication_form=AuthenticationForm)(request)


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def register_device(request, project_id):
    # Get the project associated with the ID
    project = get_object_or_404(Project, id=project_id, user=request.user)
    
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            device = form.save(commit=False)
            device.user = request.user  # Set the user to the logged-in user
            device.project = project    # Associate the device with the selected project
            device.save()
            # Redirect back to the devices dashboard for the specific project
            return redirect('dashboard', project_id=project.id)  
    else:
        form = DeviceForm()

    return render(request, 'register_device.html', {'form': form, 'project': project})


@login_required
def device_delete(request, device_id):
    device = get_object_or_404(Device, device_id=device_id)
    project_id = device.project.id  # Assuming Device has a ForeignKey to Project
    
    if request.method == 'POST':
        device.delete()
        return HttpResponse(f"<script>alert('Device deleted successfully.'); window.location.href='{reverse('dashboard', args=[project_id])}';</script>")

    return redirect('device-list')  # Fallback in case it's not a POST request



@login_required
def project_delete(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        project.delete()
        return HttpResponse(f"<script>alert('Project deleted successfully.'); window.location.href='{reverse('project-list')}';</script>")

    return redirect('project-list')  # Fallback in case it's not a POST request




def fetch_latest_device_data(request, project_id):
    project = Project.objects.get(id=project_id, user=request.user)  # Fetch the selected project
    devices = project.devices.all()  # Fetch devices related to the project

    devices_with_data = []
    for device in devices:
        latest_data = DataEntry.objects.filter(device=device).order_by('-timestamp').first()
        if latest_data:
            devices_with_data.append({
                'device_id': device.device_id,
                'acceleration_x': latest_data.acceleration_x,
                'acceleration_y': latest_data.acceleration_y,
                'acceleration_z': latest_data.acceleration_z,
                'gyro_x': latest_data.gyro_x,
                'gyro_y': latest_data.gyro_y,
                'gyro_z': latest_data.gyro_z,
                'temperature': latest_data.temperature,
                'battery': latest_data.battery,
                'timestamp': latest_data.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            })
    return JsonResponse(devices_with_data, safe=False)
