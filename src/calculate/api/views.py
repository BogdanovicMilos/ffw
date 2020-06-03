from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from .serializers import AddSerializer, CalculateSerializer, ResetSerializer, HistorySerializer
from ..models import Calculate
from users.models import User
from rest_framework import status


ARRAY = []
CALCULATIONS = []


class AddView(APIView):
    serializer_class = AddSerializer

    @staticmethod
    def post(request, format=None):
        if not request.user.is_authenticated:
            return Response({'success': False, 'error': 'You must be logged in', 'status_code': 401}, status=status.HTTP_401_UNAUTHORIZED)
        data = request.data['array']
        try:
            for i in data.split(','):
                num = int(i)
                ARRAY.append(num)
            return Response({'success': True, 'message': 'Submitted successfully', 'array': ARRAY}, status=status.HTTP_200_OK)
        except ValueError:
            try:
                val = float(data)
                if val:
                    return Response({'success': False, 'error': 'Input must be a Integer, not Float', 'status_code': 400}, status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                return Response({'success': False, 'error': 'Input must be a Integer, not String', 'status_code': 400}, status=status.HTTP_400_BAD_REQUEST)


class CalculateView(APIView):
    serializer_class = CalculateSerializer

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'success': False, 'error': 'You must be logged in', 'status_code': 401}, status=status.HTTP_401_UNAUTHORIZED)
        cal = []
        if not ARRAY:
            return Response({'success': False, 'error': 'Array is empty', 'status_code': 404}, status=status.HTTP_404_NOT_FOUND)
        if kwargs.get('all', None):
            return Response({'success': True, 'message': 'Data found', 'calculation': CALCULATIONS},status=status.HTTP_200_OK)
        else:
            for x in ARRAY:
                cal.append(x)
            CALCULATIONS.append(sum(cal))
            return Response({'success': True, 'message': 'Data found', 'calculation': sum(cal)}, status=status.HTTP_200_OK)


class ResetView(APIView):
    serializer_class = ResetSerializer

    @staticmethod
    def post(request, format=None):
        if not request.user.is_authenticated:
            return Response({'success': False, 'error': 'You must be logged in', 'status_code': 401}, status=status.HTTP_401_UNAUTHORIZED)
        if not ARRAY and not CALCULATIONS:
            return Response({'success': False, 'error': 'Not Found', 'status_code': 404}, status=status.HTTP_404_NOT_FOUND)
        serializer = ResetSerializer(data=request.data, context={'array': ARRAY, 'calculations': CALCULATIONS, 'user': request.user})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            ARRAY.clear()
            CALCULATIONS.clear()
            return Response({'success': True, 'message': 'Reset successfully'}, status=status.HTTP_200_OK)
        return Response({'success': False, 'message': 'Failed to reset', 'status_code': 400}, status=status.HTTP_400_BAD_REQUEST)


class HistoryView(APIView):
    serializer_class = HistorySerializer

    @staticmethod
    def get_object(pk):
        try:
            return Calculate.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({'success': False, 'error': 'No data', 'status_code': 404}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        if not request.user.is_authenticated:
            return Response({'success': False, 'error': 'You must be logged in', 'status_code': 401}, status=status.HTTP_401_UNAUTHORIZED)
        calc = self.get_object(pk)
        if not calc:
            return Response({'success': False, 'error': 'No data', 'status_code': 404}, status=status.HTTP_404_NOT_FOUND)
        user = User.objects.get(id=self.request.user.id)
        if calc.user == user:
            serializer = HistorySerializer(calc)
            if calc:
                return Response({'success': True, 'message': 'Data found', 'data': serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({'success': False, 'error': 'No data', 'status_code': 404}, status=status.HTTP_404_NOT_FOUND)
        return Response({'success': False, 'error': "You don't have permission to view this data", 'status_code': 403}, status=status.HTTP_403_FORBIDDEN)


class HistoryList(APIView):
    serializer_class = HistorySerializer

    def get(self, request, format=None):
        if not request.user.is_authenticated:
            return Response({'success': False, 'error': 'You must be logged in', 'status_code': 401}, status=status.HTTP_401_UNAUTHORIZED)
        user = User.objects.get(id=self.request.user.id)
        objects = Calculate.objects.filter(user=user)
        serializer = HistorySerializer(objects, many=True)
        if objects:
            return Response({'success': True, 'message': 'Data found', 'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'success': False, 'error': 'No data', 'status_code': 404}, status=status.HTTP_404_NOT_FOUND)

