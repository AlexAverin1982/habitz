from rest_framework import serializers
from rest_framework.serializers import ValidationError
from .models import Location, Action, Reward, Habit


class LocationSerializer(serializers.ModelSerializer):
    # video = serializers.URLField(validators=[validate_lesson_video_link_source], required=False)

    class Meta:
        model = Location
        # fields = '__all__'
        fields = ('id', 'name', 'description')


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ('id', 'name', 'description')
        # fields = '__all__'


class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = '__all__'


class HabitSerializer(serializers.ModelSerializer):
    frequency = serializers.IntegerField(min_value=1, max_value=6, required=False)
    duration = serializers.IntegerField(min_value=1, max_value=120, required=False)
    start_date = serializers.DateField(required=False)
    reward = serializers.PrimaryKeyRelatedField(many=False, queryset=Reward.objects.all(), allow_null=True,
                                                required=False)
    chain_habit = serializers.PrimaryKeyRelatedField(many=False, queryset=Habit.objects.filter(is_pleasant=True),
                                                     allow_null=True, required=False)

    # reward = serializers.PrimaryKeyRelatedField(many=False, queryset=Reward.objects.all(), allow_null=True,
    #                                             validators=[validators.validate_self_is_useful,
    #                                                         validators.validate_chain_habit_not_present],
    #                                             required=False)

    class Meta:
        model = Habit
        fields = '__all__'

    def validate(self, data):
        existing_data = self.to_representation(self.instance)
        # print(f"data: {data}")

        reward = data.get('reward')
        chain_habit = data.get('chain_habit')

        if reward:
            if existing_data.get('chain_habit'):
                raise ValidationError("Для привычки уже указана привязанная привычка")
            elif chain_habit:
                raise ValidationError("Неправильно указывать для привычки одновременно награду и связанную привычку")
        elif not chain_habit:
            chain_habit = existing_data.get('chain_habit')
        if chain_habit:
            if existing_data.get('is_pleasant'):
                raise ValidationError("К приятной привычке нельзя привязывать никакую другую привычку")

        frequency = data.get('frequency')
        if frequency and (frequency > 1):
            start_date = data.get('start_date')

            if not start_date:
                start_date = existing_data.get('start_date')
            if not start_date:
                raise ValidationError("Требуется указать начальную дату для не ежедневной привычки.")

        return data

        # print(f"existing_data type: {type(existing_data)}")
        # print(f"existing_data: {existing_data}")
        # print(f"{'/' * 40} validation for initial_data {'/' * 40}")
        # for key, value in initial_data:
        #     print(f"{key}: {value}")
        # # here you can access all values
        # key_id = data['key_id']
        # value_id = data['value_id']
        # # perform you validation
        # if key_id != value_id:
        #     raise serializers.ValidationError("key_id must be equal to value_id")


class HabitStrSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ('__str__',)


class HabitFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'

# class HabitCreateSerializer(serializers.ModelSerializer):
#     frequency = serializers.IntegerField(min_value=1, max_value=6, required=False)
#     duration = serializers.IntegerField(min_value=1, max_value=120, required=False)
#     reward = serializers.PrimaryKeyRelatedField(many=False, queryset=Reward.objects.all(), allow_null=True,
#                                                 validators=[validators.validate_self_is_useful,
#                                                             validators.validate_chain_habit_not_present],
#                                                 required=False)
#     chain_habit = serializers.PrimaryKeyRelatedField(many=False, queryset=Habit.objects.filter(is_pleasant=True),
#                                                      allow_null=True, required=False,
#                                                      validators=[validators.validate_self_is_useful,
#                                                                  validators.validate_reward_not_present])
#
#     class Meta:
#         model = Habit
#         fields = '__all__'

#
# class CourseSerializer(serializers.ModelSerializer):
#     lessons_count = serializers.SerializerMethodField()
#     lessons = LocationSerializer(source='Уроки', many=True, read_only=True)
#     you_have_sub = serializers.SerializerMethodField()
#
#     def get_lessons_count(self, obj):
#         return obj.Уроки.count()
#
#     def get_lessons(self, obj):
#         return obj.Уроки.order_by('seq_number')
#
#     def get_you_have_sub(self, obj):
#         user = None
#         request = self.context.get("request")
#         if request and hasattr(request, "user"):
#             user = request.user
#             return Subscription.objects.filter(user=user, course=obj).exists()
#         else:
#             return False
#
#     class Meta:
#         model = Course
#         fields = "__all__"
#
#
# class SubscriptionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Subscription
#         fields = '__all__'
