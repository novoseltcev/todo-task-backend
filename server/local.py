from flask import make_response, render_template, session, send_from_directory
from os import path, getcwd


def response(**kwargs):
    return send_from_directory(path.join(getcwd(), 'server', 'static', 'templates'), 'new_index.html'), {'data': 1}
    # return make_response(render_template('new_index.html', **kwargs, current_category=session['current_category']))


def use_session_in_kwargs(func):
    def session_wrapper(*args, **kwargs):
        kwargs['category'] = session.get('current_category')
        return func(*args, **kwargs)
    return session_wrapper

# < td style = "padding-left: 30px;" > {{tassk.title}} < / td >
