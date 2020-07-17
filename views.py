from django.shortcuts import render_to_response
from utdirect.templates import UTDirectContext
from utbroker.errors import UTBrokerError
from dpch9e.web.utd_defaults import PROJECT_UTD_DEFAULTS

# PDA Imports
from dpdpindx import Dpdpindx
from nrdprosw import Nrdprosw

defaults = PROJECT_UTD_DEFAULTS

def index(request):
    '''Staff Training Central Homepage '''
    print 'hello'
    
    context = {}
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
    
def classroster(request):
    '''Class Roster'''
    
    print 'helloroster'
      
    context = {}
    
    nrdprosw = Nrdprosw()
    nrdprosw.send.webtoken = request.META['HTTP_TOKEN']
    nrdprosw.send.component = PROJECT_UTD_DEFAULTS['component']
    nrdprosw.send.class_unique_number = request.GET.get('class_unique', '')

    if 'next_page_submitted' in request.GET:
        nrdprosw.send.paging_isn = request.GET.get('paging_isn', '')
        nrdprosw.send.paging_name = request.GET.get('paging_name', '') 
        context['next_page_submitted'] = True 
     
    elif 'form_submitted' in request.GET:
        nrdprosw.send.paging_name = request.GET.get('start_name', '')
        context['form_submitted'] = True 

    try:
        nrdprosw.call_broker_once(service=request.META['HTTP_SERVICE'])
        
    except UTBrokerError as exception:
        context['exception_msg'] = str(exception)
        return render_to_response("utd_error.html", UTDirectContext(request,
                                                            context,
                                                            defaults=defaults,))
        
    if nrdprosw.recv.return_code.startswith('X'):
        context['return_msg'] = nrdprosw.recv.return_msg
        context['return_code'] = nrdprosw.recv.return_code
        return render_to_response("utd_error.html", UTDirectContext(request,
                                                            context,
                                                            defaults=defaults,)) 
         
    context['nrdprosw'] = nrdprosw
    
    if nrdprosw.recv.number_instructors_returned:
        context['instructors'] = nrdprosw.recv.instructor_info[:int(nrdprosw.recv.number_instructors_returned)]
    
    if nrdprosw.recv.number_enrollees_returned:
        context['enrollees'] = nrdprosw.recv.enrollee_info[:int(nrdprosw.recv.number_enrollees_returned)]
        
    return render_to_response("classroster.html", UTDirectContext(request, 
                                                           context, 
                                                           defaults=defaults, 
                                                           document_title=
                                                           'Class Roster Search',))
