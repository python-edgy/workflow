edgy.workflow
=============

Workflow is a simple library that allows you to manage lightweight workflows/state machines, and easily add this logic
to business objects you already use.

It supports both python 2 and 3, and does not assume you use any framework. In the future, we may include a light
adapter for the most popular frameworks, but the code should be very trivial.

By design choice, the library does not enforce the validity of objects. If you want to set an invalid state on an
object, you will be allowed to do so. That's a tradeoff that makes the library more flexible, at the price of less
data interity (in the plans: add a «strict» mode).

Kick-start
::::::::::


.. code-block:: python

    from edgy.workflow import Workflow, Transition, StatefulObject

    # Define transitions
    @Transition(source='new', target='accepted')
    def accept(self, subject):
        print('accepting {} using {}...'.format(subject, self))

    @Transition(source='new', target='refused')
    def refuse(self, subject):
        print('refusing {} using {}...'.format(subject, self))

    # Create a workflow object
    workflow = Workflow()
    workflow.add_transition(accept)
    workflow.add_transition(refuse)

    # Create a stateful object
    class Issue(StatefulObject):
        initial_state = 'new'
        workflow = workflow

    # Play with your newly workflow-enabled object.
    iss42 = Issue()
    iss42.accept()

    iss43 = Issue()
    iss43.refuse()

    iss44 = Issue(state='invalid')




Dive-in
:::::::

.. toctree::
   :maxdepth: 2

   transition
   workflow
   stateful



Indices and tables
::::::::::::::::::

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

