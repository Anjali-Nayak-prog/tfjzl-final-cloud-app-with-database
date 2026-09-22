from django.contrib import admin
from django.urls import path
from onlinecourseapp import views


urlpatterns = [
    path('admin/', admin.site.urls),

    path(
        'course/<int:course_id>/submit/',
        views.submit,
        name='submit'
    ),

    path(
        'course/<int:course_id>/result/<int:submission_id>/',
        views.show_exam_result,
        name='show_exam_result'
    ),
]