"""
pyAirlock: Python library for Airlock products

Copyright (c) 2019-2024 Urs Zurbuchen <info@airlock.com>

Airlock, a subsidiary of Ergon Informatik, provides security products
to protect web applications and APIs against all sorts of attacks.

* [Airlock Gateway](https://www.airlock.com/en/secure-access-hub/components/gateway)
  Airlock Gateway is a web application firewall (WAF) and protects mission-critical,
  web-based applications and APIs from attacks and undesired visitors.
  As a central security instance, it examines every HTTP(S) request for attacks and
  thus blocks any attempt at data theft and manipulation.
* [Airlock Microgateway](https://www.airlock.com/en/secure-access-hub/components/microgateway)
  Airlock Microgateway protects APIs and microservices from attacks and unauthorized
  access while they are running. Being specifically designed for use in Kubernetes
  environments, it is placed close to the protected services.
* [Airlock IAM](https://www.airlock.com/en/secure-access-hub/components/iam)
  Airlock IAM is a customer identity and access management (cIAM) solution guaranteeing
  absolutely secure and efficient access procedures for web applications.
  offers centralised identity management and organisation of access permissions,
  for applications and APIs, alike.
  Integrated applications can be bundled as a single sign-on (SSO) group.

Airlock Gateway and Airlock IAM, being stand-alone, centrally installed services, both
provide REST APIs to integrate third-party or customer-specific tools.
These APIs are all documented [here](https://docs.airlock.com).

pyAirlock is a Python library wrapping these REST APIs and allowing system administrators
easier access.

- [Gateway](gateway/index.html)
    - configuration REST API, providing access to configuration objects, virtual hosts, mappings etc.
- [IAM](iam/index.html) (not yet implemented)
    - Loginapp flows for authentication, registration and self-services
    - Transaction approval flows
    - Adminapp for user and token management
- [Common](common/index.html)
    - Shared library functions such as reading config files, logging etc.


Airlock Microgateway, by the way, is tightly integrated with Kubernetes.
Configuration, for example, is specified through [custom resource definitions](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/),
expressed as YAML manifests. They are created and maintained using the standard Kubernetes APIs.
"""
