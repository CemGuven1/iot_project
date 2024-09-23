from django.shortcuts import redirect, render
from .models import Device, DataEntry
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
from django.utils import timezone
 
 
@login_required
def dashboard(request):
    user = request.user  # Use the User model instead of Customer
    devices = Device.objects.filter(user=user)  # Now filter devices by user

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
    
    return render(request, 'devices.html', {'page_obj': page_obj})



@login_required
def device_detail(request, device_id):
    user = request.user  # Use the User model instead of Customer
    device = Device.objects.get(device_id=device_id, user=user)  # Ensure it's the user's device
    data_entries = DataEntry.objects.filter(device=device).order_by('-timestamp')

    # Paginate data entries
    paginator = Paginator(data_entries, 10)  # Show 10 data entries per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'device_chart.html', {'device': device, 'page_obj': page_obj})



@csrf_exempt  # Exempt from CSRF verification for simplicity (not recommended for production)
def receive_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            device_id = data.get('device_id')
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
            # Create a new data entry
            DataEntry.objects.create(
                device=device,
                acceleration_x=acceleration_x,
                acceleration_y=acceleration_y,
                acceleration_z=acceleration_z,
                gyro_x=gyro_x,
                gyro_y=gyro_y,
                gyro_z=gyro_z,
                temperature=temperature,
                battery=battery
            )
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
            return JsonResponse({'error': 'No new data found'}, status=404)

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
def register_device(request):
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            device = form.save(commit=False)
            device.user = request.user  # Set the user to the logged-in user
            device.save()
            return redirect('dashboard')  # Redirect back to dashboard after registration
    else:
        form = DeviceForm()

    return render(request, 'register_device.html', {'form': form})