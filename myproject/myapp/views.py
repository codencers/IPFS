import os
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .pintata import upload_file_to_pinata
from django.shortcuts import render

# Configure logging
logger = logging.getLogger(__name__)

@csrf_exempt
def upload_view(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        file_path = os.path.join('temp', uploaded_file.name)

        try:
            # Save the uploaded file temporarily
            os.makedirs('temp', exist_ok=True)
            with open(file_path, 'wb') as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)

            # Upload the file to Pinata
            ipfs_hash = upload_file_to_pinata(file_path)

            # Clean up the temporary file
            os.remove(file_path)

            # Return the IPFS hash as a JSON response
            return JsonResponse({'success': True, 'ipfs_hash': ipfs_hash})

        except Exception as e:
            # Log the error
            logger.error(f"Error during file upload: {str(e)}", exc_info=True)

            # Handle errors during the upload process
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method or no file provided'}, status=400)

def home_view(request):
    return render(request, 'upload.html')