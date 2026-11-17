from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count, Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from common.views import FilteredListMixin, InstanceDeleteFormMixin
from nights.forms import GameNightCreateForm, GameNightDeleteForm, GameNightEditForm, GameNightFilterForm
from nights.models import GameNight


class NightListView(FilteredListMixin, ListView):
    model = GameNight
    template_name = 'nights/night_list.html'
    context_object_name = 'nights'
    paginate_by = 6
    filter_form_class = GameNightFilterForm

    def get_queryset(self):
        return (super().get_queryset()
                .select_related('host')
                .prefetch_related('games')
                .annotate(attendee_count=Count('attendees')))

    def get_filter_form(self):
        return self.filter_form_class(self.request.GET or {'when': 'upcoming'})

    def apply_filters(self, queryset, data):
        when = data.get('when') or 'upcoming'
        if when == 'upcoming':
            queryset = queryset.upcoming()
        elif when == 'past':
            queryset = queryset.past()
        if data.get('q'):
            queryset = queryset.filter(Q(title__icontains=data['q']) | Q(location__icontains=data['q']))
        return queryset


class NightDetailView(DetailView):
    model = GameNight
    template_name = 'nights/night_detail.html'
    context_object_name = 'night'

    def get_queryset(self):
        return super().get_queryset().select_related('host').prefetch_related('games', 'attendees')


class NightCreateView(SuccessMessageMixin, CreateView):
    model = GameNight
    form_class = GameNightCreateForm
    template_name = 'nights/night_form.html'
    success_message = '"%(title)s" is on the calendar!'

    def get_initial(self):
        initial = super().get_initial()
        if 'game' in self.request.GET:
            initial['games'] = [self.request.GET['game']]
        return initial


class NightUpdateView(SuccessMessageMixin, UpdateView):
    model = GameNight
    form_class = GameNightEditForm
    template_name = 'nights/night_form.html'
    context_object_name = 'night'
    success_message = 'Game night updated.'


class NightDeleteView(InstanceDeleteFormMixin, DeleteView):
    model = GameNight
    form_class = GameNightDeleteForm
    template_name = 'nights/night_delete.html'
    context_object_name = 'night'
    success_url = reverse_lazy('night-list')

    def form_valid(self, form):
        messages.info(self.request, f'"{self.object.title}" was cancelled.')
        return super().form_valid(form)
