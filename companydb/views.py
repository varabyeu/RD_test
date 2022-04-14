from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, generics


from companydb.models import Employee
from companydb.serializers import EmployeeSerializer

class EmployeeViewSet(generics.ListAPIView):
	"""Only authenticated users have access to API"""
	serializer_class = EmployeeSerializer
	filter_backends = [DjangoFilterBackend]
	filter_fields = ['level']
	permission_classes = (permissions.IsAuthenticated,)

	def get_queryset(self):
		return Employee.objects.all()

class DeleteEmployeeViewSet(generics.DestroyAPIView):
	"""Only admins can delete employee info"""
	queryset = Employee.objects.all()
	permission_classes = [permissions.IsAdminUser]
