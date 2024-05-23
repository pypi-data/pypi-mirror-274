import os
import onetick.query as otq

dir_home = "/home/ubuntu/onetick-onboarding/onetick"
current_dir = "/home/ubuntu/projects/onetick_latency"

try:
    from auth import username_authentication, password_authentication
except ImportError:
    raise ImportError("Please create an auth.py file with your username and password. "
                      "Refer to auth_example.py for an example.")

env = os.environ[
    "ONE_TICK_CONFIG"
] = f"{dir_home}/client_data/config/one_tick_config.txt"  # point to OneTick main config file on your local machine

onetick_lib = otq.OneTickLib(
    None
)  # activate OneTick Python API. onetick_lib should be a singleton object, i.e. only one instance should be instantiated in your python application

username_authentication = onetick_lib.set_username_for_authentication(username_authentication)  # set only if a username is required by your OneTick tickserver for authentication
password = onetick_lib.set_password(password_authentication)
