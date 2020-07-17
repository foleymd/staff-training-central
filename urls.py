from django.conf.urls import patterns, url
from utch9e.web.stc import views
 
urlpatterns = patterns('', 
    	url(r'^index/$', views.index, name='index'),
    url(r'^class_delete/(?P<action>\w{1})/(?P<component>\w{1})/(?P<unique_number>\w{5})/(?P<course_category>\w{3})/(?P<course_number>\w{3})/$', views.delete_class, name='class_delete_a'),  
    
url(r'^class_delete/$', views.delete_class, name='class_delete'),
    url(r'^class_details/(?P<unique_number>\w{5})/(?P<success>\w{1})/(?P<action>\w{1})/$', views.classdetails, name='class_details_b'),
    
url(r'^class_details/(?P<unique_number>\w{5})/$', views.classdetails, name='class_details_a'),

    	url(r'^class_details/$', views.classdetails, name='class_details'),
    
url(r'^class_roster/(?P<unique_number>\w{5})/$', views.classroster, name='classroster_a'),
    
url(r'^class_roster/$', views.classroster, name='classroster'),
    url(r'^class_list/(?P<component>\w{1})/(?P<course_cat>\w{3})/(?P<course_num>\w{3})/(?P<success>\w{1})/(?P<unique_number>\w{5})/$', views.class_list, name='class_list_b'),
    url(r'^class_list/(?P<component>\w{1})/(?P<course_cat>\w{3})/(?P<course_num>\w{3})/$', views.class_list, name='class_list_a'),

    	url(r'^class_list/$', views.class_list, name='class_list'),
    url(r'^class_maintenance/(?P<action>\w{1})/(?P<component>\w{1})/(?P<course_category>\w{3})/(?P<course_number>\w{3})/$', views.store_class, name='class_maintenance_s'),
    url(r'^class_maintenance/(?P<action>\w{1})/(?P<component>\w{1})/(?P<unique_number>\w{5})/$', views.update_class, name='class_maintenance_u'),  
    
url(r'^class_maintenance/$', views.store_class, name='class_maintenance'),
    
url(r'^course_cat_list/(?P<component>\w{1})/$', views.course_cat_list, name='course_cat_list_a'),
    
url(r'^course_cat_list/$', views.course_cat_list, name='course_cat_list'),
    url(r'^course_details/(?P<component>\w{1})/(?P<course_cat>\w{3})/(?P<course_num>\w{3})/$', views.course_details, name='course_details_a'),

url(r'^course_details/$', views.course_details, name='course_details'),
    
url(r'^course_list/(?P<component>\w{1})/(?P<course_cat>\w{3})/$', views.course_num_list, name='course_list_a'),
    
url(r'^course_list/$', views.course_num_list, name='course_list'),
)
