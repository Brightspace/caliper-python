# Change history

## 1.2.0

- Revise Entities and Events to align with 1.2 final spec draft.

  *1.2.0.5*. Bug fix for [Issue #222](https://github.com/IMSGlobal/caliper-python/issues/222).

  *1.2.0.4*. Add test support for Python 3.9.

  *1.2.0.3*. Bug fixes with [PR #220](https://github.com/IMSGlobal/caliper-python/pull/220).

  *1.2.0.2*. Addition of other valid LTI Message types to the explicit list of valid messages:
             legacy 1.0/1.1 LTI basic launch; legacy Content Item/Deep Linking 1.0 messages

  *1.2.0.1*. Small code refactor to get Flake8 tests to run clean,
             Align Caliper Entity property required status to align with 1.2 final spec draft,
             Caliper Event.Object property explicitly required


- Supports IMS Caliper specification 1.2.

- Add support for user-agent type information within SoftwareApplication entities, and add new
  optional `client` field in Session entities.

- Simplify implementation by removing marker types, LearningContext entity, as not in the Caliper
  specification.

- Drops support for Python2

- Corrects broken lists of Caliper Roles, Caliper Metrics, Caliper System Identifier Types for
  proper alignment with the 1.2 specification



## 1.1.10

- Add in support for the Feedback metric profile.

  *1.1.10.1*. Bug fix for [Issue #162](https://github.com/IMSGlobal/caliper-python/issues/162).

  *1.1.10.2*. Bug fix for [Issue #168](https://github.com/IMSGlobal/caliper-python/issues/168).

  *1.1.10.3*. Bug fix for [Issue #170](https://github.com/IMSGlobal/caliper-python/issues/170).

  *1.1.10.4*. Bug fix for [Issue #167](https://github.com/IMSGlobal/caliper-python/issues/167).

  *1.1.10.5*. Bug fix for [Issue #176](https://github.com/IMSGlobal/caliper-python/issues/176).

  *1.1.10.6*. Bug fix for [Issue #187](https://github.com/IMSGlobal/caliper-python/issues/187),
              Bug fix for [Issue #183](https://github.com/IMSGlobal/caliper-python/issues/185),
              Bug fix for [Issue #183](https://github.com/IMSGlobal/caliper-python/issues/183),
              Bug fix for [Issue #181](https://github.com/IMSGlobal/caliper-python/issues/181).


## 1.1.9

- Ensure that all Events and Entities have appropriate properties available for
  their expected fields.

  *1.1.9.1*. Bug fix for [Issue #147](https://github.com/IMSGlobal/caliper-python/issues/147).


## 1.1.8

- Provide a SimpleSensor that reduces complexity for most straightforward use
  of the reference implementation: the simple sensor has only the `send()`
  method, used to send both Caliper Entities and Events, and supports only a
  single `HttpRequestor` transport connection to a single configured endpoint.


## 1.1.7

- Add in support for the Research Management metric profile.


## 1.1.6

- No need any longer to import with_metaclass from future.utils, so pruned.


## 1.1.5

- Future package at 0.17.0 has problems when pip attempts to install for both
  Py2 and Py3 local environments; configure tox to enforce no-cache-dir for pip
  when building virtual envs for tests.


## 1.1.4

- Cope with deprecations in dependencies: rfc3986.api.is_valid_uri(s) now
  deprecated in favour of using rfc3986.validators.Validator class; collections
  ABCs no longer loadable from root module in 3.7+, should be loaded from
  collections.abc instead.


## 1.1.3

- Add in a debug option for sensor clients to capture HTTP response objects for
  later inspection.


## 1.1.2

- Fix bug in HttpRequestor in which it could send a malformed HTTP header when
  the requestor's bound HttpOptions had no auth scheme specified


## 1.1.1

- Revise test utility code for new arrangement of fixtures repository
- Revise package constants (including actions, events) for better profile-based
  context handling, including support for the new profile-specific context
  documents
- Export CALIPER_VERSION as top-level package property
- Refactor context examination so that the Caliper Basic profile's context is
  always a valid base for the other, known Caliper profile contexts
- Refactor to move profile/event/action verification into the BaseEvent class,
  and ensure it properly produces the right exception description string on
  unknown actions passed in
- Re-order tox's building of virtual environments to avoid dependency problems
  with pytest/funcsigs
- Improve on cleanliness of test erroring on fixtures not rebuildable as
  Caliper things
- Improve condensor to support more strict context checking
- Add CONTRIBUTING and HISTORY files to package


## 1.1.0

- Supports IMS Caliper specification 1.1.

  *1.1.0.1*. Bug fix for [Issue #147](https://github.com/IMSGlobal/caliper-python/issues/147>).

  *1.1.0.2*. Update of packaging and test framework for CI.


## 1.0.0

- Supports IMS Caliper specification 1.0
