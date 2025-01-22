from swelocaltoursapi.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def check_user(request):
    try:
        
        uid = request.data.get('uid')

        user = User.objects.filter(uid=uid).first()

        if user:
            data = {
                'firstName': user.first_name,
                'lastName': user.last_name,
                'bio': user.bio,
                'uid': user.uid,
            }
            return Response(data)
        else:
            return Response({'valid': False}, status=404)
    except KeyError:
        return Response({'error': "'uid' key is missing in the request"}, status=400)
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['POST'])
def register_user(request):
    user = User.objects.create(
        first_name=request.data['first_name'],
        last_name=request.data['last_name'],
        bio=request.data['bio'],
        uid=request.data['uid'],
    )

    data = {
        'id': user.id,
        'uid': user.uid,
        'bio': user.bio,
        'firstName': user.first_name,
        'lastName': user.last_name,
    }

    return Response(data)
