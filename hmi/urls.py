"""
URL configuration for hmi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from login import urls as loginurl
from login import views as loginviews
from ocr_medical_record import urls as ocrurl
from book_appointment import urls as bookappointmenturl
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login',loginviews.login_),
    path('register',include(loginurl)),
    path('digitalize_record',include(ocrurl)),
    path('book-appointment',include(bookappointmenturl))
]
