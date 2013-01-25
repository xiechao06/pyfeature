pyfeature
=========

Inspired by lettuce, but be pythonic!

pyfeature let you:

 * write specifications/acceptance auto test in python
 * one step file for one feature (of course, you could reuse the step files at will).
 * some utilities to help you write acceptance auto test more easily.

## Tutorial

### install it

```
$ python setup.py install
```

### Write your first feature file

```
# -*- coding: utf-8 -*-

# sample_feature.py

from pyfeature import Feature, Scenario
# here we assume that both Person and Beauty are pre-built sqlalchemy models
from models import Person, Beauty

# I want use pytest

def test():
    with Feature(u"test handsome boy", models=[Person, Beauty]):
        with Scenario(u"run after beauty"):
            handsome_boy = given(u"create a handsome Person (Han Solo)", handsome=True)
            ugly_boy = and_(u"create an ugly Person (Darth Vader)", handsome=False) 
            beauty = and_(u"create a Beauty named Princess Leia Organa", __hinter__=u"named (?P<name>.+)")
            result = when(u"handsome boy runs after beauty", handsome_boy, beauty)
            then_(u"got it!", result)
            result = when(u"ugly boy runs after beauty", ugly_boy, beauty)
            then_(u"fail!", result)

if __name__ == "__main__":
    test() # it could be invoked using python either
```

### read it

```
$ cat sample_feature.py | pyfeautre_reader.py
```

the output is:

```
Feature: test handsome boy
# initialize Feature

    Scenario: run after beauty
        Given: create a handsome Person (Han Solo)
        And: create an ugly Person (Darth Vader)
        And: create a Beauty named Princess Leia Organa
        When: handsome boy runs after beauty
        Then: got it!
        When: ugly boy runs after beauty
        Then: fail!
```

### generate the step file

```
$ cat sample_feature.py | pyfeature_step_gen.py > sample_steps.py
```

you got a step file like:

```
# -*- coding: utf-8 -*-

from pyfeature import step

# this step has been set up by pyfeature
@step(u"create a handsom Person (Han Solo)")
def _(step_ctx):
    pass
    
# this step has been set up by pyfeature
@step(u"create a handsom Person (Darth Vader)")
def _(step_ctx):
    pass

# this step has been set up by pyfeature
@step(u"create a Beauty named Princess Leia Organa")
def _(step_ctx):
    pass

@step(u"handsome body runs after beauty")
def _(step_ctx, handsome_boy, beauty):
    pass

@step(u"ugly body runs after beauty")
def _(step_ctx, handsome_boy, beauty):
    pass

@step(u"got it!")
def _(step_ctx, result):
    pass
    
@step(u"fail!")
def _(step_ctx, result):
    pass
```

### refine your step file:

```
# -*- coding: utf-8 -*-

# sample_steps.py

@step(u"(.*)runs after beauty")
def _(step_ctx, sth_irrelative, boy, beauty):
    pass

@step(u"got it!")
def _(step_ctx, result):
    pass

@step(u"fail!")
def _(step_ctx, result):
    pass

```

### relate you step files with Feature

```
# -*- coding: utf-8 -*-

# sample_feature.py

from pyfeature import Feature, Scenario
# here we assume that both Person and Beauty are pre-built sqlalchemy models
from models import Person, Beauty

# I wan't use pytest

def test():
    with Feature(u"test handsome boy", models=[Person, Beauty], step_files="sample_steps.py"):
        with Scenario(u"run after beauty"):
            handsome_boy = given(u"create a handsome Person (Han Solo)", handsome=True)
            ugly_boy = and_(u"create an ugly Person (Darth Vader)", handsome=False) 
            beauty = and_(u"create a Beauty named Princess Leia Organa", __hinter__=u"named (?P<name>.+)")
            result = when(u"handsome boy runs after beauty", handsome_boy, beauty)
            then_(u"got it!", result)
            result = when(u"ugly boy runs after beauty", ugly_boy, beauty)
            then_(u"fail!", result)

if __name__ == "__main__":
    test() # it could be invoked using python either
```

### try running it!

```
$ python sample_feature.py
```

the output is:

```

Feature: test handsome boy
# initialize Feature

    Scenario: run after beauty
        Given: create a handsome Person (Han Solo)
        And: create an ugly Person (Darth Vader)
        And: create a Beauty named Princess Leia Organa
        When: handsome boy runs after beauty
        Then: got it!
        When: ugly boy runs after beauty
        Then: fail!
        
# finalize Feature
# result is OK
```

### implement your step file

...




