# Administrator guide (MVP)

## Organisation administrators (owner or admin role)

* **Enable MFA first** (Administration → MFA). Adding or changing members requires a session opened with an MFA code.
* **Members.** The person must have an account. Add them by email with the role viewer, analyst or admin:

  | Role | Can do |
  |---|---|
  | viewer | Read |
  | analyst | Create and edit projects, inputs and runs |
  | admin | Also delete projects, read the audit log and manage members |
  | owner | Created at registration |

* **Audit log.** The log of registration, login, project and input changes, runs and generated documents. It is append-only.

## Platform administrators

* **Create the account** with `python -m app.seed superadmin`, using `A360_ADMIN_EMAIL` and `A360_ADMIN_PASSWORD`. Enable MFA at first login; administrative endpoints refuse sessions without MFA.
* **Accreditation.** Organisations registered as "accredited" appear as *pending*. Verify or reject them after checking their documents outside the platform, and record the reason in the note.
* **Demo workspace.** `python -m app.seed demo` (set `A360_DEMO_PASSWORD`, or note the generated password printed once).

## Data governance

* **Tenant isolation.** Tenant data is isolated at the API (membership checks) and in PostgreSQL (row-level security, forced, through a non-owner role).
* **Exports and deletion.** An organisation's data can be exported or deleted with SQL by `org_id`. A self-service workflow is on the roadmap.
* **Retention, privacy notice and consent text.** These must be drafted for the incorporation jurisdiction before commercial launch.
