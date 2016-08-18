"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from django.conf.urls import include, url, patterns
from django.contrib import admin
admin.autodiscover()
#user_views
from users.views import *
from users import views


#TrafficMonitor_views
from TrafficMonitor.views_dushboard_resources import *
from TrafficMonitor.views_resource_list import *
from TrafficMonitor.views_traffic_applications import *
from TrafficMonitor.views_traffic_report import *
from TrafficMonitor.views_netflow_query import *
from TrafficMonitor.views_netflow_transport import *
from TrafficMonitor.views_netflow_application import *
from TrafficMonitor.views_netflow_network import *
from TrafficMonitor.views_netflow_flow_stat import *
from TrafficMonitor.views_netflow_monitor import *
#DataManager_views
from DataManager.views import *

#ClusterManager
from ClusterManager.views_log_management import *
from ClusterManager.views_report_management import *
from ClusterManager.views_cluster_overview import *
from ClusterManager.views_job_management import *
from ClusterManager.ClusterOverview import *
from ClusterManager.cpu import *
from ClusterManager.memory import *
from ClusterManager.centosdisk import *
from ClusterManager.storm_cpu import *
from ClusterManager.storm_mem import *
from ClusterManager.hadoop_cpu import *
from ClusterManager.hadoop_mem import *
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
]

#Useroperation
urlpatterns += [
  
    url(r'^login/$', login.as_view()),
    url(r'^regist/$', regist.as_view()),
    url(r'^index2/$', index2.as_view()),
    url(r'^usermanage/$', usermanage.as_view()),
    url(r'^userpass/$', userpass.as_view()),
    url(r'^usernopass/$', usernopass.as_view()),
    url(r'^userpassed/$', userpassed.as_view()),

]

#TrafficMonitor
urlpatterns += [
    #dushboard_resources
    url(r'^RealtimeApplicationThroughput/Second$', RealtimeApplicationThroughput_Second.as_view()),
    url(r'^RealtimeApplicationThroughput/Minute$', RealtimeApplicationThroughput_Minute.as_view()),
    url(r'^RealtimeApplicationThroughput/$', RealtimeApplicationThroughput.as_view()),
    url(r'^RealtimeApplicationDataPacket/$', RealtimeApplicationDataPacket.as_view()),
    url(r'^RealtimeApplicationStream/$', RealtimeApplicationStream.as_view()),
    url(r'^RealtimeSourceCountryThroughput/$', RealtimeSourceCountryThroughput.as_view()),
    url(r'^RealtimeDestinationCountryThroughput/$', RealtimeDestinationCountryThroughput.as_view()),
    url(r'^RealtimeApplicationStatisticsForm/$', RealtimeApplicationStatisticsForm.as_view()),
    url(r'^RealtimeApplicationChart/$', RealtimeApplicationChart.as_view()),
    url(r'^RealtimeSourceCountryChart/$', RealtimeSourceCountryChart.as_view()),
    url(r'^RealtimeDestinationCountryChart/$', RealtimeDestinationCountryChart.as_view()),
   
    #new dashboard resource
    url(r'^Netflow/Transport/$', transport.as_view()),
    url(r'^Netflow/Application/$', application.as_view()),
    url(r'^Netflow/Network/$', network.as_view()),

    url(r'^Netflow/Flow_Stat/$', flow_stat.as_view()),
    url(r'^Netflow/Netflow_Monitor/$', netflow_monitor.as_view()),
    url(r'^Netflow/Netflow_Monitor_Table/$', netflow_monitor_table.as_view()),


    #netflow query interfaces
    url(r'^Netflow/Query/$', netflow_query.as_view()),

    #resource_list
    url(r'^ResourceList/$', ResourceList.as_view()),

    #traffic_applications
    url(r'^AnomlyDetections/$', AnomlyDetections.as_view()),
    url(r'^AnomlyDetectionsid/$', AnomlyDetectionsid.as_view()),

    #traffic_report
    url(r'^ReportForm/$', ReportForm.as_view()),

    #netflow_query
#   url(r'^NetflowQuery/$', Netflow_query.as_view()),
]

#DataManager
urlpatterns += [
    #history_data
   # url(r'^OfflineApplicationLayerResults/$', OfflineApplicationLayerResults.as_view()),
   # url(r'^OfflineTransportLayerResults/$', OfflineTransportLayerResults.as_view()),
   # url(r'^OfflineNetworkLayerResults/$', OfflineNetworkLayerResults.as_view()),

    url(r'^collect/$', collectreq.as_view()),
    url(r'^dataset/$', datasetshow.as_view()),
    url(r'^datacolreq/$', colreqshow.as_view()),
    url(r'^deleteds/$', deleteds.as_view()),
    url(r'^selectds/$', selectds.as_view())

    #dataset_query

    #apply_for_collection

    #management_application

]

#ClusterManager
urlpatterns += [
    #cluster_overview
    url(r'^ClusterOverview/$', ClusterOverview.as_view()),

    #job_management
    url(r'^JobManagement/$', JobManagement.as_view()),

    #log_management
    url(r'^LogManagement/$', LogManagement.as_view()),

    #report_management
    url(r'^ReportManagement/$', ReportManagement.as_view()),
    
    url(r'^ClusterOverview7/$', ClusterOverview7.as_view()),

    url(r'^ClusterOverview8/$', ClusterOverview8.as_view()),
    url(r'^ClusterOverview9/$', ClusterOverview9.as_view()),
    url(r'^ClusterOverview10/$', ClusterOverview10.as_view()),
    url(r'^cpu7/$', cpu7.as_view()),
    url(r'^cpu8/$', cpu8.as_view()),
    url(r'^cpu9/$', cpu9.as_view()),
    url(r'^cpu10/$', cpu10.as_view()),
    url(r'^cpu/$', cpu.as_view()),
    url(r'^memory7/$', memory7.as_view()),
    url(r'^memory8/$', memory8.as_view()),
    url(r'^memory9/$', memory9.as_view()),
    url(r'^memory10/$', memory10.as_view()),
    url(r'^memory/$', memory.as_view()),
    url(r'^centosdisk7/$', centosdisk7.as_view()),
    url(r'^centosdisk8/$', centosdisk8.as_view()),
    url(r'^centosdisk9/$', centosdisk9.as_view()),
    url(r'^centosdisk10/$', centosdisk10.as_view()),
    url(r'^centosdisk/$', centosdisk.as_view()),
    url(r'^storm_cpu7/$', storm_cpu7.as_view()),      
    url(r'^storm_cpu8/$', storm_cpu8.as_view()),
    url(r'^storm_cpu9/$', storm_cpu9.as_view()),
    url(r'^storm_cpu10/$', storm_cpu10.as_view()),
    url(r'^storm_cpu/$', storm_cpu.as_view()),
    url(r'^storm_mem7/$', storm_mem7.as_view()),
    url(r'^storm_mem8/$', storm_mem8.as_view()),
    url(r'^storm_mem9/$', storm_mem9.as_view()),
    url(r'^storm_mem10/$', storm_mem10.as_view()),
    url(r'^storm_mem/$', storm_mem.as_view()),
    url(r'^hadoop_cpu7/$', hadoop_cpu7.as_view()),
    url(r'^hadoop_cpu8/$', hadoop_cpu8.as_view()),
    url(r'^hadoop_cpu9/$', hadoop_cpu9.as_view()),
    url(r'^hadoop_cpu10/$', hadoop_cpu10.as_view()),
    url(r'^hadoop_cpu/$', hadoop_mem.as_view()),
    url(r'^hadoop_mem7/$', hadoop_mem7.as_view()),
    url(r'^hadoop_mem8/$', hadoop_mem8.as_view()),
    url(r'^hadoop_mem9/$', hadoop_mem9.as_view()),
    url(r'^hadoop_mem10/$', hadoop_mem10.as_view()),
    url(r'^hadoop_mem/$', hadoop_mem.as_view()),
]  
