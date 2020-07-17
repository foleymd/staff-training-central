from django.shortcuts import render_to_response, redirect
from utdirect.templates import UTDirectContext
from utbroker.errors import UTBrokerError
from dpch9e.web.utd_defaults import PROJECT_UTD_DEFAULTS
from django.core.context_processors import csrf
from dpch9e.web.stc.constants import TIME_HHII, YEAR, MONTH, DAY, LOCATION
# from dpch9e.web import settings

# PDA Imports
from dpdpindx import Dpdpindx
from utdprosw import Utdprosw
from dpdpccls import Dpdpccls
from dpdpcour import Dpdpcour
from dpdpcrsl import Dpdpcrsl
from dpdplist import Dpdplist
from utdp9euw import Utdp9euw
from utdp9erw import Utdp9erw

defaults = PROJECT_UTD_DEFAULTS

def index(request):
    '''Staff Training Central Homepage '''
    
    context = {}
    context['http_service'] = request.META['HTTP_SERVICE']
    dpdpindx = Dpdpindx()
          
    dpdpindx.send.webtoken = request.META['HTTP_TOKEN']
    dpdpindx.send.component = PROJECT_UTD_DEFAULTS['component']
       
    try:
        dpdpindx.call_broker_once(service=request.META['HTTP_SERVICE'])
        
    except UTBrokerError as exception:
        context['exception_msg'] = str(exception)
        return render_to_response("utd_error.html", UTDirectContext(request,
                                                            context,
                                                            defaults=defaults,))
        
    if dpdpindx.recv.return_code.startswith('X'):
        context['exception_msg'] = dpdpindx.recv.return_msg
        return render_to_response("utd_error.html", UTDirectContext(request,
                                                            context,
                                                            defaults=defaults,))
         
    context['dpdpindx'] = dpdpindx
    return render_to_response("index.html", UTDirectContext(request,
                                                           context,
                                                           defaults=defaults,
                                                           document_title=
                                                           'Staff Training Central'))
    
def course_cat_list (request, component=0):
    '''Retrieves Course Category List'''
    
    context = {}
    context['http_service'] = request.META['HTTP_SERVICE']
    dpdpccls = Dpdpccls()

    try:
        dpdpccls.send.webtoken = request.META['HTTP_TOKEN']
        dpdpccls.send.component = component
        dpdpccls.call_broker_once(service=request.META['HTTP_SERVICE'])
        
    except UTBrokerError, e:
        context['exception_msg'] = str(e)
        return render_to_response("utd_error.html", UTDirectContext(request,
                                                            context,
                                                            defaults=defaults))
        
    context['dpdpccls'] = dpdpccls
    
    return render_to_response("course_cat_list.html", UTDirectContext(request,
                                                           context,
                                                           defaults=defaults,))

def course_num_list(request, component, course_cat):
    '''Retrieves Course Number list for a given category'''
    
    context = {}
    context['http_service'] = request.META['HTTP_SERVICE']
    dpdpcrsl = Dpdpcrsl()

    try:
        dpdpcrsl.send.webtoken = request.META['HTTP_TOKEN']
        dpdpcrsl.send.component = component
        dpdpcrsl.send.course_category = course_cat
        dpdpcrsl.call_broker_once(service=request.META['HTTP_SERVICE'])
                
    except UTBrokerError, e:
        context['exception_msg'] = str(e)
        return render_to_response("utd_error.html", UTDirectContext(request,
                                                            context,
                                                            defaults=defaults,))
    
    context['dpdpcrsl'] = dpdpcrsl
        
    return render_to_response("course_list.html", UTDirectContext(request,
                                                           context,
                                                           defaults=defaults,))

def course_details(request, component, course_cat, course_num):
    '''Retrieves Course Details for a given component and course id'''
    
    context = {}
    context['http_service'] = request.META['HTTP_SERVICE']
    dpdpcour = Dpdpcour()

    try:
        dpdpcour.send.webtoken = request.META['HTTP_TOKEN']
        dpdpcour.send.component = component
        dpdpcour.send.course_category = course_cat
        dpdpcour.send.course_number = course_num
        dpdpcour.call_broker_once(service=request.META['HTTP_SERVICE'])
                
    except UTBrokerError, e:
        context['exception_msg'] = str(e)
        return render_to_response("utd_error.html", UTDirectContext(request,
                                                            context,
                                                            defaults=defaults,))
        
    if dpdpcour.recv.return_code.startswith('X'):
        context['exception_msg'] = dpdpcour.recv.return_msg
        return render_to_response("utd_error.html", UTDirectContext(request,
                                                                        context,
                                                                defaults=defaults,))
            
    context['dpdpcour'] = dpdpcour
        
    return render_to_response("course_details.html", UTDirectContext(request,
                                                           context,
                                                           defaults=defaults,))

def class_list(request, component, course_cat, course_num, success='', unique_number=''):
    '''Retrieves a Class List for a given component and course id'''
    
    context = {}
    context['http_service'] = request.META['HTTP_SERVICE']
    context['success'] = success
    context['unique_number'] = unique_number
    dpdplist = Dpdplist()
    

    try:
        dpdplist.send.webtoken = request.META['HTTP_TOKEN']
        dpdplist.send.component = component
        dpdplist.send.course_category = course_cat
        dpdplist.send.course_number = course_num
        dpdplist.call_broker_once(service=request.META['HTTP_SERVICE'])
                
    except UTBrokerError, e:
        context['exception_msg'] = str(e)
        return render_to_response("utd_error.html", UTDirectContext(request,
                                                            context,
                                                            defaults=defaults,))
    
    context['dpdplist'] = dpdplist
        
    return render_to_response("class_list.html", UTDirectContext(request,
                                                           context,
                                                           defaults=defaults,))
        
def classroster(request):
    '''given unique number input, will return class roster'''
    
    context = {}
    context['http_service'] = request.META['HTTP_SERVICE']
     
    utdprosw = Utdprosw()
    utdprosw.send.webtoken = request.META['HTTP_TOKEN']
    utdprosw.send.component = PROJECT_UTD_DEFAULTS['component']
    utdprosw.send.class_unique_number = request.GET.get('class_unique', '')
 
    if 'next_page_submitted' in request.GET:
        utdprosw.send.paging_isn = request.GET.get('paging_isn', '')
        utdprosw.send.paging_name = request.GET.get('paging_name', '')
        context['next_page_submitted'] = True
      
    elif 'form_submitted' in request.GET:
        utdprosw.send.paging_name = request.GET.get('start_name', '')
        context['form_submitted'] = True
 
    try:
        utdprosw.call_broker_once(service=request.META['HTTP_SERVICE'])
         
    except UTBrokerError as exception:
        context['exception_msg'] = str(exception)
        return render_to_response("utd_error.html", UTDirectContext(request,
                                                            context,
                                                            defaults=defaults,))
         
    if utdprosw.recv.return_code.startswith('X'):
        context['return_msg'] = utdprosw.recv.return_msg
        context['return_code'] = utdprosw.recv.return_code
        return render_to_response("utd_error.html", UTDirectContext(request,
                                                            context,
                                                            defaults=defaults,))
          
    context['utdprosw'] = utdprosw
     
    if utdprosw.recv.number_instructors_returned:
        context['instructors'] = utdprosw.recv.instructor_info[:int(utdprosw.recv.number_instructors_returned)]
     
    if utdprosw.recv.number_enrollees_returned:
        context['enrollees'] = utdprosw.recv.enrollee_info[:int(utdprosw.recv.number_enrollees_returned)]
         
    return render_to_response("class_roster.html", UTDirectContext(request,
                                                           context,
                                                           defaults=defaults,
                                                           document_title=
                                                           'Class Roster Search',))
   
def classdetails(request, unique_number='', success='', action=''):
    '''Given unique number input, will return class details'''
     
    context = {}
    context['TIME_HHII'] = TIME_HHII
    context['http_service'] = request.META['HTTP_SERVICE']
    context['success'] = success
    context['action'] = action
    
    pda = Utdp9erw()
    pda.send.webtoken = request.META['HTTP_TOKEN']
    pda.send.component = PROJECT_UTD_DEFAULTS['component']
    pda.send.class_unique_number = unique_number or request.GET.get('unique_number', '')
    
    context['service'] = request.META['HTTP_SERVICE']
       
    try:
        pda.call_broker_once(service=request.META['HTTP_SERVICE'])
        
    except UTBrokerError as exception:
        context['exception_msg'] = str(exception)
        return render_to_response("utd_error.html", UTDirectContext(request,
                                                            context,
                                                            defaults=defaults,))
        
    if pda.recv.return_code.startswith('X'):
        context['return_msg'] = pda.recv.return_msg
        context['return_code'] = pda.recv.return_code
        return render_to_response("utd_error.html", UTDirectContext(request,
                                                            context,
                                                            defaults=defaults,))
    
    context['pda'] = pda
         
    context['class_unique_number_send'] = pda.send.class_unique_number
    context['instructor_eid_1'] = pda.recv.instructor_eid[0]
    context['instructor_type_1'] = pda.recv.instructor_type[0]
    context['instructor_eid_2'] = pda.recv.instructor_eid[1]
    context['instructor_type_2'] = pda.recv.instructor_type[1]
    context['instructor_eid_3'] = pda.recv.instructor_eid[2]
    context['instructor_type_3'] = pda.recv.instructor_type[2]
    context['instructors'] = pda.recv.instructor_info
    
    if 'form_submitted' in request.GET:
        context['form_submitted'] = True
        
    return render_to_response("class_details.html", UTDirectContext(request,
                                                           context,
                                                           defaults=defaults,
                                                           document_title=
                                                           'Class Details Search',))

# IN PROD, COMBINE UPDATE CLASS AND STORE CLASS.
  
def store_class(request, action='', component=0, unique_number='', course_category='', course_number=''):
    '''Store a New Class'''
        
    context = {}
    context['TIME_HHII'] = TIME_HHII
    context['YEAR'] = YEAR
    context['MONTH'] = MONTH
    context['DAY'] = DAY
    context['LOCATION'] = LOCATION
    context['http_service'] = request.META['HTTP_SERVICE']
        
    pda = Utdp9euw()
    pda.send.webtoken = request.META['HTTP_TOKEN']
    
    pda.send.action = action
    pda.send.component = component
    pda.send.class_unique_number = request.POST.get('class_unique_number', '')
    pda.send.course_id = request.POST.get('course_id', '')
    pda.send.course_category = course_category
    pda.send.course_number = course_number
    pda.send.class_meeting_cy = request.POST.get('class_meeting_cy', '')
    pda.send.class_meeting_m = request.POST.get('class_meeting_m', '')
    pda.send.class_meeting_d = request.POST.get('class_meeting_d', '')
    pda.send.enrollment_limit = request.POST.get('enrollment_limit', 0)
    pda.send.student_fee = request.POST.get('student_fee', 0)
    pda.send.class_begin_time_hhii = request.POST.get('class_begin_time_hhii', '')
    pda.send.class_end_time_hhii = request.POST.get('class_end_time_hhii', '')
    pda.send.location = request.POST.get('location', '')
    pda.send.instructor_eid[0] = request.POST.get('instructor_eid_1', '')
    pda.send.instructor_type[0] = request.POST.get('instructor_type_1', '')
    pda.send.instructor_eid[1] = request.POST.get('instructor_eid_2', '')
    pda.send.instructor_type[1] = request.POST.get('instructor_type_2', '')
    pda.send.instructor_eid[2] = request.POST.get('instructor_eid_3', '')
    pda.send.instructor_type[2] = request.POST.get('instructor_type_3', '')
    pda.send.misc_instructions = request.POST.get('misc_instructions', '')

    if 'form_submitted' in request.POST:
        context['form_submitted'] = True
        pda.send.course_category = request.POST.get('course_category', '')
        pda.send.course_number = request.POST.get('course_number', '')
       
    try:
        pda.call_broker_once(service=request.META['HTTP_SERVICE'])
        
    except UTBrokerError as exception:
        context['exception_msg'] = str(exception)
        return render_to_response("utd_error.html", UTDirectContext(request,
                                                            context,
                                                            defaults=defaults,))
        
    if pda.recv.return_code.startswith('X'):
        context['return_code'] = pda.recv.return_code
        context['return_msg'] = pda.recv.return_msg
        return render_to_response("utd_error.html", UTDirectContext(request,
                                                            context,
                                                            defaults=defaults,))

    if pda.recv.return_code:
# In case of error, the context dictionary below will allow the form to retain
# the user inputs.
        context['pda'] = pda
        context['action'] = action
        context['instructor_eid_1'] = pda.send.instructor_eid[0]
        context['instructor_type_1'] = pda.send.instructor_type[0]
        context['instructor_eid_2'] = pda.send.instructor_eid[1]
        context['instructor_type_2'] = pda.send.instructor_type[1]
        context['instructor_eid_3'] = pda.send.instructor_eid[2]
        context['instructor_type_3'] = pda.send.instructor_type[2]
        context['misc_instructions'] = pda.send.misc_instructions
        context['instructors'] = pda.send.instructor_info
                     
        return render_to_response("class_maintenance.html", UTDirectContext(request,
                                                           context,
                                                           defaults=defaults,
                                                           document_=
                                                           'Class Maintenance'))
    
    return redirect('class_details_b', unique_number = pda.recv.new_unique_number, success = 'Y', action = 'S')
       


def update_class(request, action='', component=0, unique_number='', course_category='', course_number=''):
    '''Update a Class'''
          
    context = {}
    context['TIME_HHII'] = TIME_HHII
    context['YEAR'] = YEAR
    context['MONTH'] = MONTH
    context['DAY'] = DAY
    context['LOCATION'] = LOCATION
    context['http_service'] = request.META['HTTP_SERVICE']
    context['action'] = action
     
    if request.method == 'GET':
                      
        utdp9erw = Utdp9erw()
        utdp9erw.send.webtoken = request.META['HTTP_TOKEN']
        utdp9erw.send.component = PROJECT_UTD_DEFAULTS['component']
        utdp9erw.send.class_unique_number = unique_number or request.GET.get('unique_number', '')
      
        try:
            utdp9erw.call_broker_once(service=request.META['HTTP_SERVICE'])
          
        except UTBrokerError as exception:
            context['exception_msg'] = str(exception)
            return render_to_response("utd_error.html", UTDirectContext(request,
                                                       context,
                                                            defaults=defaults,))
          
        if utdp9erw.recv.return_code.startswith('X'):
            context['return_msg'] = utdp9erw.recv.return_msg
            context['return_code'] = utdp9erw.recv.return_code
            return render_to_response("utd_error.html", UTDirectContext(request,
                                                            context,
                                                            defaults=defaults,))
        
        context['pda'] = utdp9erw
        context['instructor_eid_1'] = utdp9erw.recv.instructor_eid[0]
        context['instructor_type_1'] = utdp9erw.recv.instructor_type[0]
        context['instructor_eid_2'] = utdp9erw.recv.instructor_eid[1]
        context['instructor_type_2'] = utdp9erw.recv.instructor_type[1]
        context['instructor_eid_3'] = utdp9erw.recv.instructor_eid[2]
        context['instructor_type_3'] = utdp9erw.recv.instructor_type[2]
        context['instructors'] = utdp9erw.recv.instructor_info

        if utdp9erw.recv.nbr_of_instructors:
            context['instructors'] =
            utdp9erw.recv.instructor_info[:int(utdp9erw.recv.nbr_of_instructors)]
          
        return render_to_response("class_maintenance.html", UTDirectContext(request,
                                                           context,
                                                           defaults=defaults,
                                                           document_title=
                                                           'Class Maintenance'))
              
    utdp9euw = Utdp9euw()
    utdp9euw.send.webtoken = request.META['HTTP_TOKEN']
    utdp9euw.send.action = action
    utdp9euw.send.component = component
    utdp9euw.send.class_unique_number = unique_number
    utdp9euw.send.class_meeting_cy = request.POST.get('class_meeting_cy', '')
    utdp9euw.send.class_meeting_m = request.POST.get('class_meeting_m', '')
    utdp9euw.send.class_meeting_d = request.POST.get('class_meeting_d', '')
    utdp9euw.send.enrollment_limit = request.POST.get('enrollment_limit', 0)
    utdp9euw.send.student_fee = request.POST.get('student_fee', 0)
    utdp9euw.send.class_begin_time_hhii = request.POST.get('class_begin_time_hhii', '')
    utdp9euw.send.class_end_time_hhii = request.POST.get('class_end_time_hhii', '')
    utdp9euw.send.location = request.POST.get('location', '')
    utdp9euw.send.instructor_eid[0] = request.POST.get('instructor_eid_1', '')
    utdp9euw.send.instructor_type[0] = request.POST.get('instructor_type_1', '')
    utdp9euw.send.instructor_eid[1] = request.POST.get('instructor_eid_2', '')
    utdp9euw.send.instructor_type[1] = request.POST.get('instructor_type_2', '')
    utdp9euw.send.instructor_eid[2] = request.POST.get('instructor_eid_3', '')
    utdp9euw.send.instructor_type[2] = request.POST.get('instructor_type_3', '')
    utdp9euw.send.misc_instructions = request.POST.get('misc_instructions', '')
  
    if 'form_submitted' in request.POST:
        context['form_submitted'] = True
        utdp9euw.send.course_category = request.POST.get('course_category', '')
        utdp9euw.send.course_number = request.POST.get('course_number', '')
     
    try:
        utdp9euw.call_broker_once(service=request.META['HTTP_SERVICE'])
      
    except UTBrokerError as exception:
        context['exception_msg'] = str(exception)
        return render_to_response("utd_error.html", UTDirectContext(request,
                                                                    context,
                                                                 defaults=defaults,))
      
    if utdp9euw.recv.return_code.startswith('X'):
        context['exception_msg'] = dpdpindx.recv.return_msg
        return render_to_response("utd_error.html", UTDirectContext(request,
                                                        context,
                                                        defaults=defaults,))

    if utdp9euw.recv.return_code:
        context['pda'] = utdp9euw
        context['instructor_eid_1'] = utdp9euw.recv.instructor_eid[0]
        context['instructor_type_1'] = utdp9euw.recv.instructor_type[0]
        context['instructor_eid_2'] = utdp9euw.recv.instructor_eid[1]
        context['instructor_type_2'] = utdp9euw.recv.instructor_type[1]
        context['instructor_eid_3'] = utdp9euw.recv.instructor_eid[2]
        context['instructor_type_3'] = utdp9euw.recv.instructor_type[2]
        context['instructors'] = utdp9euw.recv.instructor_info
        context['new_unique_number_for_store'] = utdp9euw.recv.new_unique_number
            
        return render_to_response("class_maintenance.html", UTDirectContext(request,
                                                           context,
                                                           defaults=defaults,
                                                           document_title=
                                                           'Class Maintenance'))
               
    return redirect('class_details_b', unique_number = utdp9euw.send.class_unique_number, success = 'Y', action = 'U')

   
def delete_class(request, action='', component=0, unique_number='', course_category='', course_number=''):
    '''Delete Class'''
        
    context = {}
    context['http_service'] = request.META['HTTP_SERVICE']
        
    pda = Utdp9euw()
    pda.send.webtoken = request.META['HTTP_TOKEN']
    
    pda.send.action = action
    pda.send.component = component
    pda.send.class_unique_number = unique_number
    pda.send.course_category = course_category
    pda.send.course_number = course_number

    if 'delete_submitted' in request.POST:
        context['delete_submitted'] = True
       
        try:
            pda.call_broker_once(service=request.META['HTTP_SERVICE'])
          
        except UTBrokerError as exception:
            context['exception_msg'] = str(exception)
            return render_to_response("utd_error.html", UTDirectContext(request,
                                                            context,
                                                            defaults=defaults,))
        
        if pda.recv.return_code.startswith('X'):
            context['exception_msg'] = pda.recv.return_msg
            return render_to_response("utd_error.html", UTDirectContext(request,
                                                                        context,
                                                                defaults=defaults,))
         
    context['action'] = action
    context['component'] = component
    context['class_unique_number'] = unique_number
    context['course_id'] = pda.send.course_id
    context['course_category'] = pda.send.course_category
    context['course_number'] = pda.send.course_number
    context['return_code'] = pda.recv.return_code
    context['return_msg'] = pda.recv.return_msg
    
    print 'course category', pda.recv.course_category

    if not pda.recv.return_code:
        if 'delete_submitted' in request.POST:
            return redirect('class_list_b',
                            component = pda.recv.component,
                            course_cat = pda.recv.course_category,
                            course_num = pda.recv.course_number,
                            success = 'Y',
                            unique_number = pda.send.class_unique_number
                           )
       
    return render_to_response("class_delete.html", UTDirectContext(request,
                                                           context,
                                                           defaults=defaults,
                                                           document_title=
                                                           'Delete Class'))
