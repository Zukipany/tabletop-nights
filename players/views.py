from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError, Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from common.views import FilteredListMixin, InstanceDeleteFormMixin
from players.forms import PlayerCreateForm, PlayerDeleteForm, PlayerEditForm, PlayerFilterForm
from players.models import Player


class PlayerListView(FilteredListMixin, ListView):
    model = Player
    template_name = 'players/player_list.html'
    context_object_name = 'players'
    paginate_by = 8
    filter_form_class = PlayerFilterForm

    def get_queryset(self):
        return super().get_queryset().select_related('favorite_game')

    def apply_filters(self, queryset, data):
        if data.get('q'):
            queryset = queryset.filter(Q(nickname__icontains=data['q']) | Q(full_name__icontains=data['q']))
        if data.get('level'):
            queryset = queryset.filter(skill_level=data['level'])
        return queryset


class PlayerDetailView(DetailView):
    model = Player
    template_name = 'players/player_detail.html'
    context_object_name = 'player'


class PlayerCreateView(SuccessMessageMixin, CreateView):
    model = Player
    form_class = PlayerCreateForm
    template_name = 'players/player_form.html'
    success_message = 'Welcome to the table, %(nickname)s!'


class PlayerUpdateView(SuccessMessageMixin, UpdateView):
    model = Player
    form_class = PlayerEditForm
    template_name = 'players/player_form.html'
    context_object_name = 'player'
    success_message = 'Player profile updated.'


class PlayerDeleteView(InstanceDeleteFormMixin, DeleteView):
    model = Player
    form_class = PlayerDeleteForm
    template_name = 'players/player_delete.html'
    context_object_name = 'player'
    success_url = reverse_lazy('player-list')

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
        except ProtectedError:
            messages.error(self.request, f'{self.object} is hosting game nights. Cancel or re-host them first.')
            return redirect(self.object)
        messages.info(self.request, f'{self.object} left the group.')
        return response
