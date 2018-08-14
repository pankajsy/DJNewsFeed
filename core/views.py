from django.views.generic import TemplateView, CreateView, ListView
from braces.views import LoginRequiredMixin, StaffuserRequiredMixin

class Feed(LoginRequiredMixin, TemplateView):
    template_name = "core/feed.html"
    title = "Feed"
    login_url = 'account:admin_login'

    def get_context_data(self, **kwargs):
        context = super(Feed, self).get_context_data(**kwargs)
        # users = Userprofile.objects.all()
        # if users.count() > 0:
        #     paginator = Paginator(users, 20)
        #     page = self.request.GET.get('userspage')
        #     try:
        #         final_users = paginator.page(page) #
        #     except PageNotAnInteger:
        #         final_users = paginator.page(1)
        #     except EmptyPage:
        #         final_users = paginator.page(paginator.num_pages)
        #     context['users'] = final_users
        return context