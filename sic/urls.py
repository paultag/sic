# sic - text feedback application
#
# Copyright (C) 2015  Paul R. Tagliamonte <tag@pault.ag>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views


urlpatterns = patterns('sic',
    url(r'^$', views.HomepageView.as_view(), name='sic_home'),
    url(r'^licenses/$', views.LicenseListView.as_view(), name='sic_licenses'),
    url(r'^license/(?P<hash>.*)/$', views.LicenseView.as_view(),
        name='sic_license'),
)
