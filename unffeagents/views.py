from django.shortcuts import render
from .models import (AgentProfile, Market, MarketPrice, Notice,CallRsponse,Call)
from .serializers import (AgentProfileSerializer, MarketSerializer, MarketPriceSerializer, 
NoticeSerializer,CallSerializer,ResponseSerializer)
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from rest_framework.views import APIView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.permissions import IsAuthenticated
from .forms import (AgentProfileForm, NoticeForm,EnquiryForm)
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.http import (HttpResponseRedirect,JsonResponse, HttpResponse,
                         Http404)

from django.views.generic import (
    CreateView, UpdateView, DetailView, TemplateView, View, DeleteView)
from rest_framework import filters
from django.contrib.auth.models import User, Group
import requests


# views for agentprofiles
class AgentProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows agentprofiles to be viewed or edited.
    """
    queryset = AgentProfile.objects.all().order_by('specific_role')
    serializer_class = AgentProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class AgentProfileList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'agentprofile_list.html'

    def get(self, request):
        queryset = AgentProfile.objects.order_by('specific_role')
        return Response({'agentprofiles': queryset})


class CreateAgentProfile(LoginRequiredMixin,CreateView):
    template_name = 'create_agentprofile.html'
    success_url = reverse_lazy('unffeagents:agentprofile_list')
    form_class = AgentProfileForm
    success_message = "Your profile was created successfully"


    def dispatch(self, request, *args, **kwargs):
        return super(CreateAgentProfile, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateAgentProfile, self).get_form_kwargs()
        return kwargs


    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            print(form.errors)
        return self.form_invalid(form)


    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.save()

        # send email to farmer after registration
        current_site = get_current_site(self.request)
        subject = 'Registrated Successful'
        message = render_to_string('profile_created_successful.html', {
            'user': profile.user,
            'domain': current_site.domain,
            'message':'Your Agent account has been successfully created'
            })
        to_email = profile.user.email
        email = EmailMessage(
                subject, message, to=[to_email]
            )
        email.send()
        return redirect('unffeagents:agentprofile_list')

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(self.get_context_data(form=form))



# update farm view
class EditAgentProfileView(LoginRequiredMixin,UpdateView):
    model =AgentProfile
    template_name = 'create_agentprofile.html'
    success_url = reverse_lazy('unffeagents:agentprofile_list')
    form_class = AgentProfileForm
    success_message = "Your profile was edit successfully"


    def dispatch(self, request, *args, **kwargs):
        return super(EditAgentProfileView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(EditAgentProfileView, self).get_form_kwargs()
        return kwargs


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            print(form.errors)
        return self.form_invalid(form)


    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.save()

          # send email to farmer after registration
        current_site = get_current_site(self.request)
        subject = 'Registrated Successful'
        message = render_to_string('profile_created_successful.html', {
            'user': profile.user,
            'domain': current_site.domain,
            'message':'Your Agent account has been successfully updated'
            })
        to_email = profile.user.email
        email = EmailMessage(
                subject, message, to=[to_email]
            )
        email.send()
        return redirect('unffeagents:agentprofile_list')


    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(self.get_context_data(form=form))

# views for market
class MarketViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows markets to be viewed or edited.
    """
    queryset = Market.objects.all().order_by('market_name')
    serializer_class = MarketSerializer
    permission_classes = [permissions.IsAuthenticated]


class MarketList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'market_list.html'

    def get(self, request):
        queryset = Market.objects.order_by('market_name')
        return Response({'markets': queryset})
        

# views for marketprice
class MarketPriceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows marketprices to be viewed or edited.
    """
    queryset = MarketPrice.objects.all().order_by('market')
    serializer_class = MarketPriceSerializer
    permission_classes = [permissions.IsAuthenticated]


class MarketPriceList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'marketprice_list.html'

    def get(self, request):
        queryset = MarketPrice.objects.order_by('market')
        return Response({'marketprices': queryset})


# views for notices
class NoticeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows notices to be viewed or edited.
    """
    queryset = Notice.objects.all().order_by('-created')
    serializer_class = NoticeSerializer
    permission_classes = [permissions.IsAuthenticated]


class NoticeList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'notice_list.html'

    def get(self, request):
        queryset = Notice.objects.order_by('notice_title')
        return Response({'notices': queryset})


class CallerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows farms to be viewed or edited.
    """
    queryset = Call.objects.order_by('-call_date')
    serializer_class = CallSerializer
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = '__all__'
    ordering_fields = '__all__'


class CallList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'call_list.html'

    def get(self, request):
      
        return Response()


class EquiryList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'enquiry_list.html'

    def get(self, request):
      
        return Response()


class ResponseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows farms to be viewed or edited.
    """
    queryset = CallRsponse.objects.order_by('-id')
    serializer_class = ResponseSerializer
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['type_of_question','question','solution','called_from__name','caller','agent__first_name','agent__last_name']
    ordering_fields = '__all__'

# create notification
 
class CreateNoticeView(LoginRequiredMixin,CreateView):
    template_name = 'create_notification.html'
    success_url = reverse_lazy('unffeagents:notice_list')
    form_class = NoticeForm
    success_message = "Notice has been created successfully"


    def dispatch(self, request, *args, **kwargs):
        return super(CreateNoticeView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateNoticeView, self).get_form_kwargs()
        return kwargs


    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            print(form.errors)
        return self.form_invalid(form)


    def form_valid(self, form):
        notice = form.save(commit=False)
        notice.posted_by = self.request.user
        notice.save()
        form.save_m2m()
        users = []
        print(notice.sector.all())
        if notice.sector.all().count()>0:
            users =  User.objects.filter(is_active=True, farmer__isnull=False).exclude(email='')
            for user in users:
                if user.farmer.sector.filter(id__in=notice.sector.all()).exists() and notice.region.filter(id=user.profile.region.id) or user.farmer.sector.filter(id__in=notice.sector.all()).exists() and notice.district.filter(id=user.profile.district.id) or user.farmer.sector.filter(id__in=notice.sector.all()).exists() and notice.county.filter(id=user.profile.county.id) or user.farmer.sector.filter(id__in=notice.sector.all()).exists() and notice.sub_county.filter(id=user.profile.sub_county.id) or user.farmer.sector.filter(id__in=notice.sector.all()).exists() and notice.parish.filter(id=user.profile.parish.id) or user.farmer.sector.filter(id__in=notice.sector.all()).exists() and notice.village.filter(id=user.profile.village.id):
                    # sending email with notifications
                    current_site = get_current_site(self.request)
                    subject = notice.notice_title
                    message = render_to_string('notice_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'message': notice.description,
                        })
                    to_email = user.email
                    email = EmailMessage(
                        subject, message, to=[to_email]
                        )
                    email.content_subtype = "html"
                    email.send()

                    #send sms
                    if user.profile.phone_number:
                        try:
                            request_type = "POST"
                            url = 'https://techguy.thinvoidcloud.com/api.php'
                            data = {'contacts': str(user.profile.phone_number),'message': notice.description,'username': 'ivr@unffeict4farmers.org','password': 'ccsrzwub'}
                            response = requests.request(request_type, url, data=data)
                            print(response)
                            print(user.profile.phone_number)
                        except:
                            print('unable to  send messages')
                            
                            
        else:
            users = User.objects.filter(is_active=True).exclude(email='')
            for user in users:
                
                if user.groups.filter(id__in=notice.target_audience.all()).exists() and notice.region.filter(id=user.profile.region.id): #or user.groups.filter(id__in=notice.target_audience.all()).exists() and notice.district.filter(id=user.profile.district.id) or user.groups.filter(id__in=notice.target_audience.all()).exists() and notice.county.filter(id=user.profile.county.id) or user.groups.filter(id__in=notice.target_audience.all()).exists() and notice.sub_county.filter(id=user.profile.sub_county.id) or user.groups.filter(id__in=notice.target_audience.all()).exists() and notice.parish.filter(id=user.profile.parish.id) or user.groups.filter(id__in=notice.target_audience.all()).exists() and notice.village.filter(id=user.profile.village.id):
                    
                    current_site = get_current_site(self.request)
                    subject = notice.notice_title
                    message = render_to_string('notice_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'message': notice.description,
                        })
                    to_email = user.email
                    email = EmailMessage(
                        subject, message, to=[to_email]
                        )
                    email.content_subtype = "html"
                    email.send()

                     #send sms
                    if user.profile.phone_number:
                        try:
                            request_type = "POST"
                            url = 'https://techguy.thinvoidcloud.com/api.php'
                            data = {'contacts': str(user.profile.phone_number),'message': notice.description,'username': 'ivr@unffeict4farmers.org','password': 'ccsrzwub'}
                            response = requests.request(request_type, url, data=data)
                            print(user.profile.phone_number)
                            print(response)
                        except:
                            print('unable to  send messages')
                            

        return redirect('unffeagents:notice_list')

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(self.get_context_data(form=form))


class EditNoticeView(LoginRequiredMixin,UpdateView):
    model =Notice
    template_name = 'create_notification.html'
    success_url = reverse_lazy('unffeagents:farm_list')
    form_class = NoticeForm
    success_message = "Notice has been updated successfully"


    def dispatch(self, request, *args, **kwargs):
        return super(EditNoticeView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(EditNoticeView, self).get_form_kwargs()
        return kwargs


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            print(form.errors)
        return self.form_invalid(form)


    def form_valid(self, form):
        notice = form.save(commit=False)
        notice.save()
        form.save_m2m()
        users = []
        print(notice.sector.all())
        if notice.sector.all().count()>0:
            users =  User.objects.filter(is_active=True, farmer__isnull=False).exclude(email='')
            for user in users:
                if user.farmer.sector.filter(id__in=notice.sector.all()).exists() and notice.region.filter(id=user.profile.region.id) or user.farmer.sector.filter(id__in=notice.sector.all()).exists() and notice.district.filter(id=user.profile.district.id) or user.farmer.sector.filter(id__in=notice.sector.all()).exists() and notice.county.filter(id=user.profile.county.id) or user.farmer.sector.filter(id__in=notice.sector.all()).exists() and notice.sub_county.filter(id=user.profile.sub_county.id) or user.farmer.sector.filter(id__in=notice.sector.all()).exists() and notice.parish.filter(id=user.profile.parish.id) or user.farmer.sector.filter(id__in=notice.sector.all()).exists() and notice.village.filter(id=user.profile.village.id):
                    # sending email with notifications
                    current_site = get_current_site(self.request)
                    subject = notice.notice_title
                    message = render_to_string('notice_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'message': notice.description,
                        })
                    to_email = user.email
                    email = EmailMessage(
                        subject, message, to=[to_email]
                        )
                    email.content_subtype = "html"
                    email.send()

                    #send sms
                    if user.profile.phone_number:
                        try:
                            request_type = "POST"
                            url = 'https://techguy.thinvoidcloud.com/api.php'
                            data = {'contacts': str(user.profile.phone_number),'message': notice.description,'username': 'ivr@unffeict4farmers.org','password': 'ccsrzwub'}
                            response = requests.request(request_type, url, data=data)
                            print(response)
                            print(user.profile.phone_number)
                        except:
                            print('unable to  send messages')
                            
                            
        else:
            users = User.objects.filter(is_active=True).exclude(email='')
            for user in users:
                
                if user.groups.filter(id__in=notice.target_audience.all()).exists() and notice.region.filter(id=user.profile.region.id): #or user.groups.filter(id__in=notice.target_audience.all()).exists() and notice.district.filter(id=user.profile.district.id) or user.groups.filter(id__in=notice.target_audience.all()).exists() and notice.county.filter(id=user.profile.county.id) or user.groups.filter(id__in=notice.target_audience.all()).exists() and notice.sub_county.filter(id=user.profile.sub_county.id) or user.groups.filter(id__in=notice.target_audience.all()).exists() and notice.parish.filter(id=user.profile.parish.id) or user.groups.filter(id__in=notice.target_audience.all()).exists() and notice.village.filter(id=user.profile.village.id):
                    
                    current_site = get_current_site(self.request)
                    subject = notice.notice_title
                    message = render_to_string('notice_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'message': notice.description,
                        })
                    to_email = user.email
                    email = EmailMessage(
                        subject, message, to=[to_email]
                        )
                    email.content_subtype = "html"
                    email.send()

                     #send sms
                    if user.profile.phone_number:
                        try:
                            request_type = "POST"
                            url = 'https://techguy.thinvoidcloud.com/api.php'
                            data = {'contacts': str(user.profile.phone_number),'message': notice.description,'username': 'ivr@unffeict4farmers.org','password': 'ccsrzwub'}
                            response = requests.request(request_type, url, data=data)
                            print(user.profile.phone_number)
                            print(response)
                        except:
                            print('unable to  send messages')
                            
        return redirect('unffeagents:notice_list')


    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(self.get_context_data(form=form))

# create inquiry view
class CreateEquiryView(LoginRequiredMixin,CreateView):
    template_name = 'create_enquiry.html'
    success_url = reverse_lazy('unffeagents:enquiries')
    form_class = EnquiryForm
    success_message = "Notice has been created successfully"


    def dispatch(self, request, *args, **kwargs):
        return super(CreateEquiryView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateEquiryView, self).get_form_kwargs()
        return kwargs


    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            print(form.errors)
        return self.form_invalid(form)


    def form_valid(self, form):
        call =  Call.objects.get(pk=self.kwargs['session_id'])
        enquiry = form.save(commit=False)
        enquiry.agent = self.request.user
        enquiry.caller = call.phone
        enquiry.call = call
        enquiry.save()
        return redirect('unffeagents:enquiries')

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(self.get_context_data(form=form))


class EditEquiryView(LoginRequiredMixin,UpdateView):
    model =CallRsponse
    template_name = 'create_enquiry.html'
    success_url = reverse_lazy('unffeagents:enquiries')
    form_class = EnquiryForm
    success_message = "Equiry has been updated successfully"


    def dispatch(self, request, *args, **kwargs):
        return super(EditEquiryView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(EditEquiryView, self).get_form_kwargs()
        return kwargs


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            print(form.errors)
        return self.form_invalid(form)


    def form_valid(self, form):
        notice = form.save(commit=False)
        notice.save()                  
        return redirect('unffeagents:enquiries')


    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(self.get_context_data(form=form))
    

class UsersList(APIView, LoginRequiredMixin):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'users_list.html'

    def get(self, request):
        queryset = User.objects.order_by('-id')
        phone=self.request.query_params.get('phone', None)
        if phone is not None:
            print(str(phone))
            # queryset = queryset.filter(
            #         profile__phone_number__icontains=self.request.query_params.get('phone'))
            queryset = User.objects.filter(profile__phone_number=str(phone))
           
        print(queryset)
        return Response({'users': queryset})

