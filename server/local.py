from flask import make_response, render_template, session


def response(**kwargs):
    return make_response(render_template('index.html', **kwargs, current_category=session['current_category']))


def use_session_in_kwargs(func):
    def session_wrapper(*args, **kwargs):
        kwargs['category'] = session.get('current_category')
        return func(*args, **kwargs)
    return session_wrapper
