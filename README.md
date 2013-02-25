pyfeature
=========

Inspired by lettuce, but be pythonic!

pyfeature let you:

 * write specifications/acceptance auto test in python
 * one step file for one feature (of course, you could reuse the step files at will).
 * some utilities to help you write acceptance auto test more easily. For example, set up create steps from models automatically!

## Tutorial

### install it

```
$ python setup.py install
$ pip install flask # you needn't to install it to use pyfeature, except when running sample
$ pip install flask-sqlalchemy # you needn't to install it to use pyfeature, except when running sample
$ pip install mock # you needn't to install it to use pyfeature, except when running sample
```

### Write your first feature file

```
# -*- coding: utf-8 -*-
"""
sample_feature.py
"""
from pyfeature import (Feature, Scenario, given, and_, when, then)
from basemain import app
from database import db
from models import Boy, Beauty

# I want use pytest
def test():
    from pyfeature import flask_sqlalchemy_setup
    flask_sqlalchemy_setup(app, db)
    with Feature(u"test handsome boy", step_files=["sample_steps"]):
        with Scenario(u"run after beauty"):
            handsome_boy = given(u"create a Boy (Han Solo)", handsome=True)
            ugly_boy = and_(u"create a Boy (Darth Vader)", handsome=False)
            beauty = and_(u"create a Beauty named Princess Leia Organa",
__hinter__=u"\s*named (?P<name>.+)")
            result = when(u"handsome boy runs after beauty", handsome_boy,
beauty)
            then(u"got it!", result)
            result = when(u"ugly boy runs after beauty", ugly_boy,
beauty)
            then(u"fail!", result)

if __name__ == "__main__":
    test() # it could be invoked using python either

```

### implement skeleton of your step file:

```
# -*- coding: utf-8 -*-
"""
sample_steps.py
"""

from pyfeature import step

# you needn't to implement create steps, they are builtin

@step(u"(.*)runs after beauty")
def _(step_ctx, sth_irrelative, boy, beauty):
    return boy.handsome

@step(u"got it!")
def _(step_ctx, result):
    assert result

@step(u"fail!")
def _(step_ctx, result):
    assert not result
```


### try running it!

```
$ python sample_feature.py
```

the output is:

```
Feature: test handsome boy
#initialize...
    Scenario: run after beauty
		Given: create a Boy (Han Solo)
			# * arguments:
			#   - handsome=True
		And: create a Boy (Darth Vader)
			# * arguments:
			#   - handsome=False
		And: create a Beauty named Princess Leia Organa
			# * arguments:
			#   - __hinter__=u'\\s*named (?P<name>.+)'
		when: handsome boy runs after beauty
			# * arguments:
			#   - <models.Boy object at 0x20d6910>
			#   - <models.Beauty object at 0x20dbc50>
		then: got it!
			# * arguments:
			#   - True
		when: ugly boy runs after beauty
			# * arguments:
			#   - <models.Boy object at 0x20db650>
			#   - <models.Beauty object at 0x20dbc50>
		then: fail!
			# * arguments:
			#   - False
# Scenario run after beauty passed
#finalize...
# Feature test handsome boy passed

```

### implement your step file

...

ENJOY IT!




