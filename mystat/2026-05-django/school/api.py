from rest_framework import serializers, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Battle, Character


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ("id", "name", "hp", "attack", "defense")


class BattleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Battle
        fields = ("id", "occurred_at", "first", "second", "winner", "rounds")


class BattleRequest(serializers.Serializer):
    character_1 = serializers.PrimaryKeyRelatedField(queryset=Character.objects.all())
    character_2 = serializers.PrimaryKeyRelatedField(queryset=Character.objects.all())

    def validate(self, values):
        if values["character_1"] == values["character_2"]:
            raise serializers.ValidationError("Потрібні два різні персонажі.")
        return values


class CharacterViewSet(viewsets.ModelViewSet):
    queryset = Character.objects.order_by("id")
    serializer_class = CharacterSerializer


class BattleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Battle.objects.order_by("-occurred_at", "-id")
    serializer_class = BattleSerializer


@api_view(["POST"])
def battle(request):
    payload = BattleRequest(data=request.data)
    payload.is_valid(raise_exception=True)
    first, second = (payload.validated_data[key] for key in ("character_1", "character_2"))
    hp = {first.pk: first.hp, second.pk: second.hp}
    turns = ((first, second), (second, first))
    log = []
    round_number = 0
    while hp[first.pk] > 0 and hp[second.pk] > 0:
        round_number += 1
        for source, target in turns:
            damage = max(source.attack - target.defense, 1)
            hp[target.pk] -= damage
            log.append(f"Round {round_number}: {source.name} dealt {damage} damage")
            if hp[target.pk] <= 0:
                winner = source.name
                break
    Battle.objects.create(first=first.name, second=second.name, winner=winner, rounds=round_number)
    return Response({"winner": winner, "rounds": round_number, "battle_log": log}, status=status.HTTP_200_OK)
