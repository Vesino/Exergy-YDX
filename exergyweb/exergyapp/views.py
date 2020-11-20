"""Django libraries"""
from django.shortcuts import HttpResponse, render, redirect
from django.http.response import StreamingHttpResponse
from .forms import location_pv
from marketing.models import Stay_Tuned
from django.template import RequestContext

"""Libraries for functions """
import pandas as pd
from datetime import datetime, date, timedelta   
import dropbox
from pvlib import irradiance, atmosphere, pvsystem
from pvlib.location import Location
from pvlib.forecast import GFS, NAM
from pvlib.pvsystem import retrieve_sam
from pvlib.tracking import SingleAxisTracker
from pvlib.modelchain import ModelChain

import plotly.express as px
from plotly.offline import plot

from tzwhere import tzwhere

import requests
import io

def index(request):
#    return render(None, 'index.html')
    if request.method == "POST":
        email = request.POST["email"]
        name = request.POST["name"]
        new_Stay_tuned = Stay_Tuned()
        new_Stay_tuned.email = email
        new_Stay_tuned.name = name
        new_Stay_tuned.save()


#def sky_cam(request):
    TOKEN = 'Ss5giw2X76IAAAAAAAAUNpW5cbpxT1pHzTL--XHaHW2QLer1iP-CCCqzqi3Mn2jQ'
    dbx = dropbox.Dropbox(TOKEN)

    img_time = datetime.now() - timedelta(hours=1, minutes=30)
    img_time = img_time.strftime("%Y-%m-%d_%H:%M")

    try:
        files_raspberrypi = dbx.files_search("/raspberrypi/exposure_fusion_whole", img_time, max_results=1)
        img_link_raspberrypi = dbx.files_get_temporary_link(files_raspberrypi.matches[0].metadata._path_display_value)  
    except:
        files_raspberrypi = dbx.files_search("/raspberrypi/exposure_fusion_whole", "2020-0", max_results=1)
        img_link_raspberrypi = dbx.files_get_temporary_link(files_raspberrypi.matches[0].metadata._path_display_value)  
   
    files_raspberrypi4_bld4 = dbx.files_search("/raspberrypi4_bld4/exposure_fusion_whole", img_time, max_results=1)  
    img_link_raspberrypi4_bld4 = dbx.files_get_temporary_link(files_raspberrypi4_bld4.matches[0].metadata._path_display_value)  

    context = {'img_link_raspberrypi': img_link_raspberrypi.link,
               'img_datetime_raspberrypi': img_link_raspberrypi.metadata.name[:-4].replace('_', ', '),
               'img_link_raspberrypi4_bld4': img_link_raspberrypi4_bld4.link,
               'img_datetime_raspberrypi4_bld4': img_link_raspberrypi4_bld4.metadata.name[:-4].replace('_', ', '),

               }

    #return render(request, 'sky_cam.html', context)
    return render(request, 'index.html', context)

def undotted_keys(dict):
    """
    Transform dotted keys to undotted keys. This is for the `.tag` key
    in the dict that Dropbox returns.
    """
    return {k.lstrip("."): v for k, v in dict.items()}


def dropbox_list_folder(path):
    """
    Returns a generator of files and subfolders for the given folder.
    """
    #social_auth = user.social_auth.filter(provider="dropbox-oauth2").get()
    session = requests.Session()
    session.headers.update({
        "Authorization": "Bearer {token}".format(token='Ss5giw2X76IAAAAAAAAUNpW5cbpxT1pHzTL--XHaHW2QLer1iP-CCCqzqi3Mn2jQ'),
        "Content-Type": "application/json",
    })
    response = session.post(
        url="https://api.dropboxapi.com/2/files/list_folder",
        json={"path": path},
    )
    response.raise_for_status()
    content = response.json()
    for entry in content['entries']:
        yield undotted_keys(entry)

    while content['has_more']:
        response = session.post(
            url="https://api.dropboxapi.com/2/files/list_folder/continue",
            json={"cursor": content["cursor"]},
        )
        response.raise_for_status()
        content = response.json()
        for entry in content['entries']:
            yield undotted_keys(entry)
            
def iterate_response(r):
    for chunk in r.iter_content(chunk_size=8192):
        yield chunk
    
def all_folders(request):

    folders_raspberrypi4_bld4 = dropbox_list_folder("/raspberrypi4_bld4/exposure_fusion_whole")
    folders_raspberrypi = dropbox_list_folder("/raspberrypi/exposure_fusion_whole")
    context = {
        "folders_raspberrypi4_bld4": folders_raspberrypi4_bld4,
        "folders_raspberrypi": folders_raspberrypi,
    }
    return render(request, "all_folders.html", context)

def download_folder(request):
      TOKEN = 'Ss5giw2X76IAAAAAAAAUNpW5cbpxT1pHzTL--XHaHW2QLer1iP-CCCqzqi3Mn2jQ'
      dbx = dropbox.Dropbox(TOKEN)
      path = request.POST['submit']
      filename = path.split('/')[-1]
      r = dbx.files_download_zip(path)
      response = StreamingHttpResponse(iterate_response(r[1]))
      #r = dbx.files_download(path+'/2020-07-12_09:40:05.jpg')[1]
      #inmemoryfile = io.BytesIO(r.content)
      #response = HttpResponse(r.content, content_type='application/zip')
      response['Content-Type'] = 'application/octet-stream'
      response['Content-Disposition'] = 'attachment; filename=' + filename + '.zip'
      #response['Content-Length'] = len(r.content)
      #response.content = r.content
      #response = FileResponse(r.content, as_attachment=True, filename='test.zip')
      return response

"""If the user correctly enters the data 
    as longitude and latitude, then he can calculate pvlib
    else return in the same page"""
    
def pvlib_location(request):
    if request.method == 'POST':
        formulario = location_pv(request.POST)
        if formulario.is_valid():
            params = formulario.cleaned_data                      
                        
            #Creación del diccionario para las caracteristicas del modulo PV utilizado en Cutonalá
            #Canadian_Solar_CS6X_320P___2016_ = {"Vintage": 2016, "Area":1.91 , "Material": "Poly-crystalline", "Cells_in_Series": 72, "Parallel_Strings": 1,
             #       "Isco":9.26, "Voco":45.3, "Impo":8.69, "Vmpo":36.8, "Aisc":0.000397, "Aimp":0.000181, "C0":1.01284, "C1":-0.0128398, "Bvoco":-0.21696,
              #      "Mbvoc":0, "Bvmpo":-0.235488, "Mbvmp":0, "N":1.4032, "C2":0.279317, "C3":-7.24463, "A0":0.928385, "A1":0.068093, "A2":-0.0157738, "A3":0.0016605999999999997,
               #     "A4":-6.929999999999999e-05, "B0":1, "B1":-0.002438, "B2":0.0003103, "B3":-1.246e-05, "B4":2.1100000000000002e-07, "B5":-1.36e-09, "DTC":3.0, "FD":1, "A":-3.4064099999999997, "B":-0.0842075, "C4":0.9964459999999999,
                #    "C5":0.003554, "IXO":4.97599, "IXXO":3.18803, "C6":1.15535, "C7":-0.155353, "Notes":"caracteristicas del modulo instalado en CUT"}
            
            #module = pd.Series(Canadian_Solar_CS6X_320P___2016_, name="Canadian_Solar_CS6X_320P___2016_")
            
            #Modulo desde la librería de Sandia labs
            #cec_inverters = retrieve_sam('cecinverter')
            #inverter = cec_inverters['SMA_America__SC630CP_US_315V__CEC_2012_']
            
            modules_per_string = params['modules_per_string']
            strings_per_inverter = params['strings_per_inverter']
            module = params['module']
            inverter = params['inverter']

            request.session['modules_per_string'] = modules_per_string
            request.session['strings_per_inverter'] = strings_per_inverter
            request.session['module'] = module
            request.session['inverter'] = inverter
            
            #Calcular la potencia CD, aqui debemos tener el diccionario para el tipo de Modulo en CUTonalá
            sandia_modules = retrieve_sam('SandiaMod')
            
            #### Modulo desde la librería de Sandia labs
            cec_inverters = retrieve_sam('cecinverter')

            # Lugar Tonalá
            latitude, longitude = params['latitude'], params['longitude']
           
            request.session['latitude'] = latitude
            request.session['longitude'] = longitude

            tz = tzwhere.tzwhere().tzNameAt(latitude, longitude) 
            
            request.session['timezone'] = tz

            # Parametros de la granja solar
            surface_tilt = 30
            surface_azimuth = 180  # pvlib uses 0=North, 90=East, 180=South, 270=West convention
            albedo = 0.2
            # Rango de tiempo
            start = pd.Timestamp(date.today(), tz=tz)
            # Pronostico a 3 días en adelante
            end = start + pd.Timedelta(days=5)
            
            module = pd.Series(sandia_modules[module])
    
            inverter = cec_inverters[inverter]
            
            # model a big tracker for more fun
            system = SingleAxisTracker(module_parameters=module,
                                        inverter_parameters=inverter,
                                        modules_per_string=modules_per_string,
                                        strings_per_inverter=strings_per_inverter)
             
            
            # fx is a common abbreviation for forecast
            fx_model = GFS()
            
            fx_data = fx_model.get_processed_data(latitude, longitude, start, end)
            
            # use a ModelChain object to calculate modeling intermediates
            mc = ModelChain(system, fx_model.location)
            
            # extract relevant data for model chain
            mc.run_model(fx_data.index, weather=fx_data);
            #mc.run_model(fx_data)
            
            AC = mc.ac.fillna(0);
            #AC = pd.DataFrame(AC)
            
            #labeles = AC.keys()

            #valores = AC.values()

            #data = {
            #    "Dates": labeles,
            #    "Power (W)": valores,
            #}
            #here we print the data the correct thing would be to use them to graph them
            #print(AC.head())

            #return render(request, 'chart.html', {'forma': formulario})
            
            template = 'chart.html'
            #columns = [{'field': 'date', 'title': 'Date'}, {'field': 'value', 'title': 'Value'}]
            #Write the DataFrame to JSON (as easy as can be)
            #json = AC.to_json(orient='records')  # output just the records (no fieldnames) as a collection of tuples
            #Proceed to create your context object containing the columns and the data
            #context = {
             #          'data': json,
              #         'columns': columns
               #       }
            #And render it!
            #return render(request, template, context)
            AC = AC.reset_index()
            AC.rename(columns={'index': 'Time', 0: 'AC Power (W)'}, inplace=True)
            figure = px.line(AC, x='Time', y='AC Power (W)')
            #figure.update_layout(title="Your 5 days AC power output forecast (W)", font=dict(size=20, color='black'))
            #figure.update_xaxes(title_font=dict(size=16, color='black'))
            #figure.update_yaxes(title_font=dict(size=16, color='black'))
            figure.update_xaxes(dtick=10800000)

            plot_div = plot(figure, image_height='100%', output_type='div', include_plotlyjs=False)
            
            context = {'linechart': plot_div}
            
            return render(request, template, context)
    else:
        formulario = location_pv()

    return render(request,'forecast_data.html', {'form': formulario})


def download_forecasts(request):
    modules_per_string = request.session['modules_per_string']
    strings_per_inverter = request.session['strings_per_inverter']
    module = request.session['module']
    inverter = request.session['inverter']
    latitude = request.session['latitude']
    longitude = request.session['longitude']
    tz = request.session['timezone']

    sandia_modules = retrieve_sam('SandiaMod')
    cec_inverters = retrieve_sam('SandiaInverter')

    # Parametros de la granja solar
    surface_tilt = 30
    surface_azimuth = 180  # pvlib uses 0=North, 90=East, 180=South, 270=West convention
    albedo = 0.2
    # Rango de tiempo
    start = pd.Timestamp(date.today(), tz=tz)
    # Pronostico a 3 días en adelante
    end = start + pd.Timedelta(days=3)
    
    module = pd.Series(sandia_modules[module])
    inverter = cec_inverters[inverter]
    
    # model a big tracker for more fun
    system = SingleAxisTracker(module_parameters=module,
                                inverter_parameters=inverter,
                                modules_per_string=modules_per_string,
                                strings_per_inverter=strings_per_inverter)
             
            
    # fx is a common abbreviation for forecast
    fx_model = GFS()
            
    fx_data = fx_model.get_processed_data(latitude, longitude, start, end)
            
    # use a ModelChain object to calculate modeling intermediates
    mc = ModelChain(system, fx_model.location)
            
    # extract relevant data for model chain
    mc.run_model(fx_data.index, weather=fx_data);
            
    AC = mc.ac.fillna(0);

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=AC_5days_forecasts.csv'

    AC.to_csv(path_or_buf=response,sep=';',float_format='%.2f',index=True,decimal=",")
    return response

    
