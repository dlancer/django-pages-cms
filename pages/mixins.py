"""Implements decorator chaining mixin for class based view"""

from django.contrib import messages


class DecoratorChainingMixin(object):
    def dispatch(self, *args, **kwargs):
        decorators = getattr(self, 'decorators', [])
        base = super(DecoratorChainingMixin, self).dispatch

        for decorator in decorators:
            base = decorator(base)
        return base(*args, **kwargs)


class FormMessageMixin(object):
    """Make it easy to display notification messages when using Class Based Views"""

    def delete(self, request, *args, **kwargs):
        message = None
        if hasattr(self, 'form_delete_message'):
            message = self.form_delete_message
        elif hasattr(self, 'form_valid_message'):
            message = self.form_valid_message
        if message is not None:
            messages.success(self.request, message)
        return super(FormMessageMixin, self).delete(request, *args, **kwargs)

    def form_valid(self, form):
        message = self.form_valid_message if hasattr(self, 'form_valid_message') else None
        if message is not None:
            messages.success(self.request, message)
        return super(FormMessageMixin, self).form_valid(form)

    def form_invalid(self, form):
        message = self.form_invalid_message if hasattr(self, 'form_invalid_message') else None
        if message is not None:
            messages.success(self.request, message)
        return super(FormMessageMixin, self).form_invalid(form)
