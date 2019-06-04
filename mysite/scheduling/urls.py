from django.urls import path, include

from .views import scheduling, students, teachers

app_name = 'scheduling'
urlpatterns = [
    path('', scheduling.index, name='index'),

    path('students/', include(([
        path('', scheduling.room_list, name='student_room_list'),
        path('<int:room_id>/', scheduling.room_detail, name='student_term_list'),
        path('<int:room_id>/<int:term_id>/', scheduling.term_schedule, name='student_time_list'),
    ], 'scheduling'), namespace='students')),

    path('teachers/', include(([
        path('', scheduling.room_list, name='teacher_room_list'),
        path('<int:room_id>/', scheduling.room_detail, name='teacher_term_list'),
        path('<int:room_id>/<int:term_id>/', scheduling.term_schedule, name='student_time_list'),
    ], 'scheduling'), namespace='teachers')),
]