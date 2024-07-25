from flask import current_app, _app_ctx_stack
from posthog import Posthog

class PostHogExtension:
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('POSTHOG_KEY', None)
        app.config.setdefault('POSTHOG_URL', None)
        app.teardown_appcontext(self.teardown)

    def teardown(self, exception):
        ctx = _app_ctx_stack.top
        if hasattr(ctx, 'posthog'):
            ctx.posthog = None

    @property
    def posthog(self):
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'posthog'):
                ctx.posthog = Posthog(
                    project_api_key=current_app.config['POSTHOG_KEY'],
                    host=current_app.config['POSTHOG_URL']
                )
            return ctx.posthog
