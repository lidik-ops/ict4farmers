from django.shortcuts import render
from .models import Group, FarmerProfile
from .serializers import GroupSerializer, FarmerProfileSerializer, FarmerApprovalSerializer,PostFarmerProfileSerializer
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.mixins import LoginRequiredMixin
from common.tokens import account_activation_token
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.http import (HttpResponseRedirect,JsonResponse, HttpResponse,
                         Http404)
from django.views.generic import (
    CreateView, UpdateView, DetailView, TemplateView, View, DeleteView)
from .forms import(FarmerProfileForm)
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.http import (HttpResponseRedirect,JsonResponse, HttpResponse,
                         Http404)
from .forms import(FarmerProfileForm,FarmerGroupForm)
import datetime

from django.contrib import messages
from django.contrib.auth.models import Group as UserGroup
from django.db.models import Count, Q, Sum, FloatField
import json
from django.db import IntegrityError
from rest_framework import filters
from farm .models import Sector
from django.db.models.functions import Cast




# views for groups
class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows sectors to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('-id')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['name','contact_person','contact_person_email','contact_person_phone','address']
    ordering_fields = '__all__'



class GroupList(APIView, LoginRequiredMixin):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'group_list.html'

    def get(self, request):
        queryset = Group.objects.order_by('-id')
        return Response({'groups': queryset})


# create farmer groups
class CreateFarmerGroup(LoginRequiredMixin,CreateView):
    template_name = 'create_farmer_group.html'
    success_url = reverse_lazy('farmer:group_list')
    form_class = FarmerGroupForm
    success_message = "Group has been created successfully"


    def dispatch(self, request, *args, **kwargs):
        return super(CreateFarmerGroup, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateFarmerGroup, self).get_form_kwargs()
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
        group = form.save(commit=False)
        group.save()

        return redirect('farmer:group_list')

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(self.get_context_data(form=form))

# edit farmer group

class EditFarmerGroup(LoginRequiredMixin,UpdateView):
    model =Group
    template_name = 'create_farmer_group.html'
    success_url = reverse_lazy('farmer:group_list')
    form_class = FarmerGroupForm
    success_message = "Group has been updated successfully"


    def dispatch(self, request, *args, **kwargs):
        return super(EditFarmerGroup, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(EditFarmerGroup, self).get_form_kwargs()
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
        group = form.save(commit=False)
        group.save()

        return redirect('farmer:group_list')

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(self.get_context_data(form=form))

# views for farmerprofile
class FarmerProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows sectors to be viewed or edited.
    """
    #queryset = FarmerProfile.objects.all().order_by('region')
    serializer_class = FarmerProfileSerializer
    write_serializer_class = PostFarmerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def approved(self, request, pk, format=None):
        profile = self.get_object()
        serializer = FarmerApprovalSerializer(profile, data=request.data)
        if serializer.is_valid():
            farmer_group = UserGroup.objects.get(name='Farmers')
            profile.user.groups.add(farmer_group)
            serializer.save(status ='Active', approved_date = datetime.datetime.now(),
            approver=self.request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def decline(self, request, pk, format=None):
        profile = self.get_object()
        serializer = FarmerApprovalSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save(status ='Rejected', approved_date = datetime.datetime.now(),approver=self.request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def get_queryset(self):
        """
        This view should return a list of all the farmers profiles
        for the currently authenticated user.
        """
        user = self.request.user
        farmers = FarmerProfile.objects.all().order_by('-user_id')
        if  self.request.user.has_perm('farmer.delete_farmerprofile'):
            queryset = farmers
        else:
            queryset = farmers.filter(user=user)
        
        return queryset

    def create(self, request, format=None):
        serializer = PostFarmerProfileSerializer(data=request.data)

        if serializer.is_valid():
            try:
                serializer.status ='Pending'
                serializer.save(user = self.request.user)
                serializer.save()
            except IntegrityError:
                return Response({'error':'Farmer account already exists'})
                
            return Response({'status':'successful'})
        return Response(serializer.errors, status=400)


class FarmerProfileList(APIView, LoginRequiredMixin):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'farmerprofile_list.html'

    def get(self, request):
        return Response()


'''
Create farmer profile. Used class based view.
'''
class CreateFarmerProfile(LoginRequiredMixin,CreateView):
    template_name = 'create_farmer_profile.html'
    success_url = reverse_lazy('farm:create_farm')
    form_class = FarmerProfileForm
    success_message = "Your profile was created successfully"


    def dispatch(self, request, *args, **kwargs):
        return super(CreateFarmerProfile, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateFarmerProfile, self).get_form_kwargs()
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
        # setting farmer profile to in-active
        profile.status = 'Pending'
        profile.user = self.request.user
        profile.save()
        form.save_m2m()

        # send email to farmer after registration
        current_site = get_current_site(self.request)
        subject = 'Registered Successfully'
        message = render_to_string('profile_created_successful_email.html', {
            'user': profile.user,
            'domain': current_site.domain,
            'message':'Your Profile as a farmer in the ICT4Farmers System has been recieved successfully\n'+
            'please Register your farm/s for approval as a farmer by UNFFE Agents.'
            })
        to_email = profile.user.email
        email = EmailMessage(
                subject, message, to=[to_email]
            )
        email.content_subtype = "html"
        email.send()
        messages.add_message(self.request, messages.INFO, 'Please Register your farm from here, note that you can register more than one')
        return redirect('farm:create_farm')

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(self.get_context_data(form=form))



'''
Edit farmer profile profile
'''
class UpdateFarmerProfile(LoginRequiredMixin,UpdateView):
    model =FarmerProfile
    template_name = 'create_farmer_profile.html'
    success_url = reverse_lazy('farmer:farmerprofile_list')
    form_class = FarmerProfileForm
    success_message = "Your profile was Updated successfully"


    def dispatch(self, request, *args, **kwargs):
        return super(UpdateFarmerProfile, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(UpdateFarmerProfile, self).get_form_kwargs()
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
        # updating profile for only changed fields
        profile.save()
        form.save_m2m()
        # send email to farmer after registration
        current_site = get_current_site(self.request)
        subject = 'Registered Successfully'
        message = render_to_string('profile_created_successful_email.html', {
            'user': profile.user,
            'domain': current_site.domain,
            'message':'Your Profile as a farmer in the ICT4Farmers System has been updated successfully',
          
            })
        to_email = profile.user.email
        email = EmailMessage(
                subject, message, to=[to_email]
            )
        email.content_subtype = "html"
        email.send()
        return redirect('farmer:farmerprofile_list')

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(self.get_context_data(form=form))



class FarmerProfileDetailView(LoginRequiredMixin, DetailView):
    model = FarmerProfile
    context_object_name = "profilerecord"
    template_name = "view_farmer_profile.html"

    def get_context_data(self, **kwargs):
        context = super(FarmerProfileDetailView, self).get_context_data(**kwargs)
        
        context.update({

        })
        return context


#Quering the farmers table for the data. 
# def farmer_class_view(request):


#     farmers = FarmerProfile.objects.all()
#    # print(farmers) 
#     count = float(farmers.count())
#     sectors = Sector.objects.all()
#     print(count)

#     for farmer in farmers:
#         dataset = FarmerProfile.objects.values('user__profile__region__name').annotate(
#             farmers = Count('sector', filter = Q(sector__in=sectors)),
#             percentage =  Cast(((Count('sector', filter = Q(sector__in=sectors))/count)*100),FloatField()))
                
#     print(dataset)
    


#     return render(request, 'credit.html', {'dataset': dataset})

def farmer_class_view(request):
    farmers = FarmerProfile.objects.all()
    count = float(farmers.count())
    sectors = Sector.objects.all()
    print(count)

    labels = []
    data = []
  
    dataset = FarmerProfile.objects.filter(user__profile__region__isnull = False).values('user__profile__region__name').annotate(
        #crop_count = Count('sector', filter=Q(sector='Crop Farming')),
        farmers = Count('sector', filter = Q(sector__in=sectors)),
        percentage =  ((Count('sector', filter = Q(sector__in=sectors))/count)*100))
                
    print(dataset)
    for entry in dataset:
        labels.append('%s Region' % entry['user__profile__region__name'] )
        data1=data.append( entry['percentage'])
        #data1.append('O')
        
      

    return render(request, 'credit.html', {
        'labels': labels,
        'data': data,
    })

