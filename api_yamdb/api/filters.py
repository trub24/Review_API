import django_filters as filters

from reviews.models import Title


class TitleFilter(filters.FilterSet):
    genre = filters.CharFilter(field_name='genre__slug')
    category = filters.CharFilter(field_name='category__slug')
    name = filters.CharFilter()

    class Meta:
        model = Title
        fields = ('genre', 'category', 'year', 'name')
