from django.contrib import admin

from .models import ElectricGasStatement, WaterStatement


class YearFilter(admin.SimpleListFilter):
    title = 'year'
    parameter_name = 'year'

    def lookups(self, request, model_admin):
        years = model_admin.model.objects.dates(self.field_name, 'year')
        return [(year.year, year.year) for year in years]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(**{f'{self.field_name}__year': self.value()})
        return queryset


class ElectricGasYearFilter(YearFilter):
    field_name = 'statement_date'


class WaterYearFilter(YearFilter):
    field_name = 'from_date'


@admin.register(ElectricGasStatement)
class ElectricGasStatementAdmin(admin.ModelAdmin):
    list_filter = (ElectricGasYearFilter,)


@admin.register(WaterStatement)
class WaterStatementAdmin(admin.ModelAdmin):
    list_filter = (WaterYearFilter,)
