# Secret settings for Gondor
import os 

os.environ['ADMINS_SSOUK'] = "('Name Surname', 'yourname@example.com')"
os.environ['SECRET_KEY'] ="id_fbqde55y5oev3ao(h^myql*%w*bb%o+hvxd0_t2c5%z550s"

# Email
# run "python -m smtpd -n -c DebuggingServer localhost:1025" to see outgoing
# messages dumped to the terminal

os.environ['EMAIL_HOST']="localhost"
os.environ['EMAIL_PORT']="1025"
os.environ['EMAIL_HOST_USER']=""
os.environ['EMAIL_HOST_PASSWORD']=""
os.environ['SENTRY_DSN'] = ""
