from rest_framework import serializers
from .models import PlaceImage, Category, PlaceModel


class PlaceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceImage
        fields = ['url']

    def get_url(self, obj):
        request = self.context.get('request')
        if obj.url and request is not None:
            return request.build_absolute_uri(obj.url.url)
        return obj.url.url if obj.url else None


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'type', 'url'].index()

    def get_url(self, obj):
        request = self.context.get('request')
        if obj.url and request is not None:
            return request.build_absolute_uri(obj.url.url)
        return obj.url.url if obj.url else None


class PlaceListSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = PlaceModel
        fields = ['id', 'name', 'latitude', 'longitude', 'views', 'thumbnail']

    def get_thumbnail(self, obj):
        request = self.context.get('request')
        image = obj.images.first()
        if image is not None:
            return PlaceImageSerializer(image, context={'request': request}).data
        return None


class PlaceSerializer(serializers.ModelSerializer):
    images = PlaceImageSerializer(many=True, read_only=True)
    category = CategorySerializer()

    class Meta:
        model = PlaceModel
        fields = ['id', 'name', 'category', 'latitude', 'longitude', 'description', 'views', 'rating', 'images']


class PlaceMapSerializer(serializers.Serializer):
    type = serializers.CharField(read_only=True, max_length=20)
    thumbnail = PlaceImageSerializer(source='images', required=False, read_only=True)
    count = serializers.IntegerField(required=False, read_only=True)
    places = serializers.ListField(required=False, read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['point'] = {
            'latitude': instance['latitude'],
            'longitude': instance['longitude'],
        }
        return representation


class PlaceModelSerializer(serializers.ModelSerializer):
    url = serializers.ImageField(required=False)

    class Meta:
        model = PlaceModel
        fields = '__all__'
