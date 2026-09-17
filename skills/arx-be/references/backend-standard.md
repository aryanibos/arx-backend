# Backend Standard

Use this reference for backend module design and implementation review.

## Default Direction

Prefer:

`Route -> Handler -> Service -> Repository`

when the project architecture uses layered REST modules.

Do not introduce this structure mechanically into projects that already have another approved architecture.

## Route
Own HTTP registration and middleware composition.

## Handler
Own HTTP translation:
- params/query/body parsing
- validation
- call service
- status/envelope mapping

No direct DB query.

## Service
Own:
- business rules
- orchestration
- transaction boundary
- repository/infrastructure coordination

No Hono Context or raw Response.

## Repository
Own persistence and database queries.

No:
- HTTP
- business decisions
- authorization policy
- user-facing messages

## Cross-module Calls
Prefer explicit exported services/ports. Do not import another module's private repository or handler.

## Review Questions
- Is business logic in the service/application layer?
- Is HTTP isolated from business logic?
- Are transaction boundaries explicit?
- Are external failures handled?
- Is the change smaller than necessary?
- Did the implementation create a new pattern without need?
