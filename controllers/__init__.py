from controllers.users_controller import users
from controllers.subreddits_controller import subreddits
from controllers.threads_controller import threads
from controllers.web_users_controllers import web_users
from controllers.web_subreddits_controller import web_reddits
from controllers.web_threads_controller import web_threads

registrable_controllers = [
    users,
    subreddits,
    threads,
    web_users,
    web_reddits,
    web_threads,
]
