from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.views import login, logout
from django.urls import reverse
from django.views.generic.base import RedirectView
from django.views.static import serve

from annotator.views import *

admin.site.site_header = 'eva'

urlpatterns = [
    url(r'^$', permission_required('view_home', login_url='/login/')(home)),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/img/icon.png')),
    url(r'^projects/$', permission_required('view_home', login_url='/login/')(projects), name='define_projects'),
    url(r'^video/(\d+)/(\d+)/$', permission_required('view_home', login_url='/login/')(VideoView.as_view()), name='video'),
    url(r'^annotation/(\d+)/$', permission_required('view_home', login_url='/login/')(AnnotationView.as_view())),
    url(r'^login/$', login,
        {'template_name': 'admin/login.html',
         'extra_context': {'site_header': 'BeaverDam Login'}
         }, name='login'),
    url(r'^logout/$', logout),
    url(r'^accounts/', permission_required('view_home', login_url='/login/')(RedirectView.as_view(url='/'))),
    url(r'^admin/', admin.site.urls),
    url(r'^upload/(?P<name>.*)/done/$', permission_required('view_home', login_url='/login/')(UploadVideoDone.as_view()), name='upload_video_done'),
    url(r'^upload/(?P<name>.*)/$', permission_required('view_home', login_url='/login/')(UploadVideos.as_view()), name='upload_videos'),
    url(r'^create_video/(?P<name>.*)/$', permission_required('view_home', login_url='/login/')(CreateVideo.as_view()), name='create_video'),
    url(r'^tracker/(\d+)/$', permission_required('view_home', login_url='/login/')(tracker), name='tracker'),
    url(r'^tracker/get_results/$', permission_required('view_home', login_url='/login/')(tracker_get_results), name='tracker_get_results'),
    url(r'^check_video_name/(?P<name>.*)/$', permission_required('view_home', login_url='/login/')(check_video_name)),
    url(r'^export/dataset/(?P<name>.*)/$', permission_required('view_home', login_url='/login/')(ExportDataset.as_view()), name='export_dataset'),
    url(r'^export/labels/(?P<name>.*)/$', permission_required('view_home', login_url='/login/')(ExportLabels.as_view()), name='export_labels'),
    url(r'^export/video/(?P<vid>\d+)/$', permission_required('view_home', login_url='/login/')(ExportVideo.as_view()), name='export_video'),
    url(r'^export/video/status/$', permission_required('view_home', login_url='/login/')(ExportVideoStatus.as_view())),
    url(r'^labels/labels/$', permission_required('view_home', login_url='/login/')(LabelsView.as_view()), name='labels'),
    url(r'^labels/project/$', permission_required('view_home', login_url='/login/')(ProjectView.as_view()), name='project'),
    url(r'^labels/label_select/$', permission_required('view_home', login_url='/login/')(LabelSelect.as_view()), name='label_select'),
    url(r'^labels/project_select/$', permission_required('view_home', login_url='/login/')(ProjectSelect.as_view()), name='project_select'),
    url(r'^labels/$', permission_required('view_home', login_url='/login/')(labels), name='labels'),
    url(r'^videos/$', permission_required('view_home', login_url='/login/')(Videos.as_view()), name='videos'),
    url(r'^video/status/(\d+)/$', permission_required('view_home', login_url='/login/')(VideoStatus.as_view()))
]

# Add media folder
urlpatterns.append(url(
    r'^media/(?P<path>.*)$',
    serve,
    {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}
))

# Add static when debug is off
if not settings.DEBUG:
    urlpatterns.append(url(
        r'^static/(?P<path>.*)$',
        serve,
        {'document_root': settings.STATIC_ROOT, 'show_indexes': True}
    ))
