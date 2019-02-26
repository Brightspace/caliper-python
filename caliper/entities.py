# -*- coding: utf-8 -*-
# Caliper-python package, entities module
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
#
from __future__ import (absolute_import, division, print_function, unicode_literals)
from future.standard_library import install_aliases
install_aliases()
from future.utils import raise_with_traceback
from builtins import *

try:
    from collections.abc import MutableSequence, MutableMapping
except ImportError:
    from collections import MutableSequence, MutableMapping

from caliper.constants import ENTITY_TYPES, MARKER_TYPES
from caliper.constants import CALIPER_LTI_MESSAGES, CALIPER_METRICS, CALIPER_ROLES, CALIPER_STATUS
from caliper.base import CaliperSerializable, BaseEntity
from caliper.base import ensure_type, ensure_list_type


### Fundamental entities ###
## Base entity class
class Entity(BaseEntity):

    ## Use the base context value here, but preserve the context labels
    ## in case, in the future, indivdual contexts start getting split out

    def __init__(self,
                 id=None,
                 context=None,
                 profile=None,
                 dateCreated=None,
                 dateModified=None,
                 description=None,
                 name=None,
                 version=None,
                 extensions=None):
        BaseEntity.__init__(self, context=context, profile=profile)
        self._set_id(id)
        self._set_date_prop('dateCreated', dateCreated)
        self._set_date_prop('dateModified', dateModified)
        self._set_str_prop('description', description)
        self._set_str_prop('name', name)
        self._set_obj_prop('extensions', extensions)

    @property
    def id(self):
        return self._get_prop('id')

    @property
    def dateCreated(self):
        return self._get_prop('dateCreated')

    @property
    def dateModified(self):
        return self._get_prop('dateModified')

    @property
    def description(self):
        return self._get_prop('description')

    @property
    def name(self):
        return self._get_prop('name')

    @property
    def extensions(self):
        return self._get_prop('extensions')


## Behavioural interfaces for entities ##
class Assignable(BaseEntity):
    @property
    def datePublished(self):
        return self._get_prop('datePublished')

    @property
    def dateToActivate(self):
        return self._get_prop('dateToActivate')

    @property
    def dateToShow(self):
        return self._get_prop('dateToShow')

    @property
    def dateToStartOn(self):
        return self._get_prop('dateToStartOn')

    @property
    def dateToSubmit(self):
        return self._get_prop('dateToSubmit')

    @property
    def maxAttempts(self):
        return self._get_prop('maxAttempts')

    @property
    def maxSubmits(self):
        return self._get_prop('maxSubmits')


class Generatable(BaseEntity):
    pass


class Referrable(BaseEntity):
    pass


class Targetable(BaseEntity):
    pass


### Derived entities ###


## Membership entities
class Membership(Entity):
    def __init__(self, member=None, organization=None, roles=None, status=None, **kwargs):
        Entity.__init__(self, **kwargs)
        self._set_obj_prop('member', member, t=ENTITY_TYPES['AGENT'], req=True)
        self._set_obj_prop('organization', organization, t=ENTITY_TYPES['ORGANIZATION'], req=True)

        if roles and isinstance(roles, MutableSequence):
            if set(roles).issubset(set(CALIPER_ROLES.values())):
                self._set_list_prop('roles', roles)
            else:
                raise_with_traceback(ValueError('roles must be in the list of valid Role values'))
        elif roles:
            raise_with_traceback(ValueError('roles must be a list of valid Roles values'))
        else:
            self._set_list_prop('roles', None)

        if status not in CALIPER_STATUS.values():
            raise_with_traceback(ValueError('status must be in the list of valid Status values'))
        else:
            self._set_str_prop('status', status, req=True)

    @property
    def member(self):
        return self._get_prop('member')

    @property
    def organization(self):
        return self._get_prop('organization')

    @property
    def roles(self):
        return self._get_prop('roles')

    @property
    def status(self):
        return self._get_prop('status')


## Agent entities
class Agent(Entity, Referrable):
    def __init__(self, **kwargs):
        Entity.__init__(self, **kwargs)


class SoftwareApplication(Agent):
    def __init__(self, version=None, **kwargs):
        Agent.__init__(self, **kwargs)
        self._set_str_prop('version', version)

    @property
    def version(self):
        return self._get_prop('version')


class Person(Agent):
    def __init__(self, **kwargs):
        Agent.__init__(self, **kwargs)


## Organization entities
class Organization(Agent):
    def __init__(self, members=None, subOrganizationOf=None, **kwargs):
        Entity.__init__(self, **kwargs)
        self._set_list_prop('members', members, t=ENTITY_TYPES['AGENT'])
        self._set_obj_prop('subOrganizationOf', subOrganizationOf, t=ENTITY_TYPES['ORGANIZATION'])

    @property
    def members(self):
        return self._get_prop('members')

    @property
    def subOrganizationOf(self):
        return self._get_prop('subOrganizationOf')


class CourseOffering(Organization):
    def __init__(self, academicSession=None, courseNumber=None, **kwargs):
        Organization.__init__(self, **kwargs)
        self._set_str_prop('academicSession', academicSession)
        self._set_str_prop('courseNumber', courseNumber)

    @property
    def academicSession(self):
        return self._get_prop('academicSession')

    @property
    def courseNumber(self):
        return self._get_prop('courseNumber')


class CourseSection(CourseOffering):
    def __init__(self, category=None, **kwargs):
        CourseOffering.__init__(self, **kwargs)
        self._set_str_prop('category', category)

    @property
    def category(self):
        return self._get_prop('category')


class Group(Organization):
    def __init__(self, members=None, **kwargs):
        Organization.__init__(self, **kwargs)
        self._set_list_prop('members', members, t=ENTITY_TYPES['PERSON'])


## Learning Context
# not really a Caliper Entity, but capable of serializing itself like one, for convenience
class LearningContext(CaliperSerializable):
    def __init__(self, edApp=None, group=None, membership=None, session=None):
        CaliperSerializable.__init__(self)
        self._set_obj_prop('edApp', edApp, t=ENTITY_TYPES['SOFTWARE_APPLICATION'])
        self._set_obj_prop('group', group, t=ENTITY_TYPES['ORGANIZATION'])
        self._set_obj_prop('membership', membership, t=ENTITY_TYPES['MEMBERSHIP'])
        self._set_obj_prop('session', session, t=ENTITY_TYPES['SESSION'])

    @property
    def edApp(self):
        return self._get_prop('edApp')

    @property
    def group(self):
        return self._get_prop('group')

    @property
    def membership(self):
        return self._get_prop('membership')

    @property
    def session(self):
        return self._get_prop('session')


## Learning objective
class LearningObjective(Entity):
    def __init__(self, **kwargs):
        Entity.__init__(self, **kwargs)


## Aggregate measures
class AggregateMeasure(Entity, Generatable):
    def __init__(self,
                 endedAtTime=None,
                 metric=None,
                 startedAtTime=None,
                 metricValue=None,
                 metricValueMax=None,
                 **kwargs):
        Entity.__init__(self, **kwargs)
        self._set_date_prop('endedAtTime', endedAtTime)
        self._set_date_prop('startedAtTime', startedAtTime)
        self._set_float_prop('metricValue', metricValue, req=True)
        self._set_float_prop('metricValueMax', metricValueMax)

        if metric not in CALIPER_METRICS.values():
            raise_with_traceback(ValueError('metric must be in the list of valid Metric values'))
        else:
            self._set_str_prop('metric', metric)

    @property
    def endedAtTime(self):
        return self._get_prop('endedAtTime')

    @endedAtTime.setter
    def endedAtTime(self, new_time):
        self._set_date_prop('endedAtTime', new_time)

    @property
    def metric(self):
        return self._get_prop('metric')

    @property
    def startedAtTime(self):
        return self._get_prop('startedAtTime')

    @property
    def metricValue(self):
        return self._get_prop('metricValue')

    @property
    def metricValueMax(self):
        return self._get_prop('metricValueMax')


class AggregateMeasureCollection(Entity, Generatable):
    def __init__(self, items=None, **kwargs):
        Entity.__init__(self, **kwargs)
        self._set_list_prop('items', items, t=ENTITY_TYPES['AGGREGATE_MEASURE'])

    @property
    def items(self):
        return self._get_prop('items')


## Creative works
class DigitalResource(Entity, Generatable, Referrable, Targetable):
    def __init__(self,
                 learningObjectives=None,
                 creators=None,
                 datePublished=None,
                 isPartOf=None,
                 keywords=None,
                 mediaType=None,
                 version=None,
                 **kwargs):
        Entity.__init__(self, **kwargs)
        self._set_list_prop(
            'learningObjectives', learningObjectives, t=ENTITY_TYPES['LEARNING_OBJECTIVE'])
        self._set_list_prop('creators', creators, t=ENTITY_TYPES['AGENT'])
        self._set_date_prop('datePublished', datePublished)
        self._set_obj_prop('isPartOf', isPartOf, t=ENTITY_TYPES['ENTITY'])
        self._set_list_prop('keywords', keywords, t=str)
        self._set_str_prop('mediaType', mediaType)
        self._set_str_prop('version', version)

    @property
    def learningObjectives(self):
        return self._get_prop('learningObjectives')

    @property
    def creators(self):
        return self._get_prop('creators')

    @property
    def datePublished(self):
        return self._get_prop('datePublished')

    @property
    def isPartOf(self):
        return self._get_prop('isPartOf')

    @isPartOf.setter
    def isPartOf(self, new_object):
        self._set_obj_prop('isPartOf', new_object, t=ENTITY_TYPES['ENTITY'])

    @property
    def keywords(self):
        return self._get_prop('keywords')

    @property
    def mediaType(self):
        return self._get_prop('mediaType')

    @property
    def version(self):
        return self._get_prop('version')


class DigitalResourceCollection(DigitalResource):
    def __init__(self, items=None, **kwargs):
        DigitalResource.__init__(self, **kwargs)
        self._set_list_prop('items', items, t=ENTITY_TYPES['DIGITAL_RESOURCE'])

    @property
    def items(self):
        return self._get_prop('items')


class Frame(DigitalResource, Targetable):
    def __init__(self, index=None, **kwargs):
        DigitalResource.__init__(self, **kwargs)
        self._set_int_prop('index', index, req=True)

    @property
    def index(self):
        return self._get_prop('index')


class Reading(DigitalResource):
    def __init__(self, **kwargs):
        DigitalResource.__init__(self, **kwargs)


# not a digital resource, just a web endpoint
class Link(Entity, Targetable):
    def __init__(self, **kwargs):
        Entity.__init__(self, **kwargs)


class LtiLink(DigitalResource):
    def __init__(self, messageType=None, **kwargs):
        DigitalResource.__init__(self, **kwargs)

        if messageType and messageType not in CALIPER_LTI_MESSAGES.values():
            raise_with_traceback(
                ValueError('LTI message type must be in list of valid message types'))
        else:
            self._set_str_prop('messageType', messageType)


class WebPage(DigitalResource):
    def __init__(self, **kwargs):
        DigitalResource.__init__(self, **kwargs)


class Document(DigitalResource):
    def __init__(self, **kwargs):
        DigitalResource.__init__(self, **kwargs)


class Chapter(DigitalResource):
    def __init__(self, **kwargs):
        DigitalResource.__init__(self, **kwargs)


class Page(DigitalResource):
    def __init__(self, **kwargs):
        DigitalResource.__init__(self, **kwargs)


class EpubChapter(DigitalResource):
    def __init__(self, **kwargs):
        DigitalResource.__init__(self, **kwargs)


class EpubPart(DigitalResource):
    def __init__(self, **kwargs):
        DigitalResource.__init__(self, **kwargs)


class EpubSubChapter(DigitalResource):
    def __init__(self, **kwargs):
        DigitalResource.__init__(self, **kwargs)


class EpubVolume(DigitalResource):
    def __init__(self, **kwargs):
        DigitalResource.__init__(self, **kwargs)


## Annotation entities
class Annotation(Entity, Generatable):
    def __init__(self, annotated=None, annotator=None, **kwargs):
        Entity.__init__(self, **kwargs)
        self._set_obj_prop('annotated', annotated, t=ENTITY_TYPES['DIGITAL_RESOURCE'], req=True)
        self._set_obj_prop('annotator', annotator, t=ENTITY_TYPES['PERSON'], req=True)

    @property
    def annotated(self):
        return self._get_prop('annotated')

    @property
    def annotator(self):
        return self._get_prop('annotator')


class BookmarkAnnotation(Annotation):
    def __init__(self, bookmarkNotes=None, **kwargs):
        Annotation.__init__(self, **kwargs)
        self._set_str_prop('bookmarkNotes', bookmarkNotes)

    @property
    def bookmarkNotes(self):
        return self._get_prop('bookmarkNotes')


class HighlightAnnotation(Annotation):
    def __init__(self, selection=None, selectionText=None, **kwargs):
        Annotation.__init__(self, **kwargs)
        self._set_obj_prop('selection', selection, t=ENTITY_TYPES['TEXT_POSITION_SELECTOR'])
        self._set_str_prop('selectionText', selectionText)

    @property
    def selection(self):
        return self._get_prop('selection')

    @property
    def selectionText(self):
        return self._get_prop('selectionText')


class SharedAnnotation(Annotation):
    def __init__(self, withAgents=None, **kwargs):
        Annotation.__init__(self, **kwargs)
        self._set_list_prop('withAgents', withAgents, t=ENTITY_TYPES['AGENT'])

    @property
    def withAgents(self):
        return self._get_prop('withAgents')


class TagAnnotation(Annotation):
    def __init__(self, tags=None, **kwargs):
        Annotation.__init__(self, **kwargs)
        self._set_list_prop('tags', tags, t=str)

    @property
    def tags(self):
        return self._get_prop('tags')


class TextPositionSelector(BaseEntity):
    def __init__(self, start=None, end=None, **kwargs):
        BaseEntity.__init__(self, **kwargs)
        self._set_int_prop('end', end, req=True)
        self._set_int_prop('start', start, req=True)

    @property
    def end(self):
        return self._get_prop('end')

    @end.setter
    def end(self, new_end):
        self._set_int_prop('end', new_end, req=True)

    @property
    def start(self):
        return self._get_prop('start')

    @start.setter
    def start(self, new_start):
        self._set_int_prop('start', new_start, req=True)


## Assessment entities
class AssignableDigitalResource(DigitalResource, Assignable):
    def __init__(self,
                 dateToActivate=None,
                 dateToShow=None,
                 dateToStartOn=None,
                 dateToSubmit=None,
                 maxAttempts=None,
                 maxSubmits=None,
                 maxScore=None,
                 **kwargs):
        DigitalResource.__init__(self, **kwargs)
        self._set_date_prop('dateToActivate', dateToActivate)
        self._set_date_prop('dateToShow', dateToShow)
        self._set_date_prop('dateToStartOn', dateToStartOn)
        self._set_date_prop('dateToSubmit', dateToSubmit)
        self._set_int_prop('maxAttempts', maxAttempts)
        self._set_int_prop('maxSubmits', maxSubmits)
        self._set_float_prop('maxScore', maxScore)

    @property
    def dateToActivate(self):
        return self._get_prop('dateToActivate')

    @property
    def dateToShow(self):
        return self._get_prop('dateToShow')

    @property
    def dateToStartOn(self):
        return self._get_prop('dateToStartOn')

    @property
    def dateToSubmit(self):
        return self._get_prop('dateToSubmit')

    @property
    def maxAttempts(self):
        return self._get_prop('maxAttempts')

    @property
    def maxScore(self):
        return self._get_prop('maxScore')

    @property
    def maxSubmits(self):
        return self._get_prop('maxSubmits')


class Assessment(AssignableDigitalResource, DigitalResourceCollection):
    def __init__(self, items=None, **kwargs):
        AssignableDigitalResource.__init__(self, **kwargs)
        self._set_list_prop('items', items, t=ENTITY_TYPES['ASSESSMENT_ITEM'])


class AssessmentItem(AssignableDigitalResource):
    def __init__(self, isTimeDependent=None, **kwargs):
        AssignableDigitalResource.__init__(self, **kwargs)
        self._set_bool_prop('isTimeDependent', isTimeDependent)

    @property
    def isTimeDependent(self):
        return self._get_prop('isTimeDependent')


## Attempt and Response entities
class Attempt(Entity, Generatable):
    def __init__(self,
                 assignable=None,
                 assignee=None,
                 count=None,
                 duration=None,
                 endedAtTime=None,
                 isPartOf=None,
                 startedAtTime=None,
                 **kwargs):
        Entity.__init__(self, **kwargs)
        self._set_obj_prop('assignable', assignable, t=MARKER_TYPES['ASSIGNABLE'])
        self._set_obj_prop('assignee', assignee, t=ENTITY_TYPES['PERSON'])
        self._set_int_prop('count', count)
        self._set_duration_prop('duration', duration)
        self._set_date_prop('endedAtTime', endedAtTime)
        self._set_obj_prop('isPartOf', isPartOf, t=ENTITY_TYPES['ATTEMPT'])
        self._set_date_prop('startedAtTime', startedAtTime)

    @property
    def assignable(self):
        return self._get_prop('assignable')

    @property
    def assignee(self):
        return self._get_prop('assignee')

    @property
    def count(self):
        return self._get_prop('count')

    @property
    def duration(self):
        return self._get_prop('duration')

    @duration.setter
    def duration(self, new_duration):
        self._set_duration_prop('duration', new_duration)

    @property
    def endedAtTime(self):
        return self._get_prop('endedAtTime')

    @endedAtTime.setter
    def endedAtTime(self, new_time):
        self._set_date_prop('endedAtTime', new_time)

    @property
    def isPartOf(self):
        return self._get_prop('isPartOf')

    @isPartOf.setter
    def isPartOf(self, new_object):
        self._set_obj_prop('isPartOf', new_object, t=ENTITY_TYPES['Attempt'])

    @property
    def startedAtTime(self):
        return self._get_prop('startedAtTime')


class Response(Entity, Generatable):
    def __init__(self, attempt=None, duration=None, endedAtTime=None, startedAtTime=None,
                 **kwargs):
        Entity.__init__(self, **kwargs)
        self._set_obj_prop('attempt', attempt, t=ENTITY_TYPES['ATTEMPT'])
        self._set_duration_prop('duration', duration)
        self._set_date_prop('endedAtTime', endedAtTime)
        self._set_date_prop('startedAtTime', startedAtTime)

    @property
    def attempt(self):
        return self._get_prop('attempt')

    @property
    def duration(self):
        return self._get_prop('duration')

    @duration.setter
    def duration(self, new_duration):
        self._set_duration_prop('duration', new_duration)

    @property
    def endedAtTime(self):
        return self._get_prop('endedAtTime')

    @endedAtTime.setter
    def endedAtTime(self, new_time):
        self._set_date_prop('endedAtTime', new_time)

    @property
    def startedAtTime(self):
        return self._get_prop('startedAtTime')


class FillinBlankResponse(Response):
    def __init__(self, values=None, **kwargs):
        Response.__init__(self, **kwargs)
        self._set_list_prop('values', values, t=str)

    @property
    def values(self):
        return self._get_prop('values')


class MultipleChoiceResponse(Response):
    def __init__(self, value=None, **kwargs):
        Response.__init__(self, **kwargs)
        self._set_str_prop('value', value)

    @property
    def value(self):
        return self._get_prop('value')


class MultipleResponseResponse(Response):
    def __init__(self, values=None, **kwargs):
        Response.__init__(self, **kwargs)
        self._set_list_prop('values', values, t=str)

    @property
    def values(self):
        return self._get_prop('values')


class SelectTextResponse(Response):
    def __init__(self, values=None, **kwargs):
        Response.__init__(self, **kwargs)
        self._set_list_prop('values', values, t=str)

    @property
    def values(self):
        return self._get_prop('values')


class TrueFalseResponse(Response):
    def __init__(self, value=None, **kwargs):
        Response.__init__(self, **kwargs)
        self._set_str_prop('value', value)

    @property
    def value(self):
        return self._get_prop('value')


## Discussion forum entities
class Forum(DigitalResourceCollection):
    def __init__(self, items=None, **kwargs):
        DigitalResourceCollection.__init__(self, **kwargs)
        self._set_list_prop('items', items, t=ENTITY_TYPES['THREAD'])


class Thread(DigitalResourceCollection):
    def __init__(self, items=None, **kwargs):
        DigitalResourceCollection.__init__(self, **kwargs)
        self._set_list_prop('items', items, t=ENTITY_TYPES['MESSAGE'])


class Message(DigitalResource):
    def __init__(self, body=None, replyTo=None, attachments=None, **kwargs):
        DigitalResource.__init__(self, **kwargs)
        self._set_str_prop('body', body)
        self._set_obj_prop('replyTo', replyTo, t=ENTITY_TYPES['MESSAGE'])
        self._set_list_prop('attachments', attachments, t=ENTITY_TYPES['DIGITAL_RESOURCE'])

    @property
    def body(self):
        return self._get_prop('body')

    @property
    def replyTo(self):
        return self._get_prop('replyTo')

    @property
    def attachments(self):
        return self._get_prop('attachments')


## Media entities
class MediaObject(DigitalResource):
    def __init__(self, duration=None, **kwargs):
        DigitalResource.__init__(self, **kwargs)
        self._set_duration_prop('duration', duration)

    @property
    def duration(self):
        return self._get_prop('duration')


class MediaLocation(DigitalResource, Targetable):
    def __init__(self, currentTime=None, **kwargs):
        DigitalResource.__init__(self, **kwargs)
        self._set_duration_prop('currentTime', currentTime)

    @property
    def currentTime(self):
        return self._get_prop('currentTime')


class AudioObject(MediaObject):
    def __init__(self, muted=None, volumeLevel=None, volumeMax=None, volumeMin=None, **kwargs):
        MediaObject.__init__(self, **kwargs)
        self._set_bool_prop('muted', muted)
        self._set_str_prop('volumeLevel', volumeLevel)
        self._set_str_prop('volumeMax', volumeMax)
        self._set_str_prop('volumeMin', volumeMin)

    @property
    def muted(self):
        return self._get_prop('muted')

    @property
    def volumeLevel(self):
        return self._get_prop('volumeLevel')

    @property
    def volumeMax(self):
        return self._get_prop('volumeMax')

    @property
    def volumeMin(self):
        return self._get_prop('volumeMin')


class ImageObject(MediaObject):
    def __init__(self, **kwargs):
        MediaObject.__init__(self, **kwargs)


class VideoObject(MediaObject):
    def __init__(self, **kwargs):
        MediaObject.__init__(self, **kwargs)


## Outcome entities
class Result(Entity, Generatable):
    def __init__(self,
                 attempt=None,
                 comment=None,
                 maxResultScore=None,
                 resultScore=None,
                 scoredBy=None,
                 **kwargs):
        Entity.__init__(self, **kwargs)
        self._set_obj_prop('attempt', attempt, t=ENTITY_TYPES['ATTEMPT'], req=True)
        self._set_str_prop('comment', comment)
        self._set_float_prop('maxResultScore', maxResultScore)
        self._set_float_prop('resultScore', resultScore)
        self._set_obj_prop('scoredBy', scoredBy, t=ENTITY_TYPES['AGENT'])

    @property
    def attempt(self):
        return self._get_prop('attempt')

    @property
    def comment(self):
        return self._get_prop('comment')

    @property
    def maxResultScore(self):
        return self._get_prop('maxResultScore')

    @property
    def resultScore(self):
        return self._get_prop('resultScore')

    @property
    def scoredBy(self):
        return self._get_prop('scoredBy')


class Score(Entity, Generatable):
    def __init__(self,
                 attempt=None,
                 comment=None,
                 maxScore=None,
                 scoreGiven=None,
                 scoredBy=None,
                 **kwargs):
        Entity.__init__(self, **kwargs)
        self._set_obj_prop('attempt', attempt, t=ENTITY_TYPES['ATTEMPT'], req=True)
        self._set_str_prop('comment', comment)
        self._set_float_prop('maxScore', maxScore)
        self._set_float_prop('scoreGiven', scoreGiven)
        self._set_obj_prop('scoredBy', scoredBy, t=ENTITY_TYPES['AGENT'])

    @property
    def attempt(self):
        return self._get_prop('attempt')

    @property
    def comment(self):
        return self._get_prop('comment')

    @property
    def maxScore(self):
        return self._get_prop('maxScore')

    @property
    def scoreGiven(self):
        return self._get_prop('scoreGiven')

    @property
    def scoredBy(self):
        return self._get_prop('scoredBy')


## Search entities
class Query(Entity):
    def __init__(self, creator=None, searchTarget=None, searchTerms=None, **kwargs):
        Entity.__init__(self, **kwargs)
        self._set_obj_prop('creator', creator, t=ENTITY_TYPES['PERSON'])
        self._set_obj_prop('searchTarget', searchTarget, t=ENTITY_TYPES['ENTITY'])
        self._set_str_prop('searchTerms', searchTerms)

    @property
    def creator(self):
        return self._get_prop('creator')

    @property
    def searchTarget(self):
        return self._get_prop('searchTarget')

    @property
    def searchTerms(self):
        return self._get_prop('searchTerms')


class SearchResponse(Entity, Generatable):
    def __init__(self,
                 searchProvider=None,
                 searchTarget=None,
                 query=None,
                 searchResultsItemCount=None,
                 searchResults=None,
                 **kwargs):
        Entity.__init__(self, **kwargs)
        self._set_obj_prop(
            'searchProvider', searchProvider, t=ENTITY_TYPES['SOFTWARE_APPLICATION'])
        self._set_obj_prop('searchTarget', searchTarget, t=ENTITY_TYPES['ENTITY'])
        self._set_obj_prop('query', query, t=ENTITY_TYPES['QUERY'])
        self._set_int_prop('searchResultsItemCount', searchResultsItemCount)
        self._set_list_prop('searchResults', searchResults, t=ENTITY_TYPES['ENTITY'])

    @property
    def searchProvider(self):
        return self._get_prop('searchProvider')

    @property
    def searchTarget(self):
        return self._get_prop('searchTarget')

    @property
    def query(self):
        return self._get_prop('query')

    @property
    def searchResultsItemCount(self):
        return self._get_prop('searchResultsItemCount')

    @searchResultsItemCount.setter
    def searchResultsItemCount(self, new_count):
        self._set_int_prop('searchResultsItemCount', new_count)

    @property
    def searchResults(self):
        return self._get_prop('searchResults')

    @searchResults.setter
    def searchResults(self, new_results):
        self._set_list_prop('searchResults', new_results, t=ENTITY_TYPES['ENTITY'])


## Session entities
class Session(Entity, Generatable, Targetable):
    def __init__(self, duration=None, endedAtTime=None, startedAtTime=None, user=None, **kwargs):
        Entity.__init__(self, **kwargs)
        self._set_duration_prop('duration', duration)
        self._set_date_prop('endedAtTime', endedAtTime)
        self._set_date_prop('startedAtTime', startedAtTime)
        self._set_obj_prop('user', user, t=ENTITY_TYPES['PERSON'])

    @property
    def duration(self):
        return self._get_prop('duration')

    @duration.setter
    def duration(self, new_duration):
        self._set_duration_prop('duration', new_duration)

    @property
    def endedAtTime(self):
        return self._get_prop('endedAtTime')

    @endedAtTime.setter
    def endedAtTime(self, new_time):
        self._set_date_prop('endedAtTime', new_time)

    @property
    def startedAtTime(self):
        return self._get_prop('startedAtTime')

    @property
    def user(self):
        return self._get_prop('user')


class LtiSession(Session):
    def __init__(self, messageParameters=None, **kwargs):
        Session.__init__(self, **kwargs)
        self._set_dict_prop('messageParameters', messageParameters)

    @property
    def messageParameters(self):
        return self._get_prop('messageParameters')
