from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'common/home.html'


class FilteredListMixin:
    """Validates a GET filter form and lets the subclass narrow the queryset."""

    filter_form_class = None

    def get_filter_form(self):
        return self.filter_form_class(self.request.GET or None)

    def apply_filters(self, queryset, data):
        raise NotImplementedError('Subclasses must implement apply_filters().')

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filter_form = self.get_filter_form()
        if self.filter_form.is_valid():
            return self.apply_filters(queryset, self.filter_form.cleaned_data)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.filter_form
        return context


class InstanceDeleteFormMixin:
    """Shows the object in a disabled form on the delete confirmation page."""

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.object
        return kwargs
