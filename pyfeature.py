# -*- coding: utf-8 -*-
"""
pyfeature
"""
__author__ = "xiechao"
__author_email__ = "xiechao06@gmail.com"
__version__ = "0.9.0"

import StringIO
from functools import partial, wraps
from contextlib import contextmanager
import re
import twill
import types
import sys

class Twill(object):
    """

    Twill wrapper utility class.

    Creates a Twill ``browser`` instance and handles
    WSGI intercept.
        
    Usage::

        t = Twill(self.app)
        with t:
            t.browser.go("/")
            t.url("/")

    """

    def __init__(self, app, host='127.0.0.1', port=5000, scheme='http'):
        self.app = app
        self.host = host
        self.port = port
        self.scheme = scheme

        self.browser = twill.get_browser()

    def go(self, *args, **kwargs):
        self.browser.go(*args, **kwargs)

    def __enter__(self):
        twill.set_output(StringIO.StringIO())
        twill.commands.clear_cookies()
        twill.add_wsgi_intercept(self.host,
                                 self.port,
                                 lambda: self.app)

        return self

    def __exit__(self, exc_type, exc_value, tb):
        twill.remove_wsgi_intercept(self.host, self.port)

        twill.commands.reset_output()

    def url(self, url):
        """
        Makes complete URL based on host, port and scheme
        Twill settings.

        :param url: relative URL
        """
        return "%s://%s:%d%s" % (self.scheme,
                                 self.host,
                                 self.port,
                                 url)

_feature = None

def step(desc):
    def decorator(f):
        def _f(*args, **kwargs):
            return f(*args, **kwargs)

        _feature.pattern2step[desc] = _f
        return _f

    return decorator

_before = {}

def before_(f, when):
    @wraps(f)
    def _f(feature):
        feature.print_("#initialize...")
        return f(feature)

    global _before
    _before.setdefault(when, []).append(_f)
    return _f

_after = {}

def after_(f, when):
    @wraps(f)
    def _f(feature):
        feature.print_("#finalize...")
        return f(feature)

    global _after
    _after.setdefault(when, []).append(_f)
    return _f

before_each_feature = partial(before_, when="each_feature")
after_each_feature = partial(after_, when="each_feature")
before_each_scenario = partial(before_, when="each_scenario")                 
after_each_scenario = partial(after_, when="each_scenario")          

class _Feature(object):
    def __init__(self, name, verbose):
        self.name = name
        self.__verbose = verbose
        self.pattern2step = {}

    def print_(self, s):
        if self.__verbose:
            print s

    def exec_step(self, step, desc, *args, **kwargs):
        self.print_(u"\t\t" + step.name + ": " + desc)
        self.print_(u"\t\t\t# * arguments:")
        for arg in args:
            self.print_(u"\t\t\t#   - %s" % repr(arg).decode("utf-8"))
        for k, v in kwargs.items():
            self.print_(u"\t\t\t#   - %s=%s" % (k, repr(v).decode("utf-8")))
        for pattern_, step_func in _feature.pattern2step.items():
            pattern_ = re.compile(pattern_)
            m = pattern_.match(desc)
            if m:
                args = m.groups() + args
                break
        else:
            raise (NotImplementedError(), u"no function map to " + desc)

        try:
            return step_func(step, *args, **kwargs)
        except:
            for after_hook in _after.get("each_scenario", []):
                after_hook(_feature.scenario)
            for after_hook in _after.get("each_feature", []):
                after_hook(_feature)
            raise

class _Scenario(object):
    def __init__(self, name):
        self.name = name


def given(desc, *args, **kwargs):
    return _feature.exec_step(_Step("Given", _feature, _feature.scenario),
                              desc, *args, **kwargs)


def and_(desc, *args, **kwargs):
    return _feature.exec_step(_Step("And", _feature, _feature.scenario),
                              desc, *args, **kwargs)


def when(desc, *args, **kwargs):
    return _feature.exec_step(_Step("when", _feature, _feature.scenario),
                              desc, *args, **kwargs)


def then(desc, *args, **kwargs):
    return _feature.exec_step(_Step("then", _feature, _feature.scenario),
                              desc, *args, **kwargs)


@contextmanager
def Feature(name, step_files=[], verbose=True, with_flask=False):
    if with_flask:
        flask_sqlalchemy_setup()
    global _feature
    _feature = _Feature(name, verbose)
    _feature.print_("\nFeature: " + name)
    try:
        for before_hook in _before["each_feature"]:
            before_hook(_feature)
    except KeyError:
        pass
    for step_file in step_files:
        __import__(step_file)
    yield

    for step_file in step_files:
        sys.modules.pop(step_file)
    try:
        for after_hook in _after["each_feature"]:
            after_hook(_feature)
    except KeyError:
        pass
    print "# Feature " + name + " passed"

@contextmanager
def Scenario(name):
    _feature.scenario = _Scenario(name)
    _feature.print_("\tScenario: " + name)
    global given, and_, when, then
    try:
        for before_hook in _before["each_scenario"]:
            before_hook(_feature.scenario)
    except KeyError:
        pass
    yield
    try:
        for after_hook in _after["each_scenario"]:
            after_hook(_feature.scenario)
    except KeyError:
        pass
    pass
    print "# Scenario " + name + " passed"

class _Step(object):
    def __init__(self, name, feature, senario):
        self.name = name
        self.feature = feature
        self.senario = senario

def flask_sqlalchemy_setup(app, db, create_step_prefix=u"create a "):
    import re
    import tempfile
    import os
    import mock

    
    # avoid remove db session after each Flask.test_request_context context
    patcher = mock.patch.dict(app.__dict__, 
                              {"teardown_appcontext_funcs": 
                               [f for f in app.teardown_appcontext_funcs if f.__module__ != "flask_sqlalchemy"]})

    @before_each_feature
    def setup(feature):
        db_fd, db_fname = tempfile.mkstemp()
        os.close(db_fd)
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_fname
        try:
            db.init_app(app)
        except AssertionError:  # flask-sqlalchemy forbid init_app more than once
            pass 
        db.create_all()
        feature.db = db
        feature.db_fname = db_fname

        _models_dict = {}
        for model in db.Model.__subclasses__():
            try:
                _models_dict[model.__label__] = model
            except AttributeError:
                _models_dict[model.__name__] = model

        @step(create_step_prefix+u"(\w+)(.*)")
        def _(step, model_name, desc, *args, **kwargs):
            try:
                __hinter__ = kwargs.pop("__hinter__")
            except KeyError:
                __hinter__ = "\s*\((?P<name>.+)\)"
            if __hinter__:
                m = re.match(__hinter__, desc)
                if m:
                    kwargs.update(m.groupdict())
            try:
                model = _models_dict[model_name] 
                ret = model(*args, **kwargs)
                db.session.add(ret)
                db.session.commit()
                return ret
            except KeyError, e:
                raise NotImplementedError()

        patcher.start()

    @after_each_feature
    def teardown(feature):
        feature.db.session.remove()
        os.unlink(feature.db_fname)
        patcher.stop()

def clear_hooks():
    global _before, _after # do this for py.test
    _before = {}
    _after = {}

if __name__ == "__main__":
    @before_each_feature
    def _(feature):
        print "create earth"

    @after_each_feature
    def _(feature):
        print "destroy earth"

    with Feature("God create earth"):
        @step(u'God said: "Let there be (.+)"')
        def _(step, name):
            return {"name": name}

        @step(u'there was (.+)')
        def _(step, name, sth):
            assert sth["name"] == name

        with Scenario("First day"):
              light = when(u'God said: "Let there be light"')
              then(u'there was light', light)
