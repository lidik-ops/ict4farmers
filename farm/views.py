from django.shortcuts import render
from .models import (Sector, Enterprise, Farm,ProductionRecord, Query, FarmRecord, FinancialRecord, EnterpriseSelection,Ecological_Zones)
from .serializers import (SectorSerializer, EnterpriseSerializer, FarmSerializer
,FarmMapSerializer,FarmProductionRecordSerializer,PostFarmSerializer,PostEnterpriseSelectionSerializer,PostEnterpriseSerializer, PostQuerySerializer,FarmRecordSerializer,FarmFinancilRecordSerializer,EnterpriseSelectionSerializer,QuerySerializer)
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.urls import reverse_lazy
from django.http import (HttpResponseRedirect,JsonResponse, HttpResponse,
                         Http404)
from django.views.generic import (
    CreateView, UpdateView, DetailView, TemplateView, View, DeleteView)
from .forms import (FarmForm,FarmProductionRecordForm,EnterpriseForm,QueryForm, FarmRecordForm,FarmFnancialRecordForm, EnterpriseSelectionForm)
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from farmer.models import FarmerProfile
import datetime
from django.db import IntegrityError
from django_postgres_extensions.models.expressions import Index, SliceArray
from rest_framework import filters
# views for sector
class SectorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows sectors to be viewed or edited.
    """
    queryset = Sector.objects.all().order_by('-id')
    serializer_class = SectorSerializer
    permission_classes = [permissions.IsAuthenticated]


class SectorList(LoginRequiredMixin, APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'sector_list.html'

    def get(self, request):
       # queryset = Sector.objects.order_by('-id')
        return Response()


class SectorDetail(LoginRequiredMixin, APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'sector_detail.html'
    context_object_name = "sectorrecord"

    def get(self, request, pk):
        sector = get_object_or_404(Sector, pk=pk)
        serializer = SectorSerializer(sector)
        return Response({'serializer': serializer, 'sector': sector})

    def post(self, request, pk):
        sector = get_object_or_404(Sector, pk=pk)
        serializer = SectorSerializer(sector, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'sector': sector})
        serializer.save()
        return redirect('farms:sector_list')


class CreateSector(LoginRequiredMixin, APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'create_sector.html'

    def get(self, request):
        sector = None
        serializer = SectorSerializer()
        return Response({'serializer': serializer, 'sector': sector})

    def post(self, request):
        serializer = SectorSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer})
        serializer.save()
        return redirect('farm:sector_list')


class QueryList(LoginRequiredMixin, APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'query_list.html'

    def get(self, request):
       # queryset = Sector.objects.order_by('-id')
        return Response()

# farm api for queries
class QueryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows farmer queries to be viewed or edited.
    """
    queryset = Query.objects.all()
    serializer_class = QuerySerializer
    def get_queryset(self):
        """
        This view should return a list of all the farms 
        for the currently authenticated user.
        """
        user = self.request.user
        queries = Query.objects.order_by('farm')
        
        if self.request.user.is_superuser or self.request.user.groups.filter(name='UNFFE Agents').exists():
            queryset = queries
        else:
            farmer = FarmerProfile.objects.get(user=user)
            farms = Farm.objects.filter(farmer =farmer)
            queryset = queries.filter(farm__in=farms)
           
        return queryset

    def create(self, request, format=None):
        serializer = PostQuerySerializer(data=request.data)

        if serializer.is_valid():
            try:
                user = self.request.user
                # farmer = FarmerProfile.objects.get(user=user)
                # farm = Farm.objects.get(farmer=farmer)
                #serializer.user = self.request.user
                serializer.save()
            except IntegrityError:
                return Response({'error':'Query already exists'})
                
            return Response({'status':'successful'})
        return Response(serializer.errors, status=400)

# create farm 
class CreateQueryView(LoginRequiredMixin,CreateView):
    template_name = 'create_query.html'
    success_url = reverse_lazy('farm:query_list')
    form_class = QueryForm
    success_message = "Query has been created successfully"


    def dispatch(self, request, *args, **kwargs):
        return super(CreateQueryView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateQueryView, self).get_form_kwargs()
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
        farm = form.save(commit=False)
        farm.save()
        return redirect('farm:query_list')

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(self.get_context_data(form=form))


# update farm view
class EditQueryView(LoginRequiredMixin,UpdateView):
    model =Query
    template_name = 'create_query.html'
    success_url = reverse_lazy('farm:query_list')
    form_class = QueryForm
    success_message = "Query has been updated successfully"


    def dispatch(self, request, *args, **kwargs):
        return super(EditQueryView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(EditQueryView, self).get_form_kwargs()
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
        farm = form.save(commit=False)
        farm.save()
        return redirect('farm:query_list')



# views for enterprise
class EnterpriseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows sectors to be viewed or edited.
    """
    serializer_class = EnterpriseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the farms 
        for the currently authenticated user.
        """
        user = self.request.user
       
        enterprises = Enterprise.objects.all().order_by('farm')
        if self.request.user.is_superuser or self.request.user.groups.filter(name='UNFFE Agents').exists():
            queryset = enterprises
        else:
            farmer = FarmerProfile.objects.get(user=user)
            farms = Farm.objects.filter(farmer =farmer)
            queryset = enterprises.filter(farm__in=farms)
        
        return queryset

    def create(self, request, format=None):
        serializer = PostEnterpriseSerializer(data=request.data)

        if serializer.is_valid():
            try:
                user = self.request.user
                # farmer = FarmerProfile.objects.get(user=user)
                # farm = Farm.objects.get(farmer=farmer)
                #serializer.user = self.request.user
                serializer.save()
            except IntegrityError:
                return Response({'error':'Enterprise already exists'})
                
            return Response({'status':'successful'})
        return Response(serializer.errors, status=400)

class EnterpriseList(LoginRequiredMixin, APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'enterprise_list.html'

    def get(self, request):
        queryset = Enterprise.objects.order_by('-id')
        return Response({'enterprise': queryset})



# farm api viewset
class FarmViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows farms to be viewed or edited.
    """
    serializer_class = FarmSerializer
    permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = []

    def get_queryset(self):
        """
        This view should return a list of all the farms 
        for the currently authenticated user.
        """
        user = self.request.user
        
        farms = Farm.objects.all().order_by('farmer')
        if self.request.user.is_superuser or self.request.user.groups.filter(name='UNFFE Agents').exists():
            queryset = farms
        else:
            farmer = FarmerProfile.objects.get(user=user)
            queryset = farms.filter(farmer=farmer)
        
        return queryset

    def create(self, request, format=None):
        serializer = PostFarmSerializer(data=request.data)

        if serializer.is_valid():
            try:
                serializer.status ='active'
                user = self.request.user
                farmer = FarmerProfile.objects.get(user=user)
                #serializer.user = self.request.user
                serializer.save(farmer = farmer)
            except IntegrityError:
                return Response({'error':'Farm already exists'})
                
            return Response({'status':'successful'})
        return Response(serializer.errors, status=400)

# farm api for maps
class FarmMapViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows farms to be viewed or edited.
    """
    queryset = Farm.objects.all()
    serializer_class = FarmMapSerializer
    



# list of farms
class FarmListView(APIView, LoginRequiredMixin):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'farm_list.html'

    def get(self, request):
        return Response()



# create farm 
class CreateFarmView(LoginRequiredMixin,CreateView):
    template_name = 'create_farm.html'
    success_url = reverse_lazy('farm:farm_list')
    form_class = FarmForm
    success_message = "Farm has been created successfully"


    def dispatch(self, request, *args, **kwargs):
        return super(CreateFarmView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateFarmView, self).get_form_kwargs()
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
        farm = form.save(commit=False)
        # assign total land to available land
        farm.available_land = farm.land_occupied
        farm.save()

        # send email to farmer after registration
        current_site = get_current_site(self.request)
        subject = 'Farm Created Successfully'
        message = render_to_string('farm_created_successful_email.html', {
            'user': farm.farmer.user,
            'domain': current_site.domain,
            'message': 'Your '+farm.farm_name + ' has been registered sucessfully',
            })
        to_email = farm.farmer.user.email
        email = EmailMessage(
                subject, message, to=[to_email]
            )
        email.content_subtype = "html"
        email.send()
        return redirect('farm:farm_list')

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(self.get_context_data(form=form))


# update farm view
class EditFarmView(LoginRequiredMixin,UpdateView):
    model =Farm
    template_name = 'create_farm.html'
    success_url = reverse_lazy('farm:farm_list')
    form_class = FarmForm
    success_message = "Farm has been updated successfully"


    def dispatch(self, request, *args, **kwargs):
        return super(EditFarmView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(EditFarmView, self).get_form_kwargs()
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
        farm = form.save(commit=False)
        farm.save()

         # send email to farmer  a message after an update
        current_site = get_current_site(self.request)
        subject = 'Farm Updated Successfully'
        message = render_to_string('farm_created_successful_email.html', {
            'user': farm.farmer.user,
            'domain': current_site.domain,
            'message': 'Your '+farm.farm_name + ' Details have been updated sucessfully',
            })
        to_email = farm.farmer.user.email
        email = EmailMessage(
                subject, message, to=[to_email]
            )
        email.content_subtype = "html"
        email.send()
        return redirect('farm:farm_list')


    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(self.get_context_data(form=form))



# create enterprise
class CreateEnterpriseView(LoginRequiredMixin,CreateView):
    template_name = 'create_enterprise.html'
    success_url = reverse_lazy('farm:farm_list')
    form_class = EnterpriseForm
    success_message = "Farm has been created successfully"


    def dispatch(self, request, *args, **kwargs):
        return super(CreateEnterpriseView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateEnterpriseView, self).get_form_kwargs()
        kwargs['request'] = self.request
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
        enterprise = form.save(commit=False)
        enterprise.save()
        # calculating remaining land on the farm
        # get the farm first
        farm = Farm.objects.get(id=enterprise.farm_id)
        farm_land_occupied = farm.land_occupied
        # subtracting the enterprise land from the farm land
        farm_available_land = farm_land_occupied - enterprise.land_occupied
        # update the farm object
        Farm.objects.filter(id=enterprise.farm_id).update(available_land=farm_available_land)
        print(farm_available_land)
        # send email to farmer after registration
        current_site = get_current_site(self.request)
        subject = 'Enterprise Created Successfully'
        message = render_to_string('enterprise_email.html', {
            'user': enterprise.farm.farmer.user,
            'domain': current_site.domain,
            'message': 'Your '+enterprise.name + ' has been registered sucessfully',
            })
        to_email = enterprise.farm.farmer.user.email
        email = EmailMessage(
                subject, message, to=[to_email]
            )
        email.content_subtype = "html"
        email.send()
        return redirect('farm:enterprise_list')

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_initial(self, *args, **kwargs):
        initial = super(CreateEnterpriseView, self).get_initial(**kwargs)
        initial['farm'] = Farm.objects.get(pk=self.kwargs['farm_pk'])
        return initial

    def get_context_data(self, **kwargs):
        context = super(CreateEnterpriseView, self).get_context_data(**kwargs)
        farm = Farm.objects.get(pk=self.kwargs['farm_pk'])
        context['landsize'] = farm.land_occupied
        context['available_land'] = farm.available_land
        return context


# update Enterprise view
class EditEnterpriseView(LoginRequiredMixin,UpdateView):
    model =Enterprise
    template_name = 'create_enterprise.html'
    success_url = reverse_lazy('farm:farm_list')
    form_class = EnterpriseForm
    success_message = "Enterprise has been updated successfully"


    def dispatch(self, request, *args, **kwargs):
        return super(EditEnterpriseView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(EditEnterpriseView, self).get_form_kwargs()
        kwargs['request'] = self.request
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
        enterprise = form.save(commit=False)
        enterprise.save()

         # send email to farmer  a message after an update
        current_site = get_current_site(self.request)
        subject = 'Enterprise Updated Successfully'
        message = render_to_string('enterprise_email.html', {
            'user': enterprise.farm.farmer.user,
            'domain': current_site.domain,
            'message': 'Your '+enterprise.name + ' Details have been updated sucessfully',
            })
        to_email = enterprise.farm.farmer.user.email
        email = EmailMessage(
                subject, message, to=[to_email]
            )
        email.content_subtype = "html"
        email.send()
        return redirect('farm:enterprise_list')


    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(self.get_context_data(form=form))

class FarmProfileDetailView(DetailView):
    model = Farm
    template_name = "view_farm_profile.html"

    def get_context_data(self, **kwargs):
        context = super(FarmProfileDetailView, self).get_context_data(**kwargs)
        context['farmobject'] = self.object
        
        return context

# farm record viewset
class FarmRecordViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows sectors to be viewed or edited.
    """
    serializer_class = FarmRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the farms 
        for the currently authenticated user.
        """
        user = self.request.user
        
        farmrecords = FarmRecord.objects.all().order_by('enterprise')
        if self.request.user.is_superuser or self.request.user.groups.filter(name='UNFFE Agents').exists():
            queryset = farmrecords
        else:
            farmer = FarmerProfile.objects.get(user=user)
            farms = Farm.objects.filter(farmer =farmer)
            enterprises = Enterprise.objects.filter(farm__in=farms)
            queryset = farmrecords.filter(enterprise__in=enterprises)
        
        return queryset


# create farm record
class CreateFarmRecordView(LoginRequiredMixin,CreateView):
    template_name = 'create_farm_record.html'
    success_url = reverse_lazy('farm:farm_list')
    form_class = FarmRecordForm
    success_message = "Farm Record has been created successfully"


    def dispatch(self, request, *args, **kwargs):
        return super(CreateFarmRecordView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateFarmRecordView, self).get_form_kwargs()
        kwargs['request'] = self.request
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
        farm = form.save(commit=False)
        farm.save()

        # send email to farmer after registration
        current_site = get_current_site(self.request)
        subject = 'Farm Record Captured Successfully'
        message = render_to_string('farm_created_successful_email.html', {
            'user': self.request.user,
            'domain': current_site.domain,
            'message': 'Your '+farm.name + ' has been recorded sucessfully',
            })
        to_email = self.request.user.email
        email = EmailMessage(
                subject, message, to=[to_email]
            )
        email.content_subtype = "html"
        email.send()
        return redirect('farm:farmrecords')

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(self.get_context_data(form=form))

    def get_initial(self, *args, **kwargs):
        initial = super(CreateFarmRecordView, self).get_initial(**kwargs)
        initial['enterprise'] = Enterprise.objects.get(pk=self.kwargs['enterprise_pk'])
        return initial


class FarmRecordsList(LoginRequiredMixin, APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'farm_record_list.html'

    def get(self, request):
    
        return Response()

# update farmrecord view
class EditFarmRecordView(LoginRequiredMixin,UpdateView):
    model =FarmRecord
    template_name = 'create_farm_record.html'
    success_url = reverse_lazy('farm:farm_list')
    form_class = FarmRecordForm
    success_message = "Farm Record has been updated successfully"


    def dispatch(self, request, *args, **kwargs):
        return super(EditFarmRecordView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(EditFarmRecordView, self).get_form_kwargs()
        kwargs['request'] = self.request
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
        farmrecord = form.save(commit=False)
        farmrecord.save()

         # send email to farmer  a message after an update
        current_site = get_current_site(self.request)
        subject = 'Farm Record Updated Successfully'
        message = render_to_string('enterprise_email.html', {
            'user': self.request.user,
            'domain': current_site.domain,
            'message': 'Your '+farmrecord.enterprise.name + ' Details have been updated sucessfully',
            })
        to_email = self.request.user.email
        email = EmailMessage(
                subject, message, to=[to_email]
            )
        email.content_subtype = "html"
        email.send()
        return redirect('farm:farmrecords')


    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(self.get_context_data(form=form))


# create financial record

class CreateFarmFinancialRecordView(LoginRequiredMixin,CreateView):
    template_name = 'create_farm_financial_record.html'
    success_url = reverse_lazy('farm:financialrecords')
    form_class = FarmFnancialRecordForm
    success_message = "Farm Financial Record has been created successfully"


    def dispatch(self, request, *args, **kwargs):
        return super(CreateFarmFinancialRecordView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateFarmFinancialRecordView, self).get_form_kwargs()
        kwargs['request'] = self.request
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
        record = form.save(commit=False)
        record.transaction_date =datetime.date.today()
        record.reported_by = self.request.user
        record.save()

        # send email to farmer after registration
        current_site = get_current_site(self.request)
        subject = 'Farm Record Financial Captured Successfully'
        message = render_to_string('farm_created_successful_email.html', {
            'user': self.request.user,
            'domain': current_site.domain,
            'message': 'Your Financial record spent on '+record.spent_on + ' has been recorded sucessfully',
            })
        to_email = self.request.user.email
        email = EmailMessage(
                subject, message, to=[to_email]
            )
        email.content_subtype = "html"
        email.send()
        return redirect('farm:financialrecords')

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(self.get_context_data(form=form))

    def get_initial(self, *args, **kwargs):
        initial = super(CreateFarmFinancialRecordView, self).get_initial(**kwargs)
        initial['enterprise'] = Enterprise.objects.get(pk=self.kwargs['enterprise_pk'])
        return initial


class FarmFinancilRecordsList(LoginRequiredMixin, APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'farm_financial_record_list.html'

    def get(self, request):
    
        return Response()

# update farmrecord view
class EditFarmFinancialRecordView(LoginRequiredMixin,UpdateView):
    model =FinancialRecord
    template_name = 'create_farm_financial_record.html'
    success_url = reverse_lazy('farm:financialrecords')
    form_class = FarmFnancialRecordForm
    success_message = "Farm Financial Record has been updated successfully"


    def dispatch(self, request, *args, **kwargs):
        return super(EditFarmFinancialRecordView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(EditFarmFinancialRecordView, self).get_form_kwargs()
        kwargs['request'] = self.request
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
        farmrecord = form.save(commit=False)
        farmrecord.save()

         # send email to farmer  a message after an update
        current_site = get_current_site(self.request)
        subject = 'Farm Record Updated Successfully'
        message = render_to_string('enterprise_email.html', {
            'user': self.request.user,
            'domain': current_site.domain,
            'message': 'Your Financial record spent on '+farmrecord.spent_on + ' has been recorded sucessfully',
            })
        to_email = self.request.user.email
        email = EmailMessage(
                subject, message, to=[to_email]
            )
        email.content_subtype = "html"
        email.send()
        return redirect('farm:financialrecords')


    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(self.get_context_data(form=form))



# farm record viewset
class FarmFinancialRecordViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows sectors to be viewed or edited.
    """
    serializer_class = FarmFinancilRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the farms 
        for the currently authenticated user.
        """
        user = self.request.user
        farmrecords = FinancialRecord.objects.all().order_by('enterprise')
        if self.request.user.is_superuser or self.request.user.groups.filter(name='UNFFE Agents').exists():
            queryset = farmrecords
        else:
            farmer = FarmerProfile.objects.get(user=user)
            farms = Farm.objects.filter(farmer =farmer)
            enterprises = Enterprise.objects.filter(farm__in=farms)
            queryset = farmrecords.filter(enterprise__in=enterprises)
        
        return queryset


#create Production record
class CreateFarmProductionRecordView(LoginRequiredMixin,CreateView):
    template_name = 'create_farm_production_record.html'
    success_url = reverse_lazy('farm:productionrecords')
    form_class = FarmProductionRecordForm
    success_message = "Farm Production Record has been created successfully"


    def dispatch(self, request, *args, **kwargs):
        return super(CreateFarmProductionRecordView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateFarmProductionRecordView, self).get_form_kwargs()
        kwargs['request'] = self.request
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
        record = form.save(commit=False)
        record.save()

        # send email to farmer after registration
        current_site = get_current_site(self.request)
        subject = 'Farm Record production Captured Successfully'
        message = render_to_string('farm_created_successful_email.html', {
            'user': self.request.user,
            'domain': current_site.domain,
            'message': 'Your production record  '+record.record_name + ' has been recorded sucessfully',
            })
        to_email = self.request.user.email
        email = EmailMessage(
                subject, message, to=[to_email]
            )
        email.content_subtype = "html"
        email.send()
        return redirect('farm:productionrecords')

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(self.get_context_data(form=form))

    def get_initial(self, *args, **kwargs):
        initial = super(CreateFarmProductionRecordView, self).get_initial(**kwargs)
        initial['enterprise'] = Enterprise.objects.get(pk=self.kwargs['enterprise_pk'])
        return initial


class FarmproductionRecordsList(LoginRequiredMixin, APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'farm_production_record_list.html'

    def get(self, request):
    
        return Response()

# update productionrecord view
class EditFarmproductionRecordView(LoginRequiredMixin,UpdateView):
    model =ProductionRecord
    template_name = 'create_farm_production_record.html'
    success_url = reverse_lazy('farm:productionrecords')
    form_class = FarmProductionRecordForm
    success_message = "Farm production Record has been updated successfully"


    def dispatch(self, request, *args, **kwargs):
        return super(EditFarmproductionRecordView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(EditFarmproductionRecordView, self).get_form_kwargs()
        kwargs['request'] = self.request
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
        productionrecord = form.save(commit=False)
        productionrecord.save()

         # send email to farmer  a message after an update
        current_site = get_current_site(self.request)
        subject = 'Production Record Updated Successfully'
        message = render_to_string('enterprise_email.html', {
            'user': self.request.user,
            'domain': current_site.domain,
            'message': 'Your Production record  '+productionrecord.record_name + ' has been updated sucessfully',
            })
        to_email = self.request.user.email
        email = EmailMessage(
                subject, message, to=[to_email]
            )
        email.content_subtype = "html"
        email.send()
        return redirect('farm:productionrecords')


    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(self.get_context_data(form=form))



# production record viewset
class FarmProductionRecordViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows sectors to be viewed or edited.
    """
    serializer_class = FarmProductionRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the farms 
        for the currently authenticated user.
        """
        user = self.request.user
        productionrecords = ProductionRecord.objects.all().order_by('enterprise')
        if self.request.user.is_superuser or self.request.user.groups.filter(name='UNFFE Agents').exists():
            queryset = productionrecords
        else:
            farmer = FarmerProfile.objects.get(user=user)
            farms = Farm.objects.filter(farmer =farmer)
            enterprises = Enterprise.objects.filter(farm__in=farms)
            queryset = productionrecords.filter(enterprise__in=enterprises)
        
        return queryset


class EnterpriseSelectionView(LoginRequiredMixin,CreateView):
    template_name = 'enterprise_selection.html'
    success_url = reverse_lazy('farm:select_enterpise')
    form_class = EnterpriseSelectionForm
    success_message = "Your answers were submitted successfully"
    crops_northen = ['cotton', 'millet', 'sorghum', 'legumes', 'sesame']#gulu, masindi
    crops_lango = ['cassava','maize','millet','rice','sesame'] #lira Apac
    crops_soroti = ['cotton','millet','ground nuts']#soroti, kumi, palisa
    crops_tororo = ['banana', 'cotton','millet','sorghum','maize'] #iganga, tororo, butaleja
    crops_western_savanna = ['banana','coffee','maize','cattle'] #masindi, hoima, kamwengye, luwero
    crops_lakevictoria = ['banana','coffee','maize','sweet potato','beans','vegetables', 'flowers']#wakiso, mukono, jinja, bugiri
   
    crops_karamoja = ['cattle','sorghum','maize','millet'] #moroto, kotido, karamoja
    crops_kabale = ['sorghum','solanun potato','vegetables','coffee','maize'] #kabale, sironko, mbale
   
    western_message = "Thank you for your interest in farming, We have analysed your personal profile and land profile and we would recommend the following"


    def dispatch(self, request, *args, **kwargs):
        return super(EnterpriseSelectionView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(EnterpriseSelectionView, self).get_form_kwargs()
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
        crops_ibanda = ['Diary cattle','Millet','Sorghum'] #mbarara, Bushenyi, Ibanda
        
        enterprise = form.save(commit=False)
        enterprise.user = self.request.user
        crops_info = []
       
        region = form.cleaned_data.get('region')
        #print(region.id)
        results = Ecological_Zones.objects.get(ecological_zone_name = region.id)
        print(results.crops.all())
        crops = results.crops.all()
        enterprise.recommendation = results

        enterprise.save()
        form.save_m2m()
        # context = {
        #     "crops":crops,
        # }

        
        # send email to farmer after registration
        current_site = get_current_site(self.request)
        subject = 'Registrated Service Successful'
        message = render_to_string('profile_created_successful.html', {
            'user': enterprise.user,
            'domain': current_site.domain
            })
        to_email = enterprise.user.email
        email = EmailMessage(
                subject, message, to=[to_email]
            )
        email.content_subtype = "html"
        #email.send()
        return redirect('farm:view_enterprise_selection', pk = enterprise.pk)

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(self.get_context_data(form=form))
    


"""
Enterprise selection redirect view
"""


class EnterpriseSelectionRedirect(LoginRequiredMixin, APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'enterprise_selection_list.html'

    def get(self, request):
       # queryset = Sector.objects.order_by('-id')
        return Response()

class EnterpriseSelectionDetailView(LoginRequiredMixin, DetailView):
    model = EnterpriseSelection
    context_object_name = "profilerecord"
    template_name = "enterprise_selection_redirect.html"

    def get_context_data(self, **kwargs):
        context = super(EnterpriseSelectionDetailView, self).get_context_data(**kwargs)
        
        context.update({

        })
        return context

class EnterpriseSelectionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows farms to be viewed or edited.
    """
    queryset = EnterpriseSelection.objects.all()
    serializer_class = EnterpriseSelectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the farmers profiles
        for the currently authenticated user.
        """
        user = self.request.user
        selections = EnterpriseSelection.objects.all().order_by('user')
        if  self.request.user.has_perm('selections.delete_EnterpriseSelection'):
            queryset = selections
        else:
            queryset = selections.filter(user=user)
        
        return queryset

    def create(self, request, format=None):
        serializer = PostEnterpriseSelectionSerializer(data=request.data)

        if serializer.is_valid():
            try:
                # serializer.status ='Pending'
                #serializer.user = self.request.user
                serializer.save(user = self.request.user)
            except Exception as e:
                return Response({'error':str(e)})
                 
            return Response({'status':'successful'})
        return Response(serializer.errors, status=400)

