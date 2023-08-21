from .models import Category

def categories(request):
    excluded_category_name = 'default'
    categories = Category.objects.exclude(name=excluded_category_name)
    return {'categories': categories}

