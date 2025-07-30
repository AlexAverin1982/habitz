from rest_framework import viewsets, generics, mixins
from rest_framework.permissions import IsAuthenticated

from tracker.models import Location, Action, Habit
from tracker.paginators import CommonPaginator
from tracker.serializers import LocationSerializer, ActionSerializer, HabitSerializer, \
    HabitStrSerializer, HabitFullSerializer
from users.permissions import IsModerator, IsOwner


class LocationViewSet(viewsets.ModelViewSet):
    """
       create:
       Добавление места

       retrieve:
       Получить информацию по конкретному месту

       list:
       Список мест (опционально - номер страницы с результатами)

       update:
       Обновить информацию по конкретному месту

       partial_update:
       Частично обновить информацию по конкретному месту

       delete:
       Удалить место

    """
    serializer_class = LocationSerializer
    # queryset = Location.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CommonPaginator

    def get_permissions(self):
        # if self.action in ['create']:
        #     self.permission_classes = [IsAuthenticated, ~IsModerator, ]
        # elif self.action in ['retrieve', 'update']:
        #     self.permission_classes = (IsAuthenticated, IsModerator | IsOwner)
        # elif self.action in ['destroy']:
        #     self.permission_classes = (IsAuthenticated, IsOwner,)
        # else:
        #     self.permission_classes = [IsAuthenticated]
        self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Location.objects.filter(owner=self.request.user)

    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)

    # def update(self, request, *args, **kwargs):
    """
    Вызов задачи на отправку сообщения должен происходить в контроллере обновления места:
    когда мест обновлен — тем, кто подписан на обновления именно этого места, отправляется письмо на почту.
    """
    # course_id = kwargs.get('pk')
    # # print('='*100)
    # notify_users_of_course_updated.delay(course_id)
    # print('(' * 100)
    # subs = result.get()
    # for s in subs:
    #     print(s)

    # self.object = self.get_object()
    # # print(f"kwargs: {kwargs}")
    # serializer = self.get_serializer(data=request.data)
    #
    # if serializer.is_valid():
    #     super(LocationViewSet, self).update(request, *args, **kwargs)
    #     response = {
    #         'status': 'success',
    #         'code': status.HTTP_200_OK,
    #         'message': f'The course {str(self.object)} updated successfully',
    #         'data': []
    #     }
    #
    #     return Response(response)
    #
    # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActionViewSet(viewsets.ModelViewSet):
    """
       create:
       Добавление действия

       retrieve:
       Получить информацию по конкретному действию

       list:
       Список действий (опционально - номер страницы с результатами)

       update:
       Обновить информацию по конкретному действию

       partial_update:
       Частично обновить информацию по конкретному действию

       delete:
       Удалить действие

    """
    serializer_class = ActionSerializer
    # queryset = Action.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CommonPaginator

    def get_queryset(self):
        return Action.objects.filter(owner=self.request.user)

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


###############################################################################

class CreateHabit(generics.CreateAPIView):
    """
    создание привычки
    """
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class HabitListAPIView(generics.ListAPIView):
    """
    Список привычек, включая чужие опубликованные привычки
    """
    serializer_class = HabitStrSerializer

    permission_classes = [IsAuthenticated]
    pagination_class = CommonPaginator

    def get(self, request, *args, **kwargs):
        user = request.user
        # records = (query1 | query2).distinct()
        self.queryset = (Habit.objects.filter(owner=user) | Habit.objects.filter(is_public=True)).distinct()
        return super(HabitListAPIView, self).get(request, *args, **kwargs)


class MyHabitListAPIView(generics.ListAPIView):
    """
    Список привычек только владельца
    """
    serializer_class = HabitStrSerializer

    permission_classes = [IsAuthenticated]
    pagination_class = CommonPaginator

    def get(self, request, *args, **kwargs):
        self.queryset = Habit.objects.filter(owner=request.user)
        return super(MyHabitListAPIView, self).get(request, *args, **kwargs)

    def get_serializer_class(self):
        dataset_is_full = self.kwargs.get('full', False)
        if dataset_is_full:
            return HabitFullSerializer
        else:
            return HabitStrSerializer


class HabitPartialUpdateAPIView(generics.GenericAPIView, mixins.UpdateModelMixin):
    """
    Частично обновить привычку
    """
    # queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]

    def get_queryset(self):
        # return Habit.objects.filter(owner=self.request.user)
        # for item in dir(self):
        #     print(item)
        return Habit.objects.filter(owner=self.request.user)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """
    Данные конкретной привычки
    """
    serializer_class = HabitSerializer
    # queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]

    def get_queryset(self):
        return Habit.objects.filter(owner=self.request.user)


class HabitDestroyAPIView(generics.DestroyAPIView):
    """
    Удалить привычку
    """
    serializer_class = HabitSerializer
    # queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Habit.objects.filter(owner=self.request.user)
