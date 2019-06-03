from django.urls import path, include

from .views import scheduling, students, teachers

urlpatterns = [
    path('', scheduling.index, name='index'),

    path('students/', include(([
        path('', students.RoomListView.as_view(), name='student_room_list'),
    ], 'scheduling'), namespace='students')),

    path('teachers/', include(([
        path('', teachers.RoomListView.as_view(), name='teacher_room_list'),
    ], 'scheduling'), namespace='teachers')),
]