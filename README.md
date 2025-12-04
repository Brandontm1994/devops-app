# Salesforce auto testing tool

A small CLI for running Apex tests in a Salesforce org using the Tooling API. The tool handles
OAuth login via environment variables, locates Apex classes, enqueues tests, and reports results
as JSON.

## Prerequisites

- Python 3.10+
- A Salesforce connected app configured for the username-password OAuth flow with the necessary
  permissions to run Apex tests.
- A Security Token for the user you plan to authenticate as.

## Setup

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Copy the example configuration so you can edit it without committing secrets:

   ```bash
   cp example_config.yaml my_config.yaml
   ```

3. Export the required Salesforce credentials. The config references these variables by name to
   keep secrets out of your YAML file:

   ```bash
   export SALESFORCE_CLIENT_ID="<connected-app-client-id>"
   export SALESFORCE_CLIENT_SECRET="<connected-app-client-secret>"
   export SALESFORCE_USERNAME="<username>"
   export SALESFORCE_PASSWORD="<password>"
   export SALESFORCE_SECURITY_TOKEN="<security-token>"
   ```

4. Update `my_config.yaml` with the test classes you want to run. The `classes` list controls which
   Apex test classes are executed. Set `synchronous: true` to run tests without queueing, or leave
   it `false` to queue and poll.

```yaml
auth:
  client_id_env: SALESFORCE_CLIENT_ID
  client_secret_env: SALESFORCE_CLIENT_SECRET
  username_env: SALESFORCE_USERNAME
  password_env: SALESFORCE_PASSWORD
  security_token_env: SALESFORCE_SECURITY_TOKEN
  domain: login

test_plan:
  classes:
    - ExampleTestClass
  synchronous: false
  api_version: "58.0"
  timeout_seconds: 300
```

## Usage

Run the CLI with your configuration file. Results are printed to stdout unless `--output` is
provided.

```bash
python -m salesforce_autotest my_config.yaml --output results.json
```

Exit codes:

- `0` — Tests completed with all passing results.
- `1` — Configuration or API error encountered.
- `2` — Tests ran but one or more outcomes failed.

### Common issues

- **Missing env vars**: If an environment variable referenced in the config is not set, the tool
  will exit with an error that names the variable. Confirm it is exported in your shell before
  running the CLI.
- **Bad config shape**: The CLI requires `auth` and `test_plan` sections. If the YAML parses to
  another structure (like a list) or the sections are missing, the tool will exit with a
  descriptive configuration error.
- **Class not found**: The runner will fail fast if any class in `test_plan.classes` cannot be
  located in the org. Double-check the class name matches exactly and that it is in the namespace
  accessible to the authenticated user.
- **Timeouts**: Increase `timeout_seconds` if the org is under heavy load and asynchronous tests do
  not complete within the default window.
