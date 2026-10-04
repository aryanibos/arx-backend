# TypeScript Standard

Use this reference for TypeScript implementation and review.

## Compiler posture

Prefer strict compiler settings when the project can support them, including:

- `strict`
- `noUncheckedIndexedAccess`
- `exactOptionalPropertyTypes`
- `noImplicitReturns`
- `noFallthroughCasesInSwitch`

Do not weaken compiler settings merely to make a change pass.

## Typing rules

- Avoid `any`. Use `unknown` and narrow safely.
- If third-party interoperability makes `any` unavoidable, keep it at the boundary, minimize its scope, and document why.
- Do not use `@ts-ignore`.
- Use `@ts-expect-error` only for intentional, explained type-level cases.
- Prefer explicit return types for exported functions.
- Prefer `type` by default; use `interface` when extension or declaration merging is intentional.
- Avoid TypeScript `enum`; prefer literal unions or schema-backed enums when appropriate.
- Use `import type` where it improves clarity and emitted-code behavior.
- Avoid unsafe casts and non-null assertions unless the invariant is established and local.
- Remove dead code and stale compatibility branches.

Use English for technical identifiers unless the project explicitly uses another convention.

## Schema-derived types

Prefer deriving types from validated schemas when it prevents duplicated definitions and drift. Do not force a schema library into internal-only types that do not cross a trust boundary.

## Dependency discipline

Before adding a dependency:

1. check whether the runtime or project already provides the capability
2. confirm runtime/version compatibility
3. assess maintenance and security posture
4. avoid dependencies for trivial utilities
5. prefer already-approved project libraries
6. update the lockfile intentionally

For fast-moving or version-sensitive APIs, consult current official documentation when available.
