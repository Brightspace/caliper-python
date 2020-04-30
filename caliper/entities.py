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

from collections.abc import MutableSequence

from caliper.constants import ENTITY_TYPES
from caliper.constants import (
    CALIPER_LTI_MESSAGES,
    CALIPER_METRICS,
    CALIPER_ROLES,
    CALIPER_STATUS,
    CALIPER_SYSIDTYPES,
)
from caliper.base import BaseEntity


# Fundamental entities
# Base entity class
class Entity(BaseEntity):

    # Use the base context value here, but preserve the context labels
    # in case, in the future, indivdual contexts start getting split out

    def __init__(
        self,
        id=None,
        context=None,
        profile=None,
        dateCreated=None,
        dateModified=None,
        description=None,
        name=None,
        otherIdentifiers=None,
        extensions=None,
    ):
        BaseEntity.__init__(self, context=context, profile=profile)
        self._set_id(id)
        self._set_datetime_prop("dateCreated", dateCreated)
        self._set_datetime_prop("dateModified", dateModified)
        self._set_str_prop("description", description)
        self._set_str_prop("name", name)
        self._set_list_prop(
            "otherIdentifiers", otherIdentifiers, t=ENTITY_TYPES["SYSTEM_IDENTIFIER"]
        )
        self._set_dict_prop("extensions", extensions)

    @property
    def id(self):
        return self._get_prop("id")

    @property
    def dateCreated(self):
        return self._get_prop("dateCreated")

    @property
    def dateModified(self):
        return self._get_prop("dateModified")

    @property
    def description(self):
        return self._get_prop("description")

    @property
    def name(self):
        return self._get_prop("name")

    @property
    def otherIdentifiers(self):
        return self._get_prop("otherIdentifiers")

    @property
    def extensions(self):
        return self._get_prop("extensions")


class SystemIdentifier(BaseEntity):
    def __init__(
        self,
        identifier=None,
        identifierType=None,
        source=None,
        extensions=None,
        **kwargs
    ):
        BaseEntity.__init__(self, **kwargs)
        self._set_str_prop("identifier", identifier, req=True)
        self._set_obj_prop("source", source, t=ENTITY_TYPES["SOFTWARE_APPLICATION"])
        self._set_dict_prop("extensions", extensions)

        if identifierType not in CALIPER_SYSIDTYPES.values():
            raise ValueError(
                "identifierType must be in the list of valid system identifier types"
            )
        else:
            self._set_str_prop("identifierType", identifierType, req=True)

    @property
    def identifier(self):
        return self._get_prop("identifier")

    @property
    def identifierType(self):
        return self._get_prop("identifierType")

    @property
    def source(self):
        return self._get_prop("source")

    @property
    def extensions(self):
        return self._get_prop("extensions")


# Fundamental entities
class Collection(Entity):
    def __init__(self, items=None, **kwargs):
        Entity.__init__(self, **kwargs)
        self._set_list_prop("items", items, t=ENTITY_TYPES["ENTITY"])

    @property
    def items(self):
        return self._get_prop("items")


# Derived entities
# Membership entities
class Membership(Entity):
    def __init__(
        self, member=None, organization=None, roles=None, status=None, **kwargs
    ):
        Entity.__init__(self, **kwargs)
        self._set_obj_prop("member", member, t=ENTITY_TYPES["AGENT"], req=True)
        self._set_obj_prop(
            "organization", organization, t=ENTITY_TYPES["ORGANIZATION"], req=True
        )

        if roles and isinstance(roles, MutableSequence):
            if set(roles).issubset(set(CALIPER_ROLES.values())):
                self._set_list_prop("roles", roles)
            else:
                raise ValueError("roles must be in the list of valid Role values")
        elif roles:
            raise ValueError("roles must be a list of valid Roles values")
        else:
            self._set_list_prop("roles", None)

        if status not in CALIPER_STATUS.values():
            raise ValueError("status must be in the list of valid Status values")
        else:
            self._set_str_prop("status", status, req=True)

    @property
    def member(self):
        return self._get_prop("member")

    @property
    def organization(self):
        return self._get_prop("organization")

    @property
    def roles(self):
        return self._get_prop("roles")

    @property
    def status(self):
        return self._get_prop("status")


# Agent entities
class Agent(Entity):
    def __init__(self, **kwargs):
        Entity.__init__(self, **kwargs)


class SoftwareApplication(Agent):
    def __init__(
        self, host=None, ipAddress=None, userAgent=None, version=None, **kwargs
    ):
        Agent.__init__(self, **kwargs)
        self._set_str_prop("host", host)
        self._set_str_prop("ipAddress", ipAddress)
        self._set_str_prop("userAgent", userAgent)
        self._set_str_prop("version", version)

    @property
    def host(self):
        return self._get_prop("host")

    @property
    def ipAddress(self):
        return self._get_prop("ipAddress")

    @property
    def userAgent(self):
        return self._get_prop("userAgent")

    @property
    def version(self):
        return self._get_prop("version")


class Person(Agent):
    def __init__(self, **kwargs):
        Agent.__init__(self, **kwargs)


# Organization entities
class Organization(Agent):
    def __init__(self, members=None, subOrganizationOf=None, **kwargs):
        Entity.__init__(self, **kwargs)
        self._set_list_prop("members", members, t=ENTITY_TYPES["AGENT"])
        self._set_obj_prop(
            "subOrganizationOf", subOrganizationOf, t=ENTITY_TYPES["ORGANIZATION"]
        )

    @property
    def members(self):
        return self._get_prop("members")

    @property
    def subOrganizationOf(self):
        return self._get_prop("subOrganizationOf")


class CourseOffering(Organization):
    def __init__(self, academicSession=None, courseNumber=None, **kwargs):
        Organization.__init__(self, **kwargs)
        self._set_str_prop("academicSession", academicSession)
        self._set_str_prop("courseNumber", courseNumber)

    @property
    def academicSession(self):
        return self._get_prop("academicSession")

    @property
    def courseNumber(self):
        return self._get_prop("courseNumber")


class CourseSection(CourseOffering):
    def __init__(self, category=None, **kwargs):
        CourseOffering.__init__(self, **kwargs)
        self._set_str_prop("category", category)

    @property
    def category(self):
        return self._get_prop("category")


class Group(Organization):
    def __init__(self, members=None, **kwargs):
        Organization.__init__(self, **kwargs)
        self._set_list_prop("members", members, t=ENTITY_TYPES["PERSON"])


# Learning objective
class LearningObjective(Entity):
    def __init__(self, **kwargs):
        Entity.__init__(self, **kwargs)


# Aggregate measures
class AggregateMeasure(Entity):
    def __init__(
        self,
        endedAtTime=None,
        metric=None,
        startedAtTime=None,
        metricValue=None,
        maxMetricValue=None,
        **kwargs
    ):
        Entity.__init__(self, **kwargs)
        self._set_datetime_prop("endedAtTime", endedAtTime)
        self._set_datetime_prop("startedAtTime", startedAtTime)
        self._set_float_prop("metricValue", metricValue, req=True)
        self._set_float_prop("maxMetricValue", maxMetricValue)

        if metric not in CALIPER_METRICS.values():
            raise ValueError("metric must be in the list of valid Metric values")
        else:
            self._set_str_prop("metric", metric)

    @property
    def endedAtTime(self):
        return self._get_prop("endedAtTime")

    @endedAtTime.setter
    def endedAtTime(self, new_time):
        self._set_datetime_prop("endedAtTime", new_time)

    @property
    def metric(self):
        return self._get_prop("metric")

    @property
    def startedAtTime(self):
        return self._get_prop("startedAtTime")

    @property
    def metricValue(self):
        return self._get_prop("metricValue")

    @property
    def maxMetricValue(self):
        return self._get_prop("maxMetricValue")


class AggregateMeasureCollection(Collection):
    def __init__(self, items=None, **kwargs):
        Collection.__init__(self, **kwargs)
        self._set_list_prop("items", items, t=ENTITY_TYPES["AGGREGATE_MEASURE"])


# Creative works
class DigitalResource(Entity):
    def __init__(
        self,
        learningObjectives=None,
        creators=None,
        datePublished=None,
        isPartOf=None,
        keywords=None,
        mediaType=None,
        storageName=None,
        version=None,
        **kwargs
    ):
        Entity.__init__(self, **kwargs)
        self._set_list_prop(
            "learningObjectives",
            learningObjectives,
            t=ENTITY_TYPES["LEARNING_OBJECTIVE"],
        )
        self._set_list_prop("creators", creators, t=ENTITY_TYPES["AGENT"])
        self._set_datetime_prop("datePublished", datePublished)
        self._set_obj_prop("isPartOf", isPartOf, t=ENTITY_TYPES["ENTITY"])
        self._set_list_prop("keywords", keywords, t=str)
        self._set_str_prop("mediaType", mediaType)
        self._set_str_prop("storageName", storageName)
        self._set_str_prop("version", version)

    @property
    def learningObjectives(self):
        return self._get_prop("learningObjectives")

    @property
    def creators(self):
        return self._get_prop("creators")

    @property
    def datePublished(self):
        return self._get_prop("datePublished")

    @property
    def isPartOf(self):
        return self._get_prop("isPartOf")

    @isPartOf.setter
    def isPartOf(self, new_object):
        self._set_obj_prop("isPartOf", new_object, t=ENTITY_TYPES["ENTITY"])

    @property
    def keywords(self):
        return self._get_prop("keywords")

    @property
    def mediaType(self):
        return self._get_prop("mediaType")

    @property
    def storageName(self):
        return self._get_prop("storageName")

    @property
    def version(self):
        return self._get_prop("version")


class DigitalResourceCollection(DigitalResource, Collection):
    def __init__(self, items=None, **kwargs):
        DigitalResource.__init__(self, **kwargs)
        self._set_list_prop("items", items, t=ENTITY_TYPES["DIGITAL_RESOURCE"])


class Frame(DigitalResource):
    def __init__(self, index=None, **kwargs):
        DigitalResource.__init__(self, **kwargs)
        self._set_int_prop("index", index)

    @property
    def index(self):
        return self._get_prop("index")


class Reading(DigitalResource):
    def __init__(self, **kwargs):
        DigitalResource.__init__(self, **kwargs)


# not a digital resource, just a web endpoint
class Link(Entity):
    def __init__(self, **kwargs):
        Entity.__init__(self, **kwargs)


class LtiLink(DigitalResource):
    def __init__(self, messageType=None, **kwargs):
        DigitalResource.__init__(self, **kwargs)

        if messageType and messageType not in CALIPER_LTI_MESSAGES.values():
            raise ValueError("LTI message type must be in list of valid message types")
        else:
            self._set_str_prop("messageType", messageType)


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


# Annotation entities
class Annotation(Entity):
    def __init__(self, annotated=None, annotator=None, **kwargs):
        Entity.__init__(self, **kwargs)
        self._set_obj_prop(
            "annotated", annotated, t=ENTITY_TYPES["DIGITAL_RESOURCE"], req=True
        )
        self._set_obj_prop("annotator", annotator, t=ENTITY_TYPES["PERSON"], req=True)

    @property
    def annotated(self):
        return self._get_prop("annotated")

    @property
    def annotator(self):
        return self._get_prop("annotator")


class BookmarkAnnotation(Annotation):
    def __init__(self, bookmarkNotes=None, **kwargs):
        Annotation.__init__(self, **kwargs)
        self._set_str_prop("bookmarkNotes", bookmarkNotes)

    @property
    def bookmarkNotes(self):
        return self._get_prop("bookmarkNotes")


class HighlightAnnotation(Annotation):
    def __init__(self, selection=None, selectionText=None, **kwargs):
        Annotation.__init__(self, **kwargs)
        self._set_obj_prop(
            "selection", selection, t=ENTITY_TYPES["TEXT_POSITION_SELECTOR"]
        )
        self._set_str_prop("selectionText", selectionText)

    @property
    def selection(self):
        return self._get_prop("selection")

    @property
    def selectionText(self):
        return self._get_prop("selectionText")


class SharedAnnotation(Annotation):
    def __init__(self, withAgents=None, **kwargs):
        Annotation.__init__(self, **kwargs)
        self._set_list_prop("withAgents", withAgents, t=ENTITY_TYPES["AGENT"])

    @property
    def withAgents(self):
        return self._get_prop("withAgents")


class TagAnnotation(Annotation):
    def __init__(self, tags=None, **kwargs):
        Annotation.__init__(self, **kwargs)
        self._set_list_prop("tags", tags, t=str)

    @property
    def tags(self):
        return self._get_prop("tags")


class TextPositionSelector(BaseEntity):
    def __init__(self, start=None, end=None, extensions=None, **kwargs):
        BaseEntity.__init__(self, **kwargs)
        self._set_int_prop("end", end, req=True)
        self._set_int_prop("start", start, req=True)
        self._set_dict_prop("extensions", extensions)

    @property
    def end(self):
        return self._get_prop("end")

    @end.setter
    def end(self, new_end):
        self._set_int_prop("end", new_end, req=True)

    @property
    def start(self):
        return self._get_prop("start")

    @start.setter
    def start(self, new_start):
        self._set_int_prop("start", new_start, req=True)

    @property
    def extensions(self):
        return self._get_prop("extensions")


# Assessment entities
class AssignableDigitalResource(DigitalResource):
    def __init__(
        self,
        dateToActivate=None,
        dateToShow=None,
        dateToStartOn=None,
        dateToSubmit=None,
        maxAttempts=None,
        maxSubmits=None,
        maxScore=None,
        **kwargs
    ):
        DigitalResource.__init__(self, **kwargs)
        self._set_datetime_prop("dateToActivate", dateToActivate)
        self._set_datetime_prop("dateToShow", dateToShow)
        self._set_datetime_prop("dateToStartOn", dateToStartOn)
        self._set_datetime_prop("dateToSubmit", dateToSubmit)
        self._set_int_prop("maxAttempts", maxAttempts)
        self._set_int_prop("maxSubmits", maxSubmits)
        self._set_float_prop("maxScore", maxScore)

    @property
    def datePublished(self):
        return self._get_prop("datePublished")

    @property
    def dateToActivate(self):
        return self._get_prop("dateToActivate")

    @property
    def dateToShow(self):
        return self._get_prop("dateToShow")

    @property
    def dateToStartOn(self):
        return self._get_prop("dateToStartOn")

    @property
    def dateToSubmit(self):
        return self._get_prop("dateToSubmit")

    @property
    def maxAttempts(self):
        return self._get_prop("maxAttempts")

    @property
    def maxScore(self):
        return self._get_prop("maxScore")


class Assessment(AssignableDigitalResource, DigitalResourceCollection):
    def __init__(self, items=None, **kwargs):
        AssignableDigitalResource.__init__(self, **kwargs)
        self._set_list_prop("items", items, t=ENTITY_TYPES["ASSESSMENT_ITEM"])


class AssessmentItem(AssignableDigitalResource):
    def __init__(self, isTimeDependent=None, **kwargs):
        AssignableDigitalResource.__init__(self, **kwargs)
        self._set_bool_prop("isTimeDependent", isTimeDependent)

    @property
    def isTimeDependent(self):
        return self._get_prop("isTimeDependent")


# Attempt and Response entities
class Attempt(Entity):
    def __init__(
        self,
        assignable=None,
        assignee=None,
        count=None,
        duration=None,
        endedAtTime=None,
        isPartOf=None,
        startedAtTime=None,
        **kwargs
    ):
        Entity.__init__(self, **kwargs)
        self._set_obj_prop("assignable", assignable, t=ENTITY_TYPES["DIGITAL_RESOURCE"])
        self._set_obj_prop("assignee", assignee, t=ENTITY_TYPES["PERSON"])
        self._set_int_prop("count", count)
        self._set_duration_prop("duration", duration)
        self._set_datetime_prop("endedAtTime", endedAtTime)
        self._set_obj_prop("isPartOf", isPartOf, t=ENTITY_TYPES["ATTEMPT"])
        self._set_datetime_prop("startedAtTime", startedAtTime)

    @property
    def assignable(self):
        return self._get_prop("assignable")

    @property
    def assignee(self):
        return self._get_prop("assignee")

    @property
    def count(self):
        return self._get_prop("count")

    @property
    def duration(self):
        return self._get_prop("duration")

    @duration.setter
    def duration(self, new_duration):
        self._set_duration_prop("duration", new_duration)

    @property
    def endedAtTime(self):
        return self._get_prop("endedAtTime")

    @endedAtTime.setter
    def endedAtTime(self, new_time):
        self._set_datetime_prop("endedAtTime", new_time)

    @property
    def isPartOf(self):
        return self._get_prop("isPartOf")

    @isPartOf.setter
    def isPartOf(self, new_object):
        self._set_obj_prop("isPartOf", new_object, t=ENTITY_TYPES["Attempt"])

    @property
    def startedAtTime(self):
        return self._get_prop("startedAtTime")


class Response(Entity):
    def __init__(
        self,
        attempt=None,
        duration=None,
        endedAtTime=None,
        startedAtTime=None,
        **kwargs
    ):
        Entity.__init__(self, **kwargs)
        self._set_obj_prop("attempt", attempt, t=ENTITY_TYPES["ATTEMPT"])
        self._set_duration_prop("duration", duration)
        self._set_datetime_prop("endedAtTime", endedAtTime)
        self._set_datetime_prop("startedAtTime", startedAtTime)

    @property
    def attempt(self):
        return self._get_prop("attempt")

    @property
    def duration(self):
        return self._get_prop("duration")

    @duration.setter
    def duration(self, new_duration):
        self._set_duration_prop("duration", new_duration)

    @property
    def endedAtTime(self):
        return self._get_prop("endedAtTime")

    @endedAtTime.setter
    def endedAtTime(self, new_time):
        self._set_datetime_prop("endedAtTime", new_time)

    @property
    def startedAtTime(self):
        return self._get_prop("startedAtTime")


class DateTimeResponse(Response):
    def __init__(self, dateTimeSelected=None, **kwargs):
        Response.__init__(self, **kwargs)
        self._set_datetime_prop("dateTimeSelected", dateTimeSelected)

    @property
    def dateTimeSelected(self):
        return self._get_prop("dateTimeSelected")


class FillinBlankResponse(Response):
    def __init__(self, values=None, **kwargs):
        Response.__init__(self, **kwargs)
        self._set_list_prop("values", values, t=str)

    @property
    def values(self):
        return self._get_prop("values")


class MultipleChoiceResponse(Response):
    def __init__(self, value=None, **kwargs):
        Response.__init__(self, **kwargs)
        self._set_str_prop("value", value)

    @property
    def value(self):
        return self._get_prop("value")


class MultipleResponseResponse(Response):
    def __init__(self, values=None, **kwargs):
        Response.__init__(self, **kwargs)
        self._set_list_prop("values", values, t=str)

    @property
    def values(self):
        return self._get_prop("values")


class MultiselectResponse(Response):
    def __init__(self, selections=None, **kwargs):
        Response.__init__(self, **kwargs)
        self._set_list_prop("selections", selections, t=str)

    @property
    def selections(self):
        return self._get_prop("selections")


class OpenEndedResponse(Response):
    def __init__(self, value, **kwargs):
        Response.__init__(self, **kwargs)
        self._set_str_prop("value", value)

    @property
    def value(self):
        return self._get_prop("value")


class RatingScaleResponse(Response):
    def __init__(self, selections=None, **kwargs):
        Response.__init__(self, **kwargs)
        self._set_list_prop("selections", selections, t=[str, float])

    @property
    def selections(self):
        return self._get_prop("selections")


class SelectTextResponse(Response):
    def __init__(self, values=None, **kwargs):
        Response.__init__(self, **kwargs)
        self._set_list_prop("values", values, t=str)

    @property
    def values(self):
        return self._get_prop("values")


class TrueFalseResponse(Response):
    def __init__(self, value=None, **kwargs):
        Response.__init__(self, **kwargs)
        self._set_str_prop("value", value)

    @property
    def value(self):
        return self._get_prop("value")


# Discussion forum entities
class Forum(DigitalResourceCollection):
    def __init__(self, items=None, **kwargs):
        DigitalResourceCollection.__init__(self, **kwargs)
        self._set_list_prop("items", items, t=ENTITY_TYPES["THREAD"])


class Thread(DigitalResourceCollection):
    def __init__(self, items=None, **kwargs):
        DigitalResourceCollection.__init__(self, **kwargs)
        self._set_list_prop("items", items, t=ENTITY_TYPES["MESSAGE"])


class Message(DigitalResource):
    def __init__(self, body=None, replyTo=None, attachments=None, **kwargs):
        DigitalResource.__init__(self, **kwargs)
        self._set_str_prop("body", body)
        self._set_obj_prop("replyTo", replyTo, t=ENTITY_TYPES["MESSAGE"])
        self._set_list_prop(
            "attachments", attachments, t=ENTITY_TYPES["DIGITAL_RESOURCE"]
        )

    @property
    def body(self):
        return self._get_prop("body")

    @property
    def replyTo(self):
        return self._get_prop("replyTo")

    @property
    def attachments(self):
        return self._get_prop("attachments")


# Feedback entities
class Rating(Entity):
    def __init__(
        self,
        rater=None,
        rated=None,
        ratingComment=None,
        question=None,
        selections=None,
        **kwargs
    ):
        Entity.__init__(self, **kwargs)
        self._set_obj_prop("rater", rater, t=ENTITY_TYPES["PERSON"])
        self._set_obj_prop("rated", rated, t=ENTITY_TYPES["ENTITY"])
        self._set_obj_prop("ratingComment", ratingComment, t=ENTITY_TYPES["COMMENT"])
        self._set_obj_prop("question", question, t=ENTITY_TYPES["QUESTION"])
        self._set_list_prop("selections", selections, t=[str, float])

    @property
    def rater(self):
        return self._get_prop("rater")

    @property
    def rated(self):
        return self._get_prop("rated")

    @property
    def ratingComment(self):
        return self._get_prop("ratingComment")

    @property
    def question(self):
        return self._get_prop("question")

    @property
    def selections(self):
        return self._get_prop("selections")


class Comment(Entity):
    def __init__(self, commenter=None, commentedOn=None, value=None, **kwargs):
        Entity.__init__(self, **kwargs)
        self._set_obj_prop("commenter", commenter, t=ENTITY_TYPES["PERSON"])
        self._set_obj_prop("commentedOn", commentedOn, t=ENTITY_TYPES["ENTITY"])
        self._set_str_prop("value", value)

    @property
    def commenter(self):
        return self._get_prop("commenter")

    @property
    def commentedOn(self):
        return self._get_prop("commentedOn")

    @property
    def value(self):
        return self._get_prop("value")


class Question(DigitalResource):
    def __init__(self, questionPosed=None, **kwargs):
        DigitalResource.__init__(self, **kwargs)
        self._set_str_prop("questionPosed", questionPosed)

    @property
    def questionPosed(self):
        return self._get_prop("questionPosed")


class DateTimeQuestion(Question):
    def __init__(
        self, maxDateTime=None, maxLabel=None, minDateTime=None, minLabel=None, **kwargs
    ):
        Question.__init__(self, **kwargs)
        self._set_datetime_prop("maxDateTime", maxDateTime)
        self._set_str_prop("maxLabel", maxLabel)
        self._set_datetime_prop("minDateTime", minDateTime)
        self._set_str_prop("minLabel", minLabel)

    @property
    def maxDateTime(self):
        return self._get_prop("maxDateTime")

    @property
    def maxLabel(self):
        return self._get_prop("maxLabel")

    @property
    def minDateTime(self):
        return self._get_prop("minDateTime")

    @property
    def minLabel(self):
        return self._get_prop("minLabel")


class MultiselectQuestion(Question):
    def __init__(self, itemLabels=None, itemValues=None, points=None, **kwargs):
        Question.__init__(self, **kwargs)
        self._set_list_prop("itemLabels", itemLabels, t=str)
        self._set_list_prop("itemValues", itemValues, t=str)
        self._set_int_prop("points", points)

    @property
    def itemLabels(self):
        return self._get_prop("itemLabels")

    @property
    def itemValues(self):
        return self._get_prop("itemValues")

    @property
    def points(self):
        return self._get_prop("points")


class OpenEndedQuestion(Question):
    def __init__(self, **kwargs):
        Question.__init__(self, **kwargs)


class RatingScaleQuestion(Question):
    def __init__(self, scale=None, **kwargs):
        Question.__init__(self, **kwargs)
        self._set_obj_prop("scale", scale, t=ENTITY_TYPES["SCALE"])

    @property
    def scale(self):
        return self._get_prop("scale")


class Scale(Entity):
    def __init__(self, **kwargs):
        Entity.__init__(self, **kwargs)


class LikertScale(Scale):
    def __init__(self, itemLabels=None, itemValues=None, scalePoints=None, **kwargs):
        Scale.__init__(self, **kwargs)
        self._set_list_prop("itemLabels", itemLabels, t=str)
        self._set_list_prop("itemValues", itemValues, t=str)
        self._set_int_prop("scalePoints", scalePoints)

    @property
    def itemLabels(self):
        return self._get_prop("itemLabels")

    @property
    def itemValues(self):
        return self._get_prop("itemValues")

    @property
    def scalePoints(self):
        return self._get_prop("scalePoints")


class MultiselectScale(Scale):
    def __init__(
        self,
        itemLabels=None,
        itemValues=None,
        isOrderedSelection=None,
        maxSelections=None,
        minSelections=None,
        scalePoints=None,
        **kwargs
    ):
        Scale.__init__(self, **kwargs)
        self._set_list_prop("itemLabels", itemLabels, t=str)
        self._set_list_prop("itemValues", itemValues, t=str)
        self._set_int_prop("maxSelections", maxSelections)
        self._set_int_prop("minSelections", minSelections)
        self._set_bool_prop("isOrderedSelection", isOrderedSelection)
        self._set_int_prop("scalePoints", scalePoints)

    @property
    def itemLabels(self):
        return self._get_prop("itemLabels")

    @property
    def itemValues(self):
        return self._get_prop("itemValues")

    @property
    def maxSelections(self):
        return self._get_prop("maxSelections")

    @property
    def minSelections(self):
        return self._get_prop("minSelections")

    @property
    def isOrderedSelection(self):
        return self._get_prop("isOrderedSelection")

    @property
    def scalePoints(self):
        return self._get_prop("scalePoints")


class NumericScale(Scale):
    def __init__(
        self,
        maxLabel=None,
        maxValue=None,
        minLabel=None,
        minValue=None,
        step=None,
        **kwargs
    ):
        Scale.__init__(self, **kwargs)
        self._set_str_prop("maxLabel", maxLabel)
        self._set_float_prop("maxValue", maxValue)
        self._set_str_prop("minLabel", minLabel)
        self._set_float_prop("minValue", minValue)
        self._set_float_prop("step", step)

    @property
    def maxLabel(self):
        return self._get_prop("maxLabel")

    @property
    def maxValue(self):
        return self._get_prop("maxValue")

    @property
    def minLabel(self):
        return self._get_prop("minLabel")

    @property
    def minValue(self):
        return self._get_prop("minValue")

    @property
    def step(self):
        return self._get_prop("step")


# Survey entities
class Survey(Collection):
    def __init__(self, items=None, **kwargs):
        Collection.__init__(self, **kwargs)
        self._set_list_prop("items", items, t=ENTITY_TYPES["QUESTIONNAIRE"])


class SurveyInvitation(DigitalResource):
    def __init__(
        self, rater=None, sentCount=None, dateSent=None, survey=None, **kwargs
    ):
        DigitalResource.__init__(self, **kwargs)
        self._set_obj_prop("rater", rater, t=ENTITY_TYPES["PERSON"])
        self._set_int_prop("sentCount", sentCount)
        self._set_datetime_prop("dateSent", dateSent)
        self._set_obj_prop("survey", survey, t=ENTITY_TYPES["SURVEY"])

    @property
    def rater(self):
        return self._get_prop("rater")

    @property
    def sentCount(self):
        return self._get_prop("sentCount")

    @property
    def dateSent(self):
        return self._get_prop("dateSent")

    @property
    def survey(self):
        return self._get_prop("survey")


class Questionnaire(DigitalResourceCollection):
    def __init(self, items=None, **kwargs):
        DigitalResourceCollection.__init__(self, **kwargs)
        self._set_list_prop(
            "items", items, t=ENTITY_TYPES["QUESTIONNAIRE_ITEM"], req=True
        )


class QuestionnaireItem(DigitalResource):
    def __init__(self, categories=None, question=None, weight=None, **kwargs):
        DigitalResource.__init__(self, **kwargs)
        self._set_list_prop("categories", categories, t=str)
        self._set_obj_prop("question", question, t=ENTITY_TYPES["QUESTION"])
        self._set_float_prop("weight", weight)

    @property
    def categories(self):
        return self._get_prop("categories")

    @property
    def question(self):
        return self._get_prop("question")

    @property
    def weight(self):
        return self._get_prop("weight")


# Media entities
class MediaObject(DigitalResource):
    def __init__(self, duration=None, **kwargs):
        DigitalResource.__init__(self, **kwargs)
        self._set_duration_prop("duration", duration)

    @property
    def duration(self):
        return self._get_prop("duration")


class MediaLocation(DigitalResource):
    def __init__(self, currentTime=None, **kwargs):
        DigitalResource.__init__(self, **kwargs)
        self._set_duration_prop("currentTime", currentTime)

    @property
    def currentTime(self):
        return self._get_prop("currentTime")


class AudioObject(MediaObject):
    def __init__(
        self, muted=None, volumeLevel=None, volumeMax=None, volumeMin=None, **kwargs
    ):
        MediaObject.__init__(self, **kwargs)
        self._set_bool_prop("muted", muted)
        self._set_str_prop("volumeLevel", volumeLevel)
        self._set_str_prop("volumeMax", volumeMax)
        self._set_str_prop("volumeMin", volumeMin)

    @property
    def muted(self):
        return self._get_prop("muted")

    @property
    def volumeLevel(self):
        return self._get_prop("volumeLevel")

    @property
    def volumeMax(self):
        return self._get_prop("volumeMax")

    @property
    def volumeMin(self):
        return self._get_prop("volumeMin")


class ImageObject(MediaObject):
    def __init__(self, **kwargs):
        MediaObject.__init__(self, **kwargs)


class VideoObject(MediaObject):
    def __init__(self, **kwargs):
        MediaObject.__init__(self, **kwargs)


# Outcome entities
class Result(Entity):
    def __init__(
        self,
        attempt=None,
        comment=None,
        maxResultScore=None,
        resultScore=None,
        scoredBy=None,
        **kwargs
    ):
        Entity.__init__(self, **kwargs)
        self._set_obj_prop("attempt", attempt, t=ENTITY_TYPES["ATTEMPT"], req=True)
        self._set_str_prop("comment", comment)
        self._set_float_prop("maxResultScore", maxResultScore)
        self._set_float_prop("resultScore", resultScore)
        self._set_obj_prop("scoredBy", scoredBy, t=ENTITY_TYPES["AGENT"])

    @property
    def attempt(self):
        return self._get_prop("attempt")

    @property
    def comment(self):
        return self._get_prop("comment")

    @property
    def maxResultScore(self):
        return self._get_prop("maxResultScore")

    @property
    def resultScore(self):
        return self._get_prop("resultScore")

    @property
    def scoredBy(self):
        return self._get_prop("scoredBy")


class Score(Entity):
    def __init__(
        self,
        attempt=None,
        comment=None,
        maxScore=None,
        scoreGiven=None,
        scoredBy=None,
        **kwargs
    ):
        Entity.__init__(self, **kwargs)
        self._set_obj_prop("attempt", attempt, t=ENTITY_TYPES["ATTEMPT"], req=True)
        self._set_str_prop("comment", comment)
        self._set_float_prop("maxScore", maxScore)
        self._set_float_prop("scoreGiven", scoreGiven)
        self._set_obj_prop("scoredBy", scoredBy, t=ENTITY_TYPES["AGENT"])

    @property
    def attempt(self):
        return self._get_prop("attempt")

    @property
    def comment(self):
        return self._get_prop("comment")

    @property
    def maxScore(self):
        return self._get_prop("maxScore")

    @property
    def scoreGiven(self):
        return self._get_prop("scoreGiven")

    @property
    def scoredBy(self):
        return self._get_prop("scoredBy")


# Search entities
class Query(Entity):
    def __init__(self, creator=None, searchTarget=None, searchTerms=None, **kwargs):
        Entity.__init__(self, **kwargs)
        self._set_obj_prop("creator", creator, t=ENTITY_TYPES["PERSON"])
        self._set_obj_prop("searchTarget", searchTarget, t=ENTITY_TYPES["ENTITY"])
        self._set_str_prop("searchTerms", searchTerms)

    @property
    def creator(self):
        return self._get_prop("creator")

    @property
    def searchTarget(self):
        return self._get_prop("searchTarget")

    @property
    def searchTerms(self):
        return self._get_prop("searchTerms")


class SearchResponse(Entity):
    def __init__(
        self,
        searchProvider=None,
        searchTarget=None,
        query=None,
        searchResultsItemCount=None,
        **kwargs
    ):
        Entity.__init__(self, **kwargs)
        self._set_obj_prop(
            "searchProvider", searchProvider, t=ENTITY_TYPES["SOFTWARE_APPLICATION"]
        )
        self._set_obj_prop("searchTarget", searchTarget, t=ENTITY_TYPES["ENTITY"])
        self._set_obj_prop("query", query, t=ENTITY_TYPES["QUERY"])
        self._set_int_prop("searchResultsItemCount", searchResultsItemCount)

    @property
    def searchProvider(self):
        return self._get_prop("searchProvider")

    @property
    def searchTarget(self):
        return self._get_prop("searchTarget")

    @property
    def query(self):
        return self._get_prop("query")

    @property
    def searchResultsItemCount(self):
        return self._get_prop("searchResultsItemCount")

    @searchResultsItemCount.setter
    def searchResultsItemCount(self, new_count):
        self._set_int_prop("searchResultsItemCount", new_count)


# Session entities
class Session(Entity):
    def __init__(
        self,
        client=None,
        duration=None,
        endedAtTime=None,
        startedAtTime=None,
        user=None,
        **kwargs
    ):
        Entity.__init__(self, **kwargs)
        self._set_obj_prop("client", client, t=ENTITY_TYPES["SOFTWARE_APPLICATION"])
        self._set_duration_prop("duration", duration)
        self._set_datetime_prop("endedAtTime", endedAtTime)
        self._set_datetime_prop("startedAtTime", startedAtTime)
        self._set_obj_prop("user", user, t=ENTITY_TYPES["PERSON"])

    @property
    def client(self):
        return self._get_prop("client")

    @property
    def duration(self):
        return self._get_prop("duration")

    @duration.setter
    def duration(self, new_duration):
        self._set_duration_prop("duration", new_duration)

    @property
    def endedAtTime(self):
        return self._get_prop("endedAtTime")

    @endedAtTime.setter
    def endedAtTime(self, new_time):
        self._set_datetime_prop("endedAtTime", new_time)

    @property
    def startedAtTime(self):
        return self._get_prop("startedAtTime")

    @property
    def user(self):
        return self._get_prop("user")


class LtiSession(Session):
    def __init__(self, messageParameters=None, **kwargs):
        Session.__init__(self, **kwargs)
        self._set_dict_prop("messageParameters", messageParameters)

    @property
    def messageParameters(self):
        return self._get_prop("messageParameters")
