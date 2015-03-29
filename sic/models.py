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

import hashlib

from django.db import models
from django.contrib.auth.models import User


class License(models.Model):
    """
    License model

    This covers an iteration of a license -- something like the second
    draft of the brand new AGPLv4 license.

    The hash is defined as the SHA1 hash of the text attribute.
    """
    text = models.TextField()
    name = models.CharField(max_length=128)
    hash = models.CharField(unique=True, max_length=128, primary_key=True)
    under_discussion = models.BooleanField(default=False)

    def _set_hash(self):
        sha = hashlib.sha1()
        sha.update(self.text.encode())
        self.hash = sha.hexdigest()

    def save(self, *args, **kw):
        """
        Save this object back to the database
        """
        self._set_hash()
        return super(License, self).save(*args, **kw)


COMMENT_CLASSIFICATIONS = (
    ('p', 'Positive'),
    ('n', 'Negative'),
    ('q', 'Question'),
    ('u', 'Neutral'),
)


class Comment(models.Model):
    """
    Feedback from a contributor against a License. This comment
    is targeted at a range in the text, and can express feelings
    about that section.
    """

    user = models.ForeignKey(User, related_name='comments')
    license = models.ForeignKey('License', related_name='comments')
    text = models.TextField()
    classification = models.CharField(max_length=1,
                                      choices=COMMENT_CLASSIFICATIONS)

    start_line = models.PositiveIntegerField()
    end_line = models.PositiveIntegerField()
    start_column = models.PositiveIntegerField()
    end_column = models.PositiveIntegerField()

    def to_dict(self):
        return {
            "user": self.user.username,
            "license": self.license.hash,
            "text": self.text,
            "classification": self.classification,
            "range": {
                "start": {
                    "line": self.start_line,
                    "column": self.start_column,
                },
                "end": {
                    "line": self.end_line,
                    "column": self.end_column,
                },
            }
        }
