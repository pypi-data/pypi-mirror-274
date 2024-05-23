from django.shortcuts import render
from django_utilsds import utils
from _data import zenblogds

from hitcount.views import HitCountDetailView
from django.views import generic
from .forms import SearchForm
from .models import Post, CATEGORY
from django.core.exceptions import ObjectDoesNotExist

num_pagination = 6

template_name = zenblogds.context['template_name']
c = zenblogds.context


def make_page_bundle(page_range, n=5):
    # 전체 페이지를 n 개수의 묶음으로 만든다.
    # pagination에 사용
    l = [i for i in page_range]
    return [l[i:i + n] for i in range(0, len(l), n)]


def robots(request):
    from django.shortcuts import HttpResponse
    file_content = utils.make_robots()
    return HttpResponse(file_content, content_type="text/plain")


def home(request):
    c.update({
        'category': CATEGORY,
    })
    # 포스트가 하나도 없으면 에레가 나기때문에 방지용으로..
    try:
        test = Post.objects.filter(status=1).latest('updated_on')
    except ObjectDoesNotExist:
        test = Post(
            title='test',
            slug='test',
            author_id=1,
            content='test',
            status=1,
        )
        test.save()

    return render(request, template_name + '/index.html', c)


def about(request):
    return render(request, template_name + '/about.html', c)


def contact(request):
    return render(request, template_name + '/contact.html', c)


class PostDetailView(HitCountDetailView):
    model = Post
    template_name = template_name + '/single-post.html'
    context_object_name = 'object'
    slug_field = 'slug'
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(c)
        return context


class SearchResult(generic.ListView):
    template_name = template_name + '/search-result.html'
    paginate_by = num_pagination

    def get_queryset(self):
        form = SearchForm(self.request.GET)
        if form.is_valid():
            q = form.cleaned_data['q']
        else:
            q = ''
        return Post.objects.filter(content__contains='' if q is None else q).filter(status=1).order_by('-updated_on')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pages_devided = make_page_bundle(context['paginator'].page_range)

        # 현재 페이지에 해당하는 묶음을 page_bundle로 전달한다.
        for page_bundle in pages_devided:
            if context['page_obj'].number in page_bundle:
                context['page_bundle'] = page_bundle

        context.update(c)
        return context


class SearchTag(SearchResult):
    def get_queryset(self):
        # https://stackoverflow.com/questions/56067365/how-to-filter-posts-by-tags-using-django-taggit-in-django
        return Post.objects.filter(tags__name__in=[self.kwargs['tag']]).filter(status=1).order_by('-updated_on')


class Category(SearchResult):
    template_name = template_name + '/category.html'

    def get_queryset(self):
        return Post.objects.filter(status=1).filter(category=self.kwargs['category_int']).order_by('-updated_on')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        for i, name in CATEGORY:
            if self.kwargs['category_int'] == i:
                category_name = name
                break

        context.update({
            'selected_category': category_name,
        })
        return context
