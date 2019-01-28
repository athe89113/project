# coding: utf-8
from __future__ import unicode_literals
import logging
from django.utils.six import StringIO
from django.contrib.auth.models import User, Group, Permission
from django.core.management.base import BaseCommand
from django.core import management
from django.db import models, DatabaseError
from soc.models import Agent
from soc_user.models import UserInfo
from common import generate_google_url
# Secure random generators
import random

try:
    random = random.SystemRandom()
except ImportError:
    pass
try:
    from os import urandom
except ImportError:
    urandom = None

logger = logging.getLogger('soc')


class Command(BaseCommand):
    help = "Creates agent user"

    def handle(self, *args, **options):
        """
        Create agent user and userinfo
        """
        out = StringIO()
        management.call_command('createsuperuser', stdout=out)
        if "Superuser created successfully." not in out.getvalue():
            print("Failed to create superuser! please try again.")
            return

        user = User.objects.latest("date_joined")
        print("Please associate the just created user to an already existing agent:")
        try:
            agent_list = Agent.objects.values("id", "name")
            print("*" * 40)
            if agent_list:
                for al in agent_list:
                    print("agent id: %s" % str(al["id"]) + ", name: %s" % al["name"])
            else:
                print("No existing, please add agent manually before processing.")
                return
            print("*" * 40)

            agent_id = int(raw_input("Enter agent id: "))
            agent = Agent.objects.get(id=agent_id)
            gs_key, b32secret, url, optauth = generate_google_url(user.username)
            defaults = {
                "google_secret": gs_key,
                "role_type": 2,
                "is_admin": 1,
            }
            UserInfo.objects.get_or_create(user=user, agent=agent, defaults=defaults)
            print("Scan QR code: " + url)
            print("Or enter the secret key in your Google Authenticator app: " + b32secret)
            msg = "Create user profile for %s successfully." % user
            print(msg)
            logger.info(msg)
            print("Create User successfully!")
        except DatabaseError:
            msg = "Failed to create user profile for %s, perhaps migrations haven't run yet?" % user + \
                  " Please create again."
            logger.error(msg)
            print(msg)
            # Is it ok to delete superuser without userinfo? yes
            user.delete()
        except Agent.DoesNotExist:
            msg = "Failed to create user profile for %s, agent doesn't exist." % user + \
                  " Please add agent manually before creating again."
            logger.error(msg)
            print(msg)
            user.delete()
        except Exception as e:
            msg = u"Failed to create Agent User!! {} ".format(e)
            print(msg)
            logger.error(msg)
            user.delete()
