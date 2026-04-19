from django_filters import rest_framework as filters

from ..models import BlogPost, Comment


class BaseFilter(filters.FilterSet):
    created_at = filters.DateFilter(field_name='created_at', lookup_expr='exact', label='Дата')
    created_at_gte = filters.DateFilter(field_name='created_at', lookup_expr='gte', label='Дата от')
    created_at_lte = filters.DateFilter(field_name='created_at', lookup_expr='lte', label='Дата до')

    class Meta:
        abstract = True
        fields = ()

    def filter_queryset(self, queryset):
        if self.data.get('created_at'):
            queryset = queryset.filter(created_at__date=self.data.get('created_at'))

        if self.data.get('author__username'):
            queryset = queryset.filter(author__username=self.data.get('author__username'))

        if self.data.get('created_at_gte'):
            queryset = queryset.filter(created_at__gte=self.data.get('created_at_gte'))

        if self.data.get('created_at_lte'):
            queryset = queryset.filter(created_at__lte=self.data.get('created_at_lte'))
        return queryset


class BlogPostFilterSet(BaseFilter):
    class Meta:
        model = BlogPost
        fields = ('author__username', 'created_at',)


class CommentFilter(BaseFilter):
    class Meta:
        model = Comment
        fields = ('author__username', 'created_at')

