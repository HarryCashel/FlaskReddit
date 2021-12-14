from controllers.users_controller import users
from controllers.subreddits_controller import subreddits
from controllers.threads_controller import threads
from controllers.web_users_controllers import web_users


registrable_controllers = [
    users,
    subreddits,
    threads,
    web_users
]
