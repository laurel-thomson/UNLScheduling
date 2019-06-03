from django.urls import path, include

from .views import scheduling, students, teachers

app_name = 'scheduling'
urlpatterns = [
    path('', scheduling.index, name='index'),

    path('students/', include(([
        path('', scheduling.RoomListView.as_view(), name='student_room_list'),
        path('<int:room_id>/', scheduling.TermListView.as_view(), name='student_term_list'),
        path('<int:room_id>/<int:term_id>/', scheduling.term_schedule, name='student_time_list'),
    ], 'scheduling'), namespace='students')),

    path('teachers/', include(([
        path('', scheduling.RoomListView.as_view(), name='teacher_room_list'),
        path('<int:room_id>/', scheduling.TermListView.as_view(), name='teacher_term_list'),
        path('<int:room_id>/<int:term_id>/', scheduling.term_schedule, name='student_time_list'),
    ], 'scheduling'), namespace='teachers')),
]