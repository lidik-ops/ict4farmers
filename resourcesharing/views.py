from django.shortcuts import render
from .models import (Resource, ResourceSharing, ResourceBooking)
from .forms import(ResourceForm,ResourceBookingForm)
from .serializers import ResourceSerializer,PostResourceSerializer, ResourceSharingSerializer, ResourceBookingSerializer
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.renderers import TemplateHTMLRenderer

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from django.contrib import messages
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import redirect
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.urls import reverse_lazy
from django.http import (HttpResponseRedirect,JsonResponse, HttpResponse,
                         Http404)
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.views.generic import (
    CreateView, UpdateView, DetailView, TemplateView, View, DeleteView)
from django.db import IntegrityError
from farmer.models import FarmerProfile
# views for resources
class ResourceList(LoginRequiredMixin, APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'resource_list.html'

    def get(self, request):
       # queryset = Sector.objects.order_by('-id')
        return Response()

# resourcesharing api for resourcess
class ResourceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows resources to be viewed or edited.
    """
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    
    def create(self, request, format=None):
        serializer = PostResourceSerializer(data=request.data)

        if serializer.is_valid():
            try:
                serializer.status ='Not Available'
                user = self.request.user
                owner = FarmerProfile.objects.get(user=user)
                #serializer.user = self.request.user
                serializer.save(owner = owner)
            except IntegrityError:
                return Response({'error':'Resource account already exists'})
                
            return Response({'status':'successful'})
        return Response(serializer.errors, status=400)

# create resource
class CreateResourceView(LoginRequiredMixin,CreateView):
    template_name = 'create_resource.html'
    success_url = reverse_lazy('resourcesharing:resource_list')
    form_class = ResourceForm
    success_message = "Resource has been created successfully"


    def dispatch(self, request, *args, **kwargs):
        return super(CreateResourceView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateResourceView, self).get_form_kwargs()
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
        resource = form.save(commit=False)
        resource.owner = self.request.user
        resource.save()
        return redirect('resourcesharing:resource_list')

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(self.get_context_data(form=form))



# update resource view
class EditResourceView(LoginRequiredMixin,UpdateView):
    model = Resource
    template_name = 'create_resource.html'
    success_url = reverse_lazy('resourcesharing:resource_list')
    form_class = ResourceForm
    success_message = "Resource has been updated successfully"


    def dispatch(self, request, *args, **kwargs):
        return super(EditResourceView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(EditResourceView, self).get_form_kwargs()
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
        resource = form.save(commit=False)
        resource.save()
        return redirect('resourcesharing:resource_list')



class ResourceDetailView(DetailView):
    model = Resource
    template_name = "view_resource_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ResourceDetailView, self).get_context_data(**kwargs)
        context['Resourceobject'] = self.object
        
        return context

class ResourceList(LoginRequiredMixin, APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'resource_list.html'

    def get(self, request):
       # queryset = Sector.objects.order_by('-id')
        return Response()

# views for resource booking
class ResourceBookingList(LoginRequiredMixin,APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'resourcebooking_list.html'

    def get(self, request):
        queryset = ResourceBooking.objects.order_by('resource')
        return Response({'resourcebookings': queryset})

class ResourceBookingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows resources to be viewed or edited.
    """
    queryset = ResourceBooking.objects.all()
    serializer_class = ResourceBookingSerializer
  
# create booking
class ResourceBookingView(LoginRequiredMixin,CreateView):
    template_name = 'booking.html'
    success_url = reverse_lazy('resourcesharing:resourcebooking_list')
    form_class = ResourceBookingForm
    success_message = "Booking has been created successfully"


    def dispatch(self, request, *args, **kwargs):
        return super(ResourceBookingView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(ResourceBookingView, self).get_form_kwargs()
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
        resource = form.save(commit=False)
        resource.booker = self.request.user
        resource.save()
        
        print(resource.resource.owner.user.email)

        # send email to farmer after registration
        current_site = get_current_site(self.request)
        subject = 'Booked successfully Successfully'
        message = render_to_string('booking_created_successfully_email.html', {
            'user': resource.resource.owner.user,
            'domain': current_site.domain,
            'resource':resource
            })
        to_email = resource.resource.owner.user.email
        email = EmailMessage(
                subject, message, to=[to_email]
            )
        email.content_subtype = "html"
        email.send()
        messages.add_message(self.request, messages.INFO, 'Please wait for approval from the resource owner')
        return redirect('resourcesharing:resourcebooking_list')

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(self.get_context_data(form=form))

    def get_initial(self, *args, **kwargs):
        initial = super(ResourceBookingView, self).get_initial(**kwargs)
        initial['resource'] = Resource.objects.get(pk=self.kwargs['resource_pk'])
        return initial

# edit resource view
class EditBookingView(LoginRequiredMixin,UpdateView):
    model = ResourceBooking
    template_name = 'booking.html'
    success_url = reverse_lazy('resourcesharing:resourcebooking_list')
    form_class = ResourceBookingForm
    success_message = "Booking has been updated successfully"


    def dispatch(self, request, *args, **kwargs):
        return super(EditBookingView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(EditBookingView, self).get_form_kwargs()
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
        resource = form.save(commit=False)
        resource.save()
        return redirect('resourcesharing:resourcebooking_list')



# views for resource sharing
class ResourceSharingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows agentprofiles to be viewed or edited.
    """
    queryset = ResourceSharing.objects.all().order_by('resource')
    serializer_class = ResourceSharingSerializer
    permission_classes = [permissions.IsAuthenticated]


class ResourceSharingList(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'resourcesharing_list.html'

    def get(self, request):
        queryset = ResourceSharing.objects.order_by('resource')
        return Response({'resourcesharings': queryset})



