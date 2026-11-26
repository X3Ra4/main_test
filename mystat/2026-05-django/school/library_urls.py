from django.db.models import Q
from django.urls import path, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .models import Book, Review

app_name = "library"


def list_view_for(model):
    class Listing(ListView):
        template_name = "school/records.html"
        paginate_by = 10

        def get_queryset(self):
            queryset = model.objects.all()
            query = self.request.GET.get("q", "").strip()
            if model is Book:
                genre = self.request.GET.get("genre", "").strip()
                if query:
                    queryset = queryset.filter(Q(title__icontains=query) | Q(author__icontains=query))
                if genre:
                    queryset = queryset.filter(genre__iexact=genre)
                return queryset.order_by("title", "pk")
            if query:
                queryset = queryset.filter(Q(reader__icontains=query) | Q(book__title__icontains=query))
            return queryset.select_related("book").order_by("-score", "pk")

        def get_context_data(self, **kwargs):
            from urllib.parse import urlencode
            context = super().get_context_data(**kwargs)
            filters = self.request.GET.copy()
            filters.pop("page", None)
            context.update(title=labels[model], prefix=model._meta.model_name, filter_query=urlencode(filters, doseq=True))
            return context

    return Listing.as_view(model=model)


def detail_for(model):
    class Record(DetailView):
        template_name = "school/record.html"

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["prefix"] = model._meta.model_name
            return context

    return Record.as_view(model=model)


labels = {Book: "Книжки", Review: "Відгуки"}
urlpatterns = []
for entity, fields in ((Book, ("title", "author", "genre", "summary")), (Review, ("book", "reader", "score", "text"))):
    prefix = entity._meta.model_name
    root = "" if entity is Book else "reviews/"
    success = reverse_lazy(f"library:{prefix}-list")
    urlpatterns += [
        path(root, list_view_for(entity), name=f"{prefix}-list"),
        path(root + "add/", CreateView.as_view(model=entity, fields=fields, template_name="school/form.html",
             success_url=success), name=f"{prefix}-add"),
        path(root + "<int:pk>/", detail_for(entity), name=f"{prefix}-detail"),
        path(root + "<int:pk>/edit/", UpdateView.as_view(model=entity, fields=fields, template_name="school/form.html",
             success_url=success), name=f"{prefix}-edit"),
        path(root + "<int:pk>/delete/", DeleteView.as_view(model=entity, template_name="school/form.html",
             success_url=success), name=f"{prefix}-delete"),
    ]
