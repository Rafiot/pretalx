from django.views.generic import ListView

from pretalx.common.views import ActionFromUrl, CreateOrUpdateView
from pretalx.orga.authorization import OrgaPermissionRequired
from pretalx.orga.forms import SpeakerForm
from pretalx.person.models import User


class SpeakerList(OrgaPermissionRequired, ListView):
    template_name = 'orga/speaker/list.html'
    context_object_name = 'speakers'
    model = User

    def get_queryset(self):
        return User.objects\
            .filter(submissions__in=self.request.event.submissions.all())\
            .order_by('id')\
            .distinct()


class SpeakerDetail(OrgaPermissionRequired, ActionFromUrl, CreateOrUpdateView):
    template_name = 'orga/speaker/form.html'
    form_class = SpeakerForm
    model = User

    def get_object(self):
        return User.objects\
            .filter(submissions__in=self.request.event.submissions.all())\
            .order_by('id')\
            .distinct()\
            .get(pk=self.kwargs['pk'])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['read_only'] = True
        return kwargs

    def get_context_data(self):
        ctx = super().get_context_data()
        ctx['submission_count'] = User.objects.filter(submissions__in=self.request.event.submissions.all()).count()
        return ctx