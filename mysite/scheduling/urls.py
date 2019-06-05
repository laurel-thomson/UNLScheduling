from django.urls import path, include

from .views import scheduling, students, teachers

urlpatterns = [
    path('', scheduling.index, name='index'),

    path('students/', include(([
        path('', students.room_list, name='room_list'),
        path('<int:room_id>/', scheduling.room_detail, name='room_detail'),
        path('<int:room_id>/<int:term_id>/', scheduling.term_schedule, name='time_list'),
    ], 'scheduling'), namespace='students')),

    path('teachers/', include(([
        path('', teachers.room_list, name='room_list'),
        path('<int:room_id>/', scheduling.room_detail, name='room_detail'),
        path('<int:room_id>/<int:term_id>/', scheduling.term_schedule, name='time_list'),
    ], 'scheduling'), namespace='teachers')),
]