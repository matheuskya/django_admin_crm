from django.contrib import admin
from crm.models import *

# Register your models here.

# admin.site.register(Cliente)

for model in [Cliente, Lead, Interacao, Oportunidade, Vendedor, Tarefa]:
    admin.site.register(model)
