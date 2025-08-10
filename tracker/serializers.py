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
    name = serializers.CharField(required=False)
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


class HabitStrSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ('__str__',)


class HabitFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
