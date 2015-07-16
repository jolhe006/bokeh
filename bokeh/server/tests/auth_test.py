#-----------------------------------------------------------------------------
# Copyright (c) 2012 - 2015, Continuum Analytics, Inc. All rights reserved.
#
# Powered by the Bokeh Development Team.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------
from __future__ import absolute_import

from contextlib import contextmanager

from nose.tools import assert_raises
from werkzeug.exceptions import Unauthorized

from ..app import bokeh_app
from ..models.user import User
from ..views.decorators import login_required

@contextmanager
def patch_current_user(func):
    old = bokeh_app.current_user
    try:
        bokeh_app.current_user = func
        yield
    finally:
        bokeh_app.current_user = old

def test_login_required():
    @login_required
    def test(x):
        return x
    with patch_current_user(lambda : None):
        assert_raises(Unauthorized, test)
    with patch_current_user(lambda : User):
        assert test(1) == 1
