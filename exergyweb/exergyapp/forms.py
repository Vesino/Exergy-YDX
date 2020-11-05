from django import forms
from mapwidgets.widgets import GooglePointFieldWidget

from pvlib.pvsystem import retrieve_sam

#Modulo desde la librería de Sandia labs
cec_inverters = retrieve_sam('cecinverter')
#Calcular la potencia CD, aqui debemos tener el diccionario para el tipo de Modulo en CUTonalá
sandia_modules = retrieve_sam('SandiaMod')
    
inverters_list = cec_inverters.columns.tolist()
inverters_list_0 = inverters_list.copy()
inverters_list_0.insert(0, '')
inverters_list_1 = inverters_list.copy()
inverters_list_1.insert(0, 'Choose...')
INVERTERS = tuple(zip(inverters_list_0, inverters_list_1))

modules_list = sandia_modules.columns.tolist()
modules_list_0 = modules_list.copy()
modules_list_0.insert(0, '')
modules_list_1 = modules_list.copy()
modules_list_1.insert(0, 'Choose...')
MODULES = tuple(zip(modules_list_0, modules_list_1))

class location_pv(forms.Form):
    latitude = forms.FloatField()
    longitude = forms.FloatField()
    modules_per_string  = forms.FloatField()
    strings_per_inverter = forms.FloatField()
    module = forms.ChoiceField(choices=MODULES)
    inverter = forms.ChoiceField(choices=INVERTERS)
   # widgets = {
    #        'coordinates': GooglePointFieldWidget,
     #   }
