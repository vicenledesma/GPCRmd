from django.conf.urls import url,patterns,include
from django.conf import settings
from . import views

app_name = "view"

urlpatterns = [
    url(r'^(?P<dyn_id>[0-9]+)/$', views.index, name='index'),
  #  url(r'^distances/(?P<dist_str>[0-9]+-[0-9]+(a[0-9]+-[0-9]+)*)/(?P<struc_id>[0-9]+)/(?P<traj_id>[0-9]+)$', views.distances, name='distances'),
  #  url(r'^rmsd/$', views.rmsd, name='rmsd'),
    url(r'^dwl/(?P<dist_id>dist_[0-9]+)/$', views.download_dist, name="download_dist"),
    url(r'^dwl/(?P<rmsd_id>rmsd_[0-9]+)/$', views.download_rmsd, name="download_rmsd"),
    url(r'^dwl/(?P<int_id>int_[0-9]+)/$', views.download_int, name="download_int"),
    url(r'^docs/$', views.viewer_docs, name='viewer_docs'),
    url(r'^hbonds/$', views.hbonds, name='hbonds'),
    url(r'^saltbridges/$', views.saltbridges, name='saltbridges'),
    url(r'^grid/$', views.sasa, name='sasa'),
#    url(r'^fplot/(?P<dyn_id>[0-9]+)/(?P<filename>\w+\.json)/(?P<seg_li>(|\d+(:[A-Z])?|\d+(:[A-Z])?\-\d+(:[A-Z])?),((|\d+(:[A-Z])?|\d+(:[A-Z])?\-\d+(:[A-Z])?),){13}(|\d+(:[A-Z])?|\d+(:[A-Z])?\-\d+(:[A-Z])?))/$', views.fplot_gpcr, name='fplot_gpcr'),
    url(r'^fplot2/(?P<dyn_id>[0-9]+)/(?P<filename>\w+\.json)/(?P<seg_li>(|\d+(:[A-Z])?|\d+(:[A-Z])?\-\d+(:[A-Z])?),((|\d+(:[A-Z])?|\d+(:[A-Z])?\-\d+(:[A-Z])?),){13}(|\d+(:[A-Z])?|\d+(:[A-Z])?\-\d+(:[A-Z])?))/$', views.fplot_gpcr_slide, name='fplot_gpcr_slide'),
   url(r'^fplot_test/(?P<dyn_id>[0-9]+)/(?P<filename>\w+\.json)/$', views.fplot_test, name='fplot_test'),
    url(r'^ref/(?P<dyn_id>[0-9]+)/$', views.view_reference, name='reference'),
    url(r'^session/(?P<session_name>\w*)/$', views.view_session, name='view_session'),
]

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^files/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
)
