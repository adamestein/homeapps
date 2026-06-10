from django.db import models

from library.abstract_models import Auth


class StatementBase(Auth, models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        abstract = True


class ElectricGasStatement(StatementBase):
    electric_used = models.PositiveIntegerField(help_text='(in kWh)')
    gas_used = models.PositiveIntegerField(help_text='(in ccf)')
    statement_date = models.DateField()

    class Meta:
        ordering = ['statement_date']
        unique_together = (('user', 'statement_date'),)
        verbose_name = 'electric & gas'
        verbose_name_plural = 'Electric/Gas'

    def __str__(self):
        return f'[{self.statement_date}] Electric: {self.electric_used} kWh, Gas: {self.gas_used} ccf'


class WaterStatement(StatementBase):
    from_date = models.DateField()
    to_date = models.DateField()
    water_used = models.PositiveIntegerField()

    class Meta:
        ordering = ['from_date']
        unique_together = (('user', 'from_date', 'to_date'),)
        verbose_name_plural = 'Water'

    def __str__(self):
        return f'[from {self.from_date} to {self.to_date}] {self.water_used} units'
