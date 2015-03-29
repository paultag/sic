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


from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import View

from .models import License, Comment

import json


def api_response(data):
    return HttpResponse(json.dumps(data), content_type="application/json")


class HomepageView(View):
    template_name = 'sic/public/home.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


class AuthRequiredView(View):
    @classmethod
    def as_view(cls, *args, **kwargs):
        proxy = super(AuthRequiredView, cls).as_view(*args, **kwargs)
        proxy = login_required(proxy)
        return proxy


class NoCSRFView(View):
    @classmethod
    def as_view(cls, *args, **kwargs):
        proxy = super(NoCSRFView, cls).as_view(*args, **kwargs)
        proxy = csrf_exempt(proxy)
        return proxy


class LicenseListView(View):
    template_name = 'sic/public/licenses.html'

    def get(self, request, *args, **kwargs):
        l = License.objects.all()
        return render(request, self.template_name, {
            "licenses": l
        })


def comment_map(license):
    def markers(comments):
        for comment in comments:
            yield (comment.start_line, comment.start_column, "+")
            yield (comment.end_line, comment.end_column, "-")
    def ranges(license):
        line, col = (0, 0)
        stack = 0
        for l, c, op in sorted(list(markers(license.comments.all()))):
            if stack > 0:
                yield {"value": stack,
                       "start": {"line": line, "column": col},
                       "end": {"line": l, "column": c}}
            line, col = l, c
            stack += {"+": 1, "-": -1}[op]
        if stack != 0:
            raise ValueError("We didn't end on 0 D:")
    return list(ranges(license))


class LicenseView(NoCSRFView, AuthRequiredView):
    template_name = 'sic/public/license.html'

    def get(self, request, hash, *args, **kwargs):
        l = License.objects.get(hash=hash)

        r = request.META['HTTP_ACCEPT']
        if r == 'application/json':
            return api_response({
                "license": {
                    "hash": l.hash,
                },
                "comments": [x.to_dict() for x in l.comments.all()],
                "comment_map": comment_map(l),
            })

        return render(request, self.template_name, {
            "license": l
        })

    def post(self, request, hash):
        data = request.POST
        l = License.objects.get(hash=hash)
        c = Comment.objects.create(text=data['comment'],
                    license=l,
                    user=request.user,
                    start_line=data['start_line'],
                    end_line=data['end_line'],
                    start_column=data['start_ch'],
                    end_column=data['end_ch'])

        return api_response({
            "comment_id": c.id,
            "license_hash": l.hash,
            "user_id": c.user.username,
        })
