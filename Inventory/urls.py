from django.conf.urls import url
from django.urls import path
from . import views
from .views import *
from django.contrib.auth import views as auth_views



urlpatterns=[
	#URL RAIZ
	url(r'^$', index, name= 'index'),
	#url Homepage
	url(r'^homepage$', homepage, name= "homepage"),

	#URL ADMIN
	path('admin/', auth_views.LoginView.as_view(), name= "admin"),


	#display products
	url(r'^display_products$', display_products, name= "display_products"),
	#display_clients
	url(r'^display_clients$', display_clients, name= "display_clients"),
	#display_movimientos
	url(r'^display_movimientos$', display_movimientos, name= "display_movimientos"),
	#display_remitos
	url(r'^display_remitos$', display_remitos, name= "display_remitos"),
	#display_certificaciones
	url(r'^display_certificaciones$', display_certificaciones, name= "display_certificaciones"),

	#URL PARA AÑADIR OBJETOS
	#add products
	url(r'^add_products$', add_products, name= "add_products"),
	#add_clients
	url(r'^add_clients$', add_clients, name="add_clients"),
	#add_remitos
	url(r'^add_remitos$', views.RemitoCreate.as_view(), name="add_remitos"),
	#add_certificaciones
	url(r'^add_certificaciones$', add_certificaciones, name="add_certificaciones"),


	# URL PARA EDITAR OBJETOS
	#edit product
	path('edit_producto/<int:pk>/', views.edit_producto, name='edit_producto'),
	#edit clients
	path('edit_clients/<int:pk>/', views.edit_clients, name='edit_clients'),
    #edit remitos
    path('edit_remito/<int:pk>/', views.edit_remito, name='edit_remito'),
    #edit certificaciones
    path('edit_certificacion/<int:pk>/', views.edit_certificacion, name='edit_certificacion'),

	# URL PARA ELIMINAR OBJETOS
	#delete producto
	path('delete_producto/<int:pk>/', views.delete_producto, name='delete_producto'),
	#delete clients
	path('delete_clients/<int:pk>/', views.delete_clients, name='delete_clients'),
	#delete remito
	path('delete_remito/<int:pk>/', views.delete_remito, name='delete_remito'),
	#delete certificaciones
	path('delete_certificacion/<int:pk>/', views.delete_certificacion, name='delete_certificacion'),

	#URL PARA IMPRIMIR REMITOS Y CERTIFICACIONES
	path('imprimir/<int:pk>/', views.imprimir, name="imprimir"),
    path('mostrar_remitos_certificacion/<int:pk>/', views.mostrar_remitos_certificacion, name="mostrar_remitos_certificacion"),

]


