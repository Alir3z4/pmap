PMap
====

.. image:: https://travis-ci.org/Alir3z4/pmap.svg?branch=master
    :target: https://travis-ci.org/Alir3z4/pmap
.. image:: https://codecov.io/gh/Alir3z4/pmap/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/Alir3z4/pmap


Installation
------------

Manual installation
~~~~~~~~~~~~~~~~~~~

Make a new virtualenv for the project, and run::

    pip install -r requirements/dev.txt
    python manage.py migrate
    python manage.py runserver


Continuous Integration
-----------------------

PMap uses multiple CI to preform:

* Running Tests Suite.
* Running Code Quality Standards.

In case of failure of any the validations checks above, the build will fail
and no deployment will happen.

Our pull request & code review flow is also heavily depends on those factors.

Before pushing your code for review, be sure to run the following commands
to perform those validations against your local code changes.

::

  fab test cq


Branching
=========

Features: Any new work should be branched out from "master" branch and must
be merged back into the "master" branch.

Hot fixes: Fixes should be branched out from "production" branch and must be
merged back into "master" and "production".


Branches
--------

Branch **production**, should be last and stable working code that is on
Production servers. All the pull requests (from Master branch) should
pass the code checks, including and not limited to:

* Test Coverage
* Unit Tess Status
* Build Status
* Reviewers Approval

Branch **master**, should contains the latest development work and should
be on staging. All the pull requests (from developers) should pass the code
checks, including and not limited to:

* Test Coverage
* Unit Tess Status
* Build Status
* Reviewers Approval


Deployment
----------

Deployment happens automatically via the CI.

Latest code on **master** branch will be deployed to the staging, while
branch **production** will be deployed to production server.


Release
-------

To release a new version or have the latest changes on the production:

* Make a new Pull Request from branch **master** to **production**.
* The pull request should pass (not limited to):
    * Test Coverage
    * Unit Tess Status
    * Build Status
    * Reviewers Approval

After merging the pull request into **production**, the CI will build and
deploy the latest code from production branch to the Production server.
