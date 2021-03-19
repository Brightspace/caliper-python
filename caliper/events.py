# -*- coding: utf-8 -*-
# Caliper-python package, events module
#
# This file is part of the IMS Caliper Analytics(tm) and is licensed to IMS
# Global Learning Consortium, Inc. (http://www.imsglobal.org) under one or more
# contributor license agreements. See the NOTICE file distributed with this
# work for additional information.
#
# IMS Caliper is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, version 3 of the License.
#
# IMS Caliper is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see http://www.gnu.org/licenses/.

from caliper.constants import CALIPER_ACTIONS, CALIPER_PROFILES
from caliper.constants import ENTITY_TYPES
from caliper.base import BaseEvent, ensure_type, ensure_types


# Base event class
class Event(BaseEvent):
    def __init__(
        self,
        id=None,
        context=None,
        profile=None,
        action=None,
        actor=None,
        edApp=None,
        object=None,
        eventTime=None,
        extensions=None,
        federatedSession=None,
        generated=None,
        group=None,
        membership=None,
        referrer=None,
        session=None,
        target=None,
    ):
        BaseEvent.__init__(
            self,
            context=context,
            id=id,
            profile=profile,
            action=action,
            eventTime=eventTime,
            object=object,
        )
        self._set_obj_prop("actor", actor, t=ENTITY_TYPES["AGENT"], req=True)
        self._set_obj_prop("edApp", edApp, t=ENTITY_TYPES["SOFTWARE_APPLICATION"])
        self._set_dict_prop("extensions", extensions)
        self._set_obj_prop(
            "federatedSession", federatedSession, t=ENTITY_TYPES["LTI_SESSION"]
        )
        self._set_obj_prop("generated", generated)
        self._set_obj_prop("group", group, t=ENTITY_TYPES["ORGANIZATION"])
        self._set_obj_prop("membership", membership, t=ENTITY_TYPES["MEMBERSHIP"])
        self._set_obj_prop("referrer", referrer)
        self._set_obj_prop("session", session, t=ENTITY_TYPES["SESSION"])
        self._set_obj_prop("target", target)

    def as_minimal_event(self):
        return MinimalEvent(
            id=self.id,
            action=self.action,
            actor=self.actor,
            object=self.object,
            eventTime=self.eventTime,
        )

    @property
    def actor(self):
        return self._get_prop("actor")

    @property
    def edApp(self):
        return self._get_prop("edApp")

    @property
    def extensions(self):
        return self._get_prop("extensions")

    @property
    def federatedSession(self):
        return self._get_prop("federatedSession")

    @property
    def generated(self):
        return self._get_prop("generated")

    @property
    def group(self):
        return self._get_prop("group")

    @property
    def membership(self):
        return self._get_prop("membership")

    @property
    def referrer(self):
        return self._get_prop("referrer")

    @property
    def session(self):
        return self._get_prop("session")

    @property
    def target(self):
        return self._get_prop("target")


class MinimalEvent(BaseEvent):
    def __init__(self, id=None, action=None, actor=None, object=None, eventTime=None):
        BaseEvent.__init__(
            self, id=id, action=action, object=object, eventTime=eventTime
        )
        self._set_obj_prop("actor", actor, t=ENTITY_TYPES["AGENT"], req=True)

    @property
    def actor(self):
        return self._get_prop("actor")


# Derived Events
class AnnotationEvent(Event):
    def __init__(self, **kwargs):
        Event.__init__(self, **kwargs)
        ensure_type(self.actor, ENTITY_TYPES["PERSON"])
        ensure_type(self.object, ENTITY_TYPES["DIGITAL_RESOURCE"])
        ensure_type(self.generated, ENTITY_TYPES["ANNOTATION"], optional=True)
        ensure_type(self.target, ENTITY_TYPES["FRAME"], optional=True)


class AssessmentEvent(Event):
    def __init__(self, target=None, **kwargs):
        Event.__init__(self, target=None, **kwargs)
        ensure_type(self.actor, ENTITY_TYPES["PERSON"])
        ensure_type(self.object, ENTITY_TYPES["ASSESSMENT"])
        ensure_type(self.generated, ENTITY_TYPES["ATTEMPT"], optional=True)


class AssessmentItemEvent(Event):
    def __init__(self, target=None, **kwargs):
        Event.__init__(self, target=None, **kwargs)
        ensure_type(self.actor, ENTITY_TYPES["PERSON"])
        ensure_type(self.object, ENTITY_TYPES["ASSESSMENT_ITEM"])
        ensure_type(self.referrer, ENTITY_TYPES["ASSESSMENT_ITEM"], optional=True)
        if self.action == CALIPER_ACTIONS["COMPLETED"]:
            ensure_type(self.generated, ENTITY_TYPES["RESPONSE"], optional=True)


class AssignableEvent(Event):
    def __init__(self, **kwargs):
        Event.__init__(self, **kwargs)
        ensure_type(self.actor, ENTITY_TYPES["PERSON"])
        ensure_type(self.object, ENTITY_TYPES["ASSIGNABLE_DIGITAL_RESOURCE"])
        ensure_type(self.generated, ENTITY_TYPES["ATTEMPT"], optional=True)
        ensure_type(self.target, ENTITY_TYPES["FRAME"], optional=True)


class FeedbackEvent(Event):
    def __init__(self, **kwargs):
        Event.__init__(self, **kwargs)
        ensure_type(self.actor, ENTITY_TYPES["PERSON"])
        ensure_type(self.object, ENTITY_TYPES["ENTITY"])
        ensure_type(self.target, ENTITY_TYPES["FRAME"], optional=True)
        if self.action == CALIPER_ACTIONS["RANKED"]:
            ensure_type(self.generated, ENTITY_TYPES["RATING"], optional=True)
        elif self.action == CALIPER_ACTIONS["COMMENTED"]:
            ensure_type(self.generated, ENTITY_TYPES["COMMENT"], optional=True)


class ForumEvent(Event):
    def __init__(self, **kwargs):
        Event.__init__(self, **kwargs)
        ensure_type(self.actor, ENTITY_TYPES["PERSON"])
        ensure_type(self.object, ENTITY_TYPES["FORUM"])


class GradeEvent(Event):
    def __init__(self, target=None, **kwargs):
        Event.__init__(self, target=None, **kwargs)
        ensure_type(self.object, ENTITY_TYPES["ATTEMPT"])
        ensure_type(self.generated, ENTITY_TYPES["SCORE"], optional=True)


class MediaEvent(Event):
    def __init__(self, **kwargs):
        Event.__init__(self, **kwargs)
        ensure_type(self.actor, ENTITY_TYPES["PERSON"])
        ensure_type(self.object, ENTITY_TYPES["MEDIA_OBJECT"])
        ensure_type(self.target, ENTITY_TYPES["MEDIA_LOCATION"], optional=True)


class MessageEvent(Event):
    def __init__(self, **kwargs):
        Event.__init__(self, **kwargs)
        ensure_type(self.actor, ENTITY_TYPES["PERSON"])
        ensure_type(self.object, ENTITY_TYPES["MESSAGE"])


class NavigationEvent(Event):
    def __init__(self, **kwargs):
        Event.__init__(self, **kwargs)
        ensure_type(self.actor, ENTITY_TYPES["PERSON"])
        ensure_types(
            self.referrer,
            [ENTITY_TYPES["DIGITAL_RESOURCE"], ENTITY_TYPES["SOFTWARE_APPLICATION"]],
            optional=True,
        )
        if self.profile == CALIPER_PROFILES["SURVEY"]:
            ensure_types(
                self.object,
                [ENTITY_TYPES["QUESTIONNAIRE"], ENTITY_TYPES["QUESTIONNAIRE_ITEM"]],
            )

        else:
            ensure_types(
                self.object,
                [
                    ENTITY_TYPES["DIGITAL_RESOURCE"],
                    ENTITY_TYPES["SOFTWARE_APPLICATION"],
                ],
                optional=True,
            )
            ensure_type(self.target, ENTITY_TYPES["DIGITAL_RESOURCE"], optional=True)


class QuestionnaireEvent(Event):
    def __init__(self, **kwargs):
        Event.__init__(self, **kwargs)
        ensure_type(self.actor, ENTITY_TYPES["PERSON"])
        ensure_type(self.object, ENTITY_TYPES["QUESTIONNAIRE"])


class QuestionnaireItemEvent(Event):
    def __init__(self, **kwargs):
        Event.__init__(self, **kwargs)
        ensure_type(self.actor, ENTITY_TYPES["PERSON"])
        ensure_type(self.object, ENTITY_TYPES["QUESTIONNAIRE_ITEM"])
        ensure_type(self.generated, ENTITY_TYPES["RESPONSE"], optional=True)


class ResourceManagementEvent(Event):
    def __init__(self, **kwargs):
        Event.__init__(self, **kwargs)
        ensure_type(self.actor, ENTITY_TYPES["PERSON"])
        ensure_type(self.object, ENTITY_TYPES["DIGITAL_RESOURCE"])
        if self.action == CALIPER_ACTIONS["COPIED"]:
            ensure_type(self.generated, ENTITY_TYPES["DIGITAL_RESOURCE"])
        else:
            ensure_type(self.generated, ENTITY_TYPES["DIGITAL_RESOURCE"], optional=True)


class SearchEvent(Event):
    def __init__(self, **kwargs):
        Event.__init__(self, **kwargs)
        ensure_type(self.actor, ENTITY_TYPES["PERSON"])
        ensure_type(self.object, ENTITY_TYPES["ENTITY"])
        ensure_type(self.generated, ENTITY_TYPES["SEARCH_RESPONSE"], optional=True)


class SessionEvent(Event):
    def __init__(self, **kwargs):
        Event.__init__(self, **kwargs)
        if self.action == CALIPER_ACTIONS["LOGGED_IN"]:
            ensure_type(self.actor, ENTITY_TYPES["PERSON"])
            ensure_type(self.object, ENTITY_TYPES["SOFTWARE_APPLICATION"])
            ensure_type(self.generated, ENTITY_TYPES["SESSION"], optional=True)
            ensure_type(self.target, ENTITY_TYPES["DIGITAL_RESOURCE"], optional=True)
        elif self.action == CALIPER_ACTIONS["LOGGED_OUT"]:
            ensure_type(self.actor, ENTITY_TYPES["PERSON"])
            ensure_type(self.object, ENTITY_TYPES["SOFTWARE_APPLICATION"])
            ensure_type(self.target, ENTITY_TYPES["SESSION"], optional=True)
        elif self.action == CALIPER_ACTIONS["TIMED_OUT"]:
            ensure_type(self.actor, ENTITY_TYPES["SOFTWARE_APPLICATION"])
            ensure_type(self.object, ENTITY_TYPES["SESSION"])
        ensure_types(
            self.referrer,
            [ENTITY_TYPES["DIGITAL_RESOURCE"], ENTITY_TYPES["SOFTWARE_APPLICATION"]],
            optional=True,
        )


class SurveyEvent(Event):
    def __init__(self, **kwargs):
        Event.__init__(self, **kwargs)
        ensure_type(self.actor, ENTITY_TYPES["PERSON"])
        ensure_type(self.object, ENTITY_TYPES["SURVEY"])


class SurveyInvitationEvent(Event):
    def __init__(self, **kwargs):
        Event.__init__(self, **kwargs)
        ensure_type(self.actor, ENTITY_TYPES["PERSON"])
        ensure_type(self.object, ENTITY_TYPES["SURVEY_INVITATION"])


class ThreadEvent(Event):
    def __init__(self, **kwargs):
        Event.__init__(self, **kwargs)
        ensure_type(self.actor, ENTITY_TYPES["PERSON"])
        ensure_type(self.object, ENTITY_TYPES["THREAD"])


class ToolLaunchEvent(Event):
    def __init__(self, **kwargs):
        Event.__init__(self, **kwargs)
        ensure_type(self.actor, ENTITY_TYPES["PERSON"])
        ensure_type(self.object, ENTITY_TYPES["SOFTWARE_APPLICATION"])
        ensure_type(self.generated, ENTITY_TYPES["DIGITAL_RESOURCE"], optional=True)
        ensure_types(
            self.target, [ENTITY_TYPES["LINK"], ENTITY_TYPES["LTI_LINK"]], optional=True
        )
        if self.action == CALIPER_ACTIONS["LAUNCHED"]:
            ensure_type(self.federatedSession, ENTITY_TYPES["LTI_SESSION"])


class ToolUseEvent(Event):
    def __init__(self, **kwargs):
        Event.__init__(self, **kwargs)
        ensure_type(self.actor, ENTITY_TYPES["PERSON"])
        ensure_type(self.object, ENTITY_TYPES["SOFTWARE_APPLICATION"])
        ensure_type(self.target, ENTITY_TYPES["SOFTWARE_APPLICATION"], optional=True)
        ensure_type(
            self.generated, ENTITY_TYPES["AGGREGATE_MEASURE_COLLECTION"], optional=True
        )


class ViewEvent(Event):
    def __init__(self, **kwargs):
        Event.__init__(self, **kwargs)
        ensure_type(self.actor, ENTITY_TYPES["PERSON"])
        if self.profile == CALIPER_PROFILES["SURVEY"]:
            ensure_types(
                self.object,
                [ENTITY_TYPES["QUESTIONNAIRE"], ENTITY_TYPES["QUESTIONNAIRE_ITEM"]],
            )
        else:
            ensure_type(self.object, ENTITY_TYPES["DIGITAL_RESOURCE"])
