import random

from django.db.models import QuerySet
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from characters.models import Character
from characters.serializers import CharacterSerializer
from pagination import CharacterListPagination


@extend_schema(responses={status.HTTP_200_OK: CharacterSerializer})
@api_view(["GET"])
def get_random_character_view(request: Request) -> Response:
    """Get random character from Rick and Morty world."""
    pks = Character.objects.values_list("pk", flat=True)
    random_pk = random.choice(pks)
    random_character = Character.objects.get(pk=random_pk)

    serializer = CharacterSerializer(random_character)

    return Response(serializer.data, status=status.HTTP_200_OK)


class CharacterListView(generics.ListAPIView):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
    pagination_class = CharacterListPagination

    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset()
        name = self.request.query_params.get("name")

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="name",
                type=OpenApiTypes.STR,
                description="Filter by name insensitive contains (ex. &name=Bob)",
                required=False,
            )
        ]
    )
    def get(self, request, *args, **kwargs) -> Response:
        """List characters with filter by name."""
        return super().get(request, *args, **kwargs)
