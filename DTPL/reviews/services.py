from django.db.models import Avg, Count
from .models import Review


def get_review_summary_for_instance(instance):
    queryset = Review.objects.filter(
        content_type__app_label=instance._meta.app_label,
        content_type__model=instance._meta.model_name,
        object_id=instance.pk,
        is_approved=True,
    )

    aggregate = queryset.aggregate(avg_rating=Avg('rating'), total_reviews=Count('id'))
    avg_rating = aggregate['avg_rating'] or 0
    total_reviews = aggregate['total_reviews'] or 0

    return {
        'reviews': queryset,
        'avg_rating': round(avg_rating, 1) if total_reviews else 0,
        'avg_rating_int': int(round(avg_rating)) if total_reviews else 0,
        'total_reviews': total_reviews,
        'rating_breakdown': {
            stars: queryset.filter(rating=stars).count() for stars in range(5, 0, -1)
        },
    }