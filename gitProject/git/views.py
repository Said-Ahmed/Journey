import math
from itertools import groupby

from rest_framework import status
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


from .models import Category, PlaceImage, PlaceModel
from .serializers import PlaceModelSerializer, PlaceSerializer, CategorySerializer, PlaceMapSerializer, \
    PlaceListSerializer


class CreatePlaceView(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        place_serializer = PlaceModelSerializer(
            data=request.data
        )
        if place_serializer.is_valid(raise_exception=True):
            image = place_serializer.validated_data.pop('url')
            place = PlaceModel.objects.create(
                **place_serializer.validated_data
            )
            place_data = place_serializer.data.copy()
            if image:
                image = PlaceImage.objects.create(
                    place_id=place.id,
                    url=image
                )
                place_data['image'] = image.url.url
            return Response(place_data, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)


class GetPlacesView(generics.ListAPIView):
    queryset = PlaceModel.objects.all()
    serializer = PlaceSerializer


class GetPlacesByIds(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        places_ids_str = request.GET.get('places_ids')
        places_ids = [int(pk.strip()) for pk in places_ids_str.split(',')]
        if len(places_ids) > 1:
            places = PlaceModel.objects.filter(id__in=places_ids)
        else:
            places = PlaceModel.objects.filter(id=places_ids[0])
        place_serializer = PlaceListSerializer(
            places,
            context={'request': request},
            many=True
        )
        return Response(place_serializer.data, status=status.HTTP_200_OK)


class PlaceDetail(generics.RetrieveAPIView):
    serializer_class = PlaceSerializer
    lookup_field = 'pk'
    queryset = PlaceModel.objects.all()

    def get_object(self):
        instance = super().get_object()
        instance.increment_view_count()
        return instance


class PlaceListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 50


class SearchPlaces(generics.ListAPIView):
    pagination_class = PlaceListPagination
    serializer_class = PlaceSerializer

    def get_queryset(self):
        queryset = PlaceModel.objects.filter(
            name__contains=self.request.GET.get(
                'text', ':)'
            )
        )
        return queryset


class GetPlaceMapView(generics.ListAPIView):
    @staticmethod
    def get_quadkey(lat, lng, zoom):
        x = int((lng + 180) / 360 * (1 << zoom))
        y = int(
            (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * (1 << zoom))
        quadkey = ''
        for i in range(zoom, 0, -1):
            digit = 0
            mask = 1 << (i - 1)
            if (x & mask) != 0:
                digit += 1
            if (y & mask) != 0:
                digit += 2
            quadkey += str(digit)
        return quadkey

    def get(self, request, *args, **kwargs):
        top_left_latitude = float(request.query_params.get('top_left_latitude'))
        top_left_longitude = float(request.query_params.get('top_left_longitude'))
        bottom_right_latitude = float(request.query_params.get('bottom_right_latitude'))
        bottom_right_longitude = float(request.query_params.get('bottom_right_longitude'))
        map_zoom = int(request.query_params.get('zoom'))
        zoom = 23
        while (self.get_quadkey(top_left_latitude, top_left_longitude, zoom=zoom) !=
               self.get_quadkey(bottom_right_latitude, bottom_right_longitude, zoom=zoom)):
            zoom -= 1
        quadkey = self.get_quadkey(
            top_left_latitude,
            top_left_longitude,
            zoom=zoom
        )
        places_in_range = PlaceModel.objects.filter(quadkey__startswith=quadkey)
        grouped_objects = []
        for _, group in groupby(places_in_range, key=lambda place_cnt: place_cnt.quadkey[:map_zoom + 2]):
            places = list(group)
            latitude = 0
            longitude = 0
            for place in places:
                latitude += place.latitude
                longitude += place.longitude
            avg_latitude = latitude / len(places)
            avg_longitude = longitude / len(places)
            if len(places) > 1:
                grouped_objects.append(
                    {
                        'type': 'CLUSTER',
                        'latitude': avg_latitude,
                        'longitude': avg_longitude,
                        'count': len(places),
                        'places': [place.id for place in places]
                    }
                )
            else:
                place = places[0]
                grouped_objects.append(
                    {
                        'id': place.id,
                        'type': 'PLACE',
                        'latitude': place.latitude,
                        'longitude': place.longitude,
                        'images': place.images.first()
                    },
                )
        serializer_data = PlaceMapSerializer(
            grouped_objects,
            many=True,
            context={'request': request}
        )
        return Response(serializer_data.data, status=status.HTTP_200_OK)


class GetCategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


