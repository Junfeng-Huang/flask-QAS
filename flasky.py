from app import create_app
from config import Config
import click

app = create_app()


@app.shell_context_processor
def make_shell_context():
    from app.models import db, User, Role, Question, Article, Answer
    return dict(db=db, User=User, Role=Role, Question=Question,
                Article=Article, Answer=Answer)


@app.context_processor
def inject_permissions():
    """
    为了方便在模板中访问，将其添加到模板上下文管理器
    """
    from app.models import db,Article,Answer, Like, Collection, QuestionFollow, Follow, User, Question
    from flask_login import current_user
    return dict(db=db,
                User=User,
                Question=Question,
                Like=Like,
                Collection=Collection,
                QuestionFollow=QuestionFollow,
                Follow=Follow,
                Answer=Answer,
                Article=Article,)


# @app.cli.command()
# @click.option('--length', default=25,
#               help='Number of functions to include in the profiler report.')
# @click.option('--profile-dir', default=None,
#               help='Directory where profiler data files are saved.')
# def profile(length, profile_dir):
#     """Start the application under the code profiler."""
#     from werkzeug.middleware.profiler import ProfilerMiddleware
#     app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],
#                                       profile_dir=profile_dir)
#     if __name__ == "__main__":
#         app.run(debug=False)
