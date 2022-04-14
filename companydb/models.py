from django.core.exceptions import ValidationError
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Employee(MPTTModel):
	MAX_TREE_DEPTH = 5
	name = models.CharField(verbose_name='ФИО', max_length=255)
	position = models.CharField(verbose_name='Должность', max_length=255)
	employment_date = models.DateField(verbose_name='Дата приема на работу')
	salary = models.IntegerField(verbose_name='Заработная плата', default=0)
	total_pay = models.IntegerField(
		verbose_name='Информация по выплаченной зарплате',
		default=0
	)
	parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True,
							blank=True, related_name='children',
							verbose_name='Руководитель')


	def clean(self):
		if self.parent:
			if self.parent.get_level() + 2 > self.MAX_TREE_DEPTH:
				raise ValidationError(
					{'parent': f'Данный сотрудник не может быть руководителем'})


	def __str__(self):
		return '{}: {}'.format(self.name, self.position)

	class MPTTMeta:
		order_insertion_by = ['name']
