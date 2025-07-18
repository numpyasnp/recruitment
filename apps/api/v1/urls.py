from django.urls import include, path


app_name = "v1"

urlpatterns = [path("hr-users", include("apps.api.v1.hr_user.urls"))]
