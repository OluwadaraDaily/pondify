from django.urls import path

from . import views

urlpatterns = [
	path("", views.index, name = "index"),
	path("register", views.register, name = "register"),
	path("login", views.signin, name = "login"),
	path("add_pond", views.add_pond, name = "add_pond"),
	path("<int:pond_id>", views.each_pond, name = "each_pond"),
	path("logout", views.signout, name = "logout")
]