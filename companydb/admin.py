from django.contrib import admin
from .models import Employee


@admin.action(description='Удалить информацию о выплаченной зарплате')
def clear_total_pay(modeldmin, request, queryset):
	queryset.update(total_pay=0)


class EmployeeAdmin(admin.ModelAdmin):
	list_display = (
		'name', 'position', 'link_to_chief',
		'salary', 'total_pay', 'get_employee_level',
	)

	list_display_links = ('name', 'link_to_chief',)
	list_filter = (
		'position',
		'parent',
	)
	actions = [clear_total_pay]

	def get_employee_level(self, object):
		return object.get_level()

	get_employee_level.short_description = 'Уровень'
	get_employee_level.allow_tags = True

	def link_to_chief(self, object):
		from django.utils.html import format_html

		chief_level = object.get_level() - 1
		if chief_level >= 0:
			chief_name = str(Employee.objects.filter(level=chief_level)).split(':')[1].strip()
			chief_id = Employee.objects.get(name=chief_name).id
			chief_url = f'/admin/companydb/employee/{chief_id}/change/'
			return format_html(f'<a href="{chief_url}">{chief_name}</a>')

	link_to_chief.short_description = 'Руководитель'
	link_to_chief.allow_tags = True

admin.site.register(Employee, EmployeeAdmin)
