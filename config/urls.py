from django.urls import include, re_path
from django.conf.urls import handler404, handler500
from django.contrib import admin
from django.conf import settings
from config import views
from modules.dynadb import views as dyn_views


urlpatterns = [
    re_path(r'^contmaps/', include('modules.contact_maps.urls')),
#   re_path(r'^juanmaapp/', include('juanmaapp.urls')),  #### introducida por mi para  /var/www/protwis/sites/protwis/gpcrmd_srv/juanmaapp
#    re_path(r'^polls/', include('polls.urls')),
#    re_path(r'^tutorial/', include('tutorial.urls')),
    re_path(r'^dynadb/', include('modules.dynadb.urls')),
#    re_path(r'^juanmaapp/', include('juanmaapp.urls')), 
#    re_path(r'^pruebaapp/', include('pruebaapp.urls')), 
    re_path(r'^', include('modules.home.urls')),
    re_path(r'^accounts/', include('modules.accounts.urls')),
    re_path(r'^view/', include('modules.view.urls')),
    re_path(r'^gpcrome/', include('modules.crossreceptor_analysis.urls')),
#    re_path(r'^services/', include('api_' + settings.SITE_NAME + '.urls')),
#    re_path(r'^admin/', include(admin.site.urls)),
    re_path(r'^common/', include('modules.common.urls')),
#    re_path(r'^protein/', include('protein.urls')),
#    re_path(r'^family/', include('family.urls')),
#    re_path(r'^mutations/', include('mutation.urls')),
#    re_path(r'^news/', include('news.urls')),
#    re_path(r'^interaction/', include('interaction.urls')),
#    re_path(r'^residue/', include('residue.urls')),
#    re_path(r'^alignment/', include('alignment.urls')),
#    re_path(r'^similaritysearch/', include('similaritysearch.urls')),
#    re_path(r'^pages/', include('pages.urls')),
#    re_path(r'^phylogenetic_trees/', include('phylogenetic_trees.urls')),
#    re_path(r'^similaritymatrix/', include('similaritymatrix.urls')),
#    re_path(r'^structure/',include('structure.urls')),
#    re_path(r'^construct/',include('construct.urls')),
#    re_path(r'^sitesearch/',include('sitesearch.urls')),
#    re_path(r'^drugs/',include('drugs.urls')),
    re_path(r'^covid19/', include('modules.covid19.urls')),
    re_path(r'^sc2md/', include('modules.sc2md.urls')),
    re_path(r'^mdsrv/(?P<path>Precomputed/.*)$',dyn_views.mdsrv_redirect,name='mdsrv_redirect'),
    re_path(r'^corplots/', include('modules.corplots.urls')),
]

if not settings.FILES_NO_LOGIN:
    urlpatterns.append(re_path(r'^mdsrv/(?P<path_dir>dir/files/[^/\\]+/[^/\\]+)|mdsrv/(?P<path>.*/files/[^/\\]+/[^/\\]+/.*)$',
    dyn_views.mdsrv_redirect_prelogin,name='mdsrv_redirect_prelogin'))
urlpatterns += [ re_path(r'^mdsrv/(?P<path>.*)$', dyn_views.mdsrv_redirect,name='mdsrv_redirect'),
    re_path(r'^html/(?P<path>.*)$', dyn_views.mdsrv_redirect,name='mdsrv_redirect'),
]

handler404 = views.error404
handler500 = views.error500

if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append( re_path(r'^__debug__/', include(debug_toolbar.urls)) )
