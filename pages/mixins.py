
class DecoratorChainingMixin(object):
    def dispatch(self, *args, **kwargs):
        decorators = getattr(self, 'decorators', [])
        base = super(DecoratorChainingMixin, self).dispatch

        for decorator in decorators:
            base = decorator(base)
        return base(*args, **kwargs)