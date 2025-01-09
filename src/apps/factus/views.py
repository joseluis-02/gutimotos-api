import json
from datetime import datetime
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from decouple import config
from django.views.generic import ListView, TemplateView

from .models import AuthToken
from .serializers import AuthTokenSerializer
from utils.services import fetch_login, fetch_invoices, fetch_validate_and_create_invoice

from utils.data_customers import customers
from utils.data_items import items

from .forms import LoginOrRefreshTokenForm
# Lista de facturas
def render_invoices_view(request):
    # Aquí obtenemos en token
    Token = AuthToken.objects.first()
    # Llamar a la API para obtener el token
    response = fetch_invoices(token=Token.access_token)
     
    if response.status_code == 200:
        data = response.json()
        data_only = data['data']['data']
        # Parseamos el JSON a una lista de Python
        # invoices = json.loads(data_only)
        return render(request, 'factus/list_invoices.html', {'invoices': data_only})
        # Redirigir a la lista de tokens
        #return []
        # Cambia 'list_tokens' por el nombre de tu vista de lista
    else:
        # Mostrar error si la API devuelve un error
        messages.error(request, "Error al obtener el token: " + response.json().get('error_description', 'Error desconocido'))
   

    # Renderizamos el template con la lista de objetos
    return redirect('login')

# Crear y validar factura
class create_or_validate_invoice(TemplateView):
    template_name = 'factus/create_or_validate.html'
    def post(self, request, *args, **kwargs):
        # Extraemos los valores de los diferentes campos del formulario
        fecha_hora = request.POST.get('fecha_hora')
        # Convertir la fecha de string a objeto datetime
        date_obj = datetime.fromisoformat(fecha_hora)
        # Formatear la fecha al formato deseado "YYYY-MM-DD"
        formatted_date = date_obj.strftime("%Y-%m-%d")
        
        rango = request.POST.get('tipo_comprobante')
        idventa = request.POST.get('idventa')  # Este podría estar vacío
        idcliente = request.POST.get('idcliente')
        result_customer = next((item for item in customers if item["identification"] == idcliente), None)
        
        total_venta = request.POST.get('total_venta')
        
        # Recuperamos las listas de los artículos (idarticulo, cantidad, precio_venta, descuento)
        idarticulo = request.POST.getlist('idarticulo[]')
        cantidad = request.POST.getlist('cantidad[]')
        precio_venta = request.POST.getlist('precio_venta[]')
        descuento = request.POST.getlist('descuento[]')
        
        observacion = request.POST.get('observation')

        # Preparar los datos de los artículos
        articulos = []
        for i in range(len(idarticulo)):
            articulo = {
                "code_reference": idarticulo[i],
                "name": "producto de prueba 2",
                "quantity": int(cantidad[i]),
                "discount_rate": float(descuento[i]),
                "price": float(precio_venta[i]),
                "tax_rate": "5.00",
                "unit_measure_id": 70,
                "standard_code_id": 1,
                "is_excluded": 0,
                "tribute_id": 1,
                "withholding_taxes": [],
            }
            articulos.append(articulo)
        
        # Aquí puedes procesar los datos, como enviar al servicio o guardarlos en la base de datos
        # Ejemplo: enviamos una respuesta con los datos procesados
        response_data = {
            "numbering_range_id": int(rango),
            "reference_code": "I3",
            "observation": str(observacion),
            "payment_form": "1",
            "payment_due_date": formatted_date,
            "payment_method_code": "10",
            "billing_period": {
                "start_date": "2024-01-10",
                "start_time": "00:00:00",
                "end_date": "2024-02-09",
                "end_time": "23:59:59"
            },
            "customer": result_customer,
            "items": articulos
        }
        # print(response_data)
        # Aquí obtenemos en token
        Token = AuthToken.objects.first()
        print(response_data)
        # Llamar a la API para validar y crear factura
        response = fetch_validate_and_create_invoice(Token.access_token,payload=response_data)
        
        print(response.status_code)
        
        if response.status_code == 201:
            data = response.json()
            print(data.get('status') )
            print(data.get('message') )
            print(data.get('data') )
            
            
            return JsonResponse({'status':'success', 'message':data.get('message'), 'invoice': data.get('data') })
            
            # Redirigir a la lista de tokens
            messages.success(request, "Login exitoso. Token guardado.")
            return redirect('list_tokens')  # Cambia 'list_tokens' por el nombre de tu vista de lista
        else:
            # Mostrar error si la API devuelve un error
            return JsonResponse({'status':'error', 'message':'Error al intentar validar y emitir la factura'})

# Lista de Tokens
class AuthTokenListView(ListView):
    model = AuthToken
    template_name = 'factus/list_token.html'  # Especificamos la plantilla
    context_object_name = 'tokens'  # Nombre de la variable en el contexto

    def get_queryset(self):
        return AuthToken.objects.all()  # Devuelve todos los tokens almacenados

# Login obtener token
def login_or_refresh_token(request):
    if request.method == 'POST':
        form = LoginOrRefreshTokenForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Datos en el cuerpo de la solicitud
            payload = {
                "grant_type": "password",
                "client_id": config('CLIENT_ID'),
                "client_secret": config('CLIENT_SECRET'),
                "username": email,
                "password": password
            }
            
            # Llamar a la API para obtener el token
            response = fetch_login(payload=payload)
            
            if response.status_code == 200:
                data = response.json()
                print(data)
                
                # Eliminar todos los registros existentes
                AuthToken.objects.all().delete()
                print(AuthToken.objects.all())
                # Guardar el token en el modelo
                AuthToken.objects.create(
                    access_token= data.get('access_token'),
                    refresh_token = data.get('refresh_token')
                )
                
                print(AuthToken.objects.all())
                # Redirigir a la lista de tokens
                messages.success(request, "Login exitoso. Token guardado.")
                return redirect('list_tokens')  # Cambia 'list_tokens' por el nombre de tu vista de lista
            else:
                # Mostrar error si la API devuelve un error
                messages.error(request, "Error al obtener el token: " + response.json().get('error_description', 'Error desconocido'))
        else:
            messages.error(request, "Formulario inválido. Por favor verifica los datos ingresados.")
    else:
        form = LoginOrRefreshTokenForm()
    # Renderizar el formulario en caso de GET o error
    return render(request, 'factus/login.html', {'form': form})

# Lista de clientes
def customer_list(request):
    return JsonResponse(customers, safe=False)

# Lista de productos
def items_list(request):
    return JsonResponse(items, safe=False)