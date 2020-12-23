from navutils import menu
main_menu = menu.Menu('main')
menu.register(main_menu)

# function to check whether a user belongs to a certain group
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists() 

# function to check wether a user has permissions to view farmers
def can_view_farmers(user, context):
    if user.is_superuser:
        return True
    return user.has_perm('farmer.view_farmerprofile')

def can_view_users(user, context):
    if user.is_superuser:
        return True
    return user.has_perm('auth.view_user')

# function to check whether a user is a unffeagent
def is_unffeagent(user, context):
    if user.is_superuser:
        return True
    return has_group(user, 'UNFFE Agents') 
# function to check whether a user has permissions to view farmers groups
def can_view_farmer_groups(user, context):
    if user.is_superuser:
        return True
    return user.has_perm('farmer.view_group')

def can_add_farmer_profile(user, context):
    if user.is_superuser:
        return True
    return user.has_perm('farmer.add_farmerprofile')

def can_view_farms(user, context):
    if user.is_superuser:
        return True
    return user.has_perm('farm.view_farm')

def can_view_enterprise(user, context):
    if user.is_superuser:
        return True
    return user.has_perm('farm.view_enterprise')

def can_view_farm_records(user, context):
    if user.is_superuser:
        return True
    return user.has_perm('farm.view_farmrecord')

def can_view_financial_records(user, context):
    if user.is_superuser:
        return True
    return user.has_perm('farm.view_financialrecord')


def can_view_production_records(user, context):
    if user.is_superuser:
        return True
    return user.has_perm('farm.view_productionrecord')

def can_view_pest_and_diseases(user, context):
    if user.is_superuser:
        return True
    return user.has_perm('farm.view_pest_and_diseases')

def can_view_queries(user, context):
    if user.is_superuser:
        return True
    return user.has_perm('farm.view_query')

def can_add_resources(user, context):
    if user.is_superuser:
        return user.has_perm('resourcesharing.add_resource')

def can_view_resources(user, context):
    if user.is_superuser:
        return True
    return user.has_perm('resourcesharing.view_resource') or user.has_perm('resourcesharing.add_resource')

def can_view_service_provider(user, context):
    if user.is_superuser:
        return True
    return user.has_perm('openmarket.view_serviceprovider')

def can_add_service_provider(user, context):
    if user.is_superuser:
        return True

    return user.has_perm('openmarket.add_serviceprovider')

def can_register_services(user, context):
    if user.is_superuser:
        return True
    return user.has_perm('openmarket.add_service')

def can_view_services(user, context):
    if user.is_superuser:
        return True
    return user.has_perm('openmarket.view_service')

def can_add_seller(user, context):
    if user.is_superuser:
        return True
    return user.has_perm('openmarket.add_seller')
    
        


def can_view_sellers(user, context):
    if user.is_superuser:
        return True
    return user.has_perm('openmarket.view_seller') and not has_group(user,"Farmers")
    
def can_view_products(user, context):
     if user.is_superuser:
        return True
     return user.has_perm('openmarket.view_product')

def can_view_unffeagents(user, context):
   
   
    if user.is_superuser:
        return True
    return user.has_perm('unffeagents.view_agentprofile')

def can_register_agent(user, context):
    if user.is_superuser:
        return True
    return user.has_perm('unffeagents.add_agentprofile')


def can_view_notifications(user, context):
    if user.is_superuser:
        return True
    return user.has_perm('unffeagents.view_notice')

def can_add_product(user, context):
    if user.is_superuser:
        return True
    return user.has_perm('openmarket.add_product')


def can_view_weather(user, context):
    if user.is_superuser:
        return True
    return user.has_perm('weather.view_communityweather')

def can_view_enterprise_selection(user, context):
    if user.is_superuser:
        return True
    return user.has_perm('farm.view_enterpriseselection')

def can_add_enterprise_selection(user, context):
    if user.is_superuser:
        return True

    return user.has_perm('farm.add_enterpriseselection')

menus = [
    menu.Node(id='dashboard',css_class="sidebar-header", label='<i data-feather="home"></i><span>Dashboard</span>', pattern_name='common:home', link_attrs={'id': 'dashboard'}),
    
    menu.PassTestNode(
        id='Enterprise-selection-section',
        css_class="sidebar-header",
        label='<span class="fas fa-briefcase"></span>  <span>Agric Enterprise</span><i class="fas fa-angle-right fa-pull-right"></i>',
        url='#',
        test=can_view_service_provider,
        children=[
            
            menu.PassTestNode(id='provider_list',
                              label='<i class="fa fa-circle"></i>Enterprise Selection',
                             
                              pattern_name='farm:select_enterpise', test=can_view_service_provider),
           
        ]
    ),
   
    menu.PassTestNode(
        id='farmer-section',
        css_class="sidebar-header",
        label='<span class="fas fa-person-booth"></span>  <span>Farmer Profile</span><i class="fas fa-angle-right fa-pull-right"></i>',
        url='#',
        test=can_view_farmers,
        children=[
            menu.PassTestNode(id='farmers',
                              label='<i class="fa fa-circle"></i>{% if  request.user.is_superuser %} Manage Applications {% else %}My Application{% endif %}',
                             
                              pattern_name='farmer:farmerprofile_list', test=can_view_farmers),
            menu.PassTestNode(id='farmer_groups',
                              label='<i class="fa fa-circle"></i>Farmer Groups',
                             
                              pattern_name='farmer:group_list', test=can_view_farmer_groups),
         
         
        ]
    ),
      menu.PassTestNode(
        id='farm-section',
        css_class="sidebar-header",
        label='<span class="fas fa-tractor"></span>  <span>Farm Management</span><i class="fa fa-angle-right fa-pull-right"></i>',
        url='#',
        test=can_view_farms,
        children=[

        
            menu.PassTestNode(id='farms',
                              label='<i class="fa fa-circle"></i>Farms',
                             
                              pattern_name='farm:farm_list', test=can_view_farms),
           
            menu.PassTestNode(id='enterprises',
                              label='<i class="fa fa-circle"></i>Enterprises',
                                        
                             pattern_name='farm:enterprise_list', test=can_view_enterprise),

            menu.PassTestNode(id='farmrecords',
                              label='<i class="fa fa-circle"></i>Farm Records',
                             
                              pattern_name='farm:farmrecords', test=can_view_farm_records),
            menu.PassTestNode(id='financialrecords',
                              label='<i class="fa fa-circle"></i>Financial Records',
                             
                              pattern_name='farm:financialrecords', test=can_view_financial_records),
         
            menu.PassTestNode(id='productionrecords',
                              label='<i class="fa fa-circle"></i>Production Records',
                             
                              pattern_name='farm:productionrecords', test=can_view_production_records),
                              

            menu.PassTestNode(id='pests_and_diseases',
                              label='<i class="fa fa-circle"></i>Queries',
                             
                              pattern_name='farm:query_list', test=can_view_queries),

         
        ]
    ),


    menu.PassTestNode(
        id='provider-section',
        css_class="sidebar-header",
        label='<span class="fas fa-people-carry"></span>  <span>Service Providers</span><i class="fas fa-angle-right fa-pull-right"></i>',
        url='#',
        test=can_view_service_provider,
        children=[
            menu.PassTestNode(id='provider-children',
                              label='<i class="fa fa-circle"></i>{% if  request.user.is_superuser %} Manage Applications {% else %}My Applications{% endif %}',
                             
                              pattern_name='openmarket:serviceprovider_list', test=can_view_service_provider),
            
         
        ]
    ),

menu.PassTestNode(
        id='Service-section',
        css_class="sidebar-header",
        label='<i data-feather="truck"></i><span>Manage Services</span><i class="fa fa-angle-right fa-pull-right"></i>',
        url='#',
        test=can_view_services,
        children=[
            
            menu.PassTestNode(id='register_service',
                              label='<i class="fa fa-circle"></i>Register',
                             
                              pattern_name='openmarket:service_registration', test=can_register_services),
            menu.PassTestNode(id='services',
                              label='<i class="fa fa-circle"></i>My Services',
                             
                              pattern_name='openmarket:serviceregistration_list', test=can_view_services),
 
         
        ]
    ),


    #Open market menu

menu.PassTestNode(
        id='Open-Market-section',
        css_class="sidebar-header",
        label='<span class="fas fa-balance-scale"></span>  <span>Open Market</span><i class="fa fa-angle-right fa-pull-right"></i>',
        url='#',
        test=can_view_service_provider,
        children=[
          
       
            # menu.PassTestNode(id='register_service',
            #                   label='<i class="fa fa-circle"></i>Register Market',
                             
            #                   pattern_name='openmarket:service_registration', test=can_register_services),
            # menu.PassTestNode(id='services',
            #                   label='<i class="fa fa-circle"></i>Markets',
                             
            #                   pattern_name='openmarket:serviceregistration_list', test=can_view_services),
            # menu.PassTestNode(id='services',
            #                   label='<i class="fa fa-circle"></i>Hire',
                             
            #                   pattern_name='openmarket:serviceregistration_list', test=can_view_services),
 
         
         
        ]
    ),



    menu.PassTestNode(
        id='Seller-section',
        css_class="sidebar-header",
        label='<i data-feather="users"></i><span>Seller Profile</span><i class="fa fa-angle-right fa-pull-right"></i>',
        url='#',
        test=can_view_sellers,
        children=[
            menu.PassTestNode(id='seller_registration',
                              label='<i class="fa fa-circle"></i>{% if  request.user.is_superuser %} Manage Applications {% else %}My Application{% endif %}',
                             
                              pattern_name='openmarket:seller_list', test=can_add_seller),
            # menu.PassTestNode(id='seller_list',
            #                   label='<i class="fa fa-circle"></i>Applications',
                             
            #                   pattern_name='openmarket:seller_list', test=can_view_sellers),
           
         
        ]
    ),

  menu.PassTestNode(
        id='product-section',
        css_class="sidebar-header",
        label='<span class="fas fa-lemon"></span>  <span>My Products</span><i class="fa fa-angle-right fa-pull-right"></i>',
        url='#',
        test=can_view_products,
        children=[
            menu.PassTestNode(id='create_product',
                              label='<i class="fa fa-circle"></i>Add Products',
                             
                              pattern_name='openmarket:create_product', test=can_add_product),
            menu.PassTestNode(id='product_list',
                              label='<i class="fa fa-circle"></i>Products',
                             
                              pattern_name='openmarket:product_list', test=can_view_products),
         
        ]
    ),

 menu.PassTestNode(
        id='agent-section',
        css_class="sidebar-header",
        label='<span class="fas fa-headset"></span>  <span>Call Center</span><i class="fa fa-angle-right fa-pull-right"></i>',
        url='#',
        test=is_unffeagent,
        children=[
            menu.PassTestNode(id='agent_registration',
                              label='<i class="fa fa-circle"></i>Register Agent',
                             
                              pattern_name='unffeagents:create_agentprofile', test=can_register_agent),
            menu.PassTestNode(id='agents_list',
                              label='<i class="fa fa-circle"></i>View UNFFE Agents',
                             
                              pattern_name='unffeagents:agentprofile_list', test=can_view_unffeagents),
            menu.PassTestNode(id='calls_list',
                              label='<i class="fa fa-circle"></i>Calls',
                             
                              pattern_name='unffeagents:calls', test=can_view_unffeagents),
            menu.PassTestNode(id='enquiry_list',
                              label='<i class="fa fa-circle"></i>Enquiries',
                             
                              pattern_name='unffeagents:enquiries', test=can_view_unffeagents),
            menu.PassTestNode(id='user_list',
                              label='<i class="fa fa-circle"></i>System User',
                             
                              pattern_name='unffeagents:users_list', test=can_view_users),
           
         
           
         
        ]
    ),
    menu.PassTestNode(
        id='Seller-resource-sharing',
        css_class="sidebar-header",
        label='<span class="fas fa-store"></span>  <span>Resource Sharing</span><i class="fa fa-angle-right fa-pull-right"></i>',
        url='#',
        test=can_view_resources,
        children=[
            # menu.PassTestNode(id='create_resource',
            #                   label='<i class="fa fa-circle"></i>Share Resource',
                             
                            #   pattern_name='resourcesharing:create_resource', test=can_add_resources),
            menu.PassTestNode(id='resource_list',
                              label='<i class="fa fa-circle"></i>{% if  request.user.is_superuser %} Manage resources {% else %}Share Resource{% endif %}',
                             
                              pattern_name='resourcesharing:resource_list', test=can_view_resources),
           
         
        ]
    ),
     menu.PassTestNode(id='notifications',
                              label='<i data-feather="bell"></i>Alert & Opportunities',
                             
                              pattern_name='unffeagents:notice_list', test=can_view_notifications),
    menu.PassTestNode(id='weather',css_class="sidebar-header", label='<span class="fas fa-cloud-sun"></span> <span>Micro Weather Services</span>',test=can_view_weather, pattern_name='weather:communityweather_list', link_attrs={'id': 'weather'}),

]
for entry in menus:
    main_menu.register(entry)