# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.QUEUE.
#
# SENAITE.QUEUE is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright 2018-2019 by it's authors.
# Some rights reserved, see README and LICENSE.

import logging

from Products.Archetypes.atapi import listTypes
from Products.Archetypes.atapi import process_types
from Products.CMFCore.permissions import AddPortalContent
from Products.CMFCore.utils import ContentInit
from senaite.queue.config import CHUNK_SIZES
from senaite.queue.interfaces import IQueueDispatcher
from zope.i18nmessageid import MessageFactory
from zope.component._api import queryUtility


PRODUCT_NAME = "senaite.queue"
PROFILE_ID = "profile-{}:default".format(PRODUCT_NAME)

# Defining a Message Factory for when this product is internationalized.
messageFactory = MessageFactory(PRODUCT_NAME)

logger = logging.getLogger(PRODUCT_NAME)


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
    logger.info("*** Initializing SENAITE QUEUE Customization package ***")

    types = listTypes(PRODUCT_NAME)
    content_types, constructors, ftis = process_types(types, PRODUCT_NAME)

    # Register each type with it's own Add permission
    # use ADD_CONTENT_PERMISSION as default
    allTypes = zip(content_types, constructors)
    for atype, constructor in allTypes:
        kind = "%s: Add %s" % (PRODUCT_NAME, atype.portal_type)
        ContentInit(kind,
                    content_types=(atype,),
                    permission=AddPortalContent,
                    extra_constructors=(constructor, ),
                    fti=ftis,
                    ).initialize(context)


# TODO Move the stuff below outside from senaite.queue.__init__

def is_queue_enabled():
    """Returns whether the queue is active for current instance or not.
    """
    return get_queue_utility() is not None


def get_queue_utility():
    """
    Returns the queue utility
    """
    return queryUtility(IQueueDispatcher)


def get_chunk_size(task_name):
    """Returns the default chunk size for a given task
    """
    if task_name in CHUNK_SIZES:
        return CHUNK_SIZES[task_name]
    return CHUNK_SIZES["default"]


def get_action_task_name(action):
    return "task_action_{}".format(action)
