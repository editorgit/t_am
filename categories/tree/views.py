import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Category


@csrf_exempt
def create_categories(request):
    if request.method == 'POST':
        create_tree_data(json.loads(request.body))
        cnt = Category.objects.count()
        return JsonResponse({'Created categories': cnt})


@csrf_exempt
def get_categories(request, pk):
    result = dict()
    cat_data = Category.objects.get(pk=pk)
    result['id'] = cat_data.pk
    result['name'] = cat_data.name
    result['parents'] = get_parents(cat_data.parent)
    result['children'] = get_children(cat_data)
    result['siblings'] = get_siblings(cat_data)
    return JsonResponse(result)


def create_tree_data(content, parent=None):
    if isinstance(content, dict):
        head = dict(list(content.items())[:2])
        if head:
            parent = Category.objects.create(name=head['name'], parent=parent)
            if head.get('children', None):
                create_tree_data(head['children'], parent=parent)

    elif isinstance(content, list):
        for elem in content:
            create_tree_data(elem, parent=parent)


def get_parents(parent, parents=None):
    if not parents:
        parents = list()

    if hasattr(parent, 'id'):
        parents.append({'id': parent.pk, 'name': parent.name})

    if hasattr(parent, 'parent'):
        get_parents(parent.parent, parents)

    return parents


def get_children(cat_data):
    if not hasattr(cat_data, 'children'):
        return list()
    return [{'id': child.pk, 'name': child.name} for child in cat_data.children.all()]


def get_siblings(cat_data):
    if not hasattr(cat_data, 'parent') or not hasattr(cat_data.parent, 'children'):
        return list()
    return [{'id': child.pk, 'name': child.name} for child in cat_data.parent.children.all() if child.id != cat_data.pk]
