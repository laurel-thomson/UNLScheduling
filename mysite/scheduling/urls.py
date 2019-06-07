from django.urls import path, include

from .views import scheduling, students, teachers

urlpatterns = [
    path('', scheduling.index, name='index'),

    path('students/', include(([
        path('', students.room_list, name='room_list'),
        path('<int:room_id>/', students.room_detail, name='room_detail'),
        path('<int:room_id>/<int:term_id>/', students.term_detail, name='term_detail'),
    ], 'scheduling'), namespace='students')),

    path('teachers/', include(([
        path('', teachers.room_list, name='room_list'),
        path('create_room/', teachers.create_room, name='create_room'),
        path('<int:room_id>/create_term/', teachers.create_term, name='create_term'),
        path('<int:room_id>/', teachers.room_detail, name='room_detail'),
        path('<int:room_id>/<int:term_id>/add_time_slot', teachers.add_time_slot, name='add_time_slot'),
        path('<int:room_id>/delete_room/', teachers.delete_room, name='delete_room'),
        path('<int:room_id>/<int:term_id>/delete_term', teachers.delete_term, name='delete_term'),
        path('<int:room_id>/remove_user/<int:user_id>', teachers.remove_user, name='remove_user'),
        path('<int:room_id>/<int:term_id>/finalize/', teachers.finalize_schedule, name='finalize_schedule'),
        path('<int:room_id>/<int:term_id>/unfinalize/', teachers.unfinalize_schedule, name='unfinalize_schedule'),
        path('<int:room_id>/<int:term_id>/', teachers.term_detail, name='term_detail'),
    ], 'scheduling'), namespace='teachers')),
]