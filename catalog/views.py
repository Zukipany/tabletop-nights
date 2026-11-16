from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from catalog.forms import BoardGameCreateForm, BoardGameDeleteForm, BoardGameEditForm, BoardGameFilterForm
from catalog.models import BoardGame
from common.views import FilteredListMixin, InstanceDeleteFormMixin


class GameListView(FilteredListMixin, ListView):
    model = BoardGame
    template_name = 'catalog/game_list.html'
    context_object_name = 'games'
    paginate_by = 6
    filter_form_class = BoardGameFilterForm

    def apply_filters(self, queryset, data):
        if data.get('q'):
            queryset = queryset.filter(name__icontains=data['q'])
        if data.get('category'):
            queryset = queryset.filter(category=data['category'])
        return queryset.order_by(data.get('sort') or 'name')


class GameDetailView(DetailView):
    model = BoardGame
    template_name = 'catalog/game_detail.html'
    context_object_name = 'game'


class GameCreateView(SuccessMessageMixin, CreateView):
    model = BoardGame
    form_class = BoardGameCreateForm
    template_name = 'catalog/game_form.html'
    success_message = '"%(name)s" was added to the shelf.'


class GameUpdateView(SuccessMessageMixin, UpdateView):
    model = BoardGame
    form_class = BoardGameEditForm
    template_name = 'catalog/game_form.html'
    context_object_name = 'game'
    success_message = 'The game was updated.'


class GameDeleteView(InstanceDeleteFormMixin, DeleteView):
    model = BoardGame
    form_class = BoardGameDeleteForm
    template_name = 'catalog/game_delete.html'
    context_object_name = 'game'
    success_url = reverse_lazy('game-list')

    def form_valid(self, form):
        messages.info(self.request, f'"{self.object}" was removed from the shelf.')
        return super().form_valid(form)
