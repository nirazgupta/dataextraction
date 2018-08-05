from django.conf.urls import url
from . import views


urlpatterns = [
    # url(r'^$', views.HomePageView.as_view(), name='index'),
    url(r'^$', views.file_add, name='index'),
    url(r'^files/', views.DocumentView, name='files'),
    url(r'^details/(?P<id>\d+)/$', views.details, name='details'),
    url(r'^pdfExtract/(?P<id>\d+)/$', views.pdfExtract, name='pdfExtract'),
    url(r'^dxfExtract/(?P<id>\d+)/$', views.dxfExtract, name='dxfExtract'),
    url(r'^deletepdf/(?P<id>\d+)/$', views.deletePdfFile, name='deletePdf'),
    url(r'^deletedxf/(?P<id>\d+)/$', views.deleteDxfFile, name='deletedxf'),
    url(r'^viewImage/(?P<id>\d+)/$', views.viewImages, name='viewImage'),
    url(r'^viewPdfText/(?P<id>\d+)/$', views.viewPdfText, name='viewPdfText'),
    url(r'^viewText/(?P<id>\d+)/$', views.showText, name='viewText'),
    url(r'^viewCsv/(?P<id>\d+)/$', views.showCsv, name='viewCsv'),
    
    
    # url(r'^index$', views.index, name='index'),
    # url(r'^loan/$', views.loan, name='loan'),
    # url(r'^user/$', views.user, name='user'),
    # url(r'^show_data/$', views.show_data, name='show_data'),
    # url(r'^clear/$', views.clear_session, name='clear_session'),
    # url(r'^show_configs/$', views.show_configs, name='show_configs'),
    # url(r'^loan_config_detail/(?P<id>[0-9]+)/$', views.loan_config_detail, name='loan_config_detail'),
    # url(r'^delete/(\d+)/$', views.delete, name='delete'),
]