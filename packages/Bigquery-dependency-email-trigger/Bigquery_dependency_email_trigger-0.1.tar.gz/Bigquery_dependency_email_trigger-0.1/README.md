Bigquery_dependency_email_trigger is a Python library that monitors the results of a BigQuery dependency query and sends email notifications based on the outcome. It is designed to help users automate and manage dependency checks and receive alerts via email.

Features
1. Monitors BigQuery dependency query results.
2. Sends warning emails if the expected result is not met within a specified number of tries.
3. Sends error emails if the maximum number of tries is exceeded without meeting the expected result.
4. Configurable retry intervals and email contents.


**Installation**

Install the library using pip:

```Bash
pip install bigquery-dependency-email-trigger
```

Usage
Here's an example of how to use the bigquery_dependency_email_trigger function:

```Python
import time
import pandas_gbq
from bigquery_dependency_email_trigger import bigquery_dependency_email_trigger

# Set up parameters
dependency_query = "SELECT COUNT(*) FROM `project.dataset.table` WHERE condition"
project = "your-gcp-project-id"
expected_dependent_result = "expected-result"
number_of_tries = 10
num_of_tries_before_warn_email = 5
time_interval = 60  # Time interval in seconds
warn_email_content = "Warning: Dependency check not met"
warn_email_subject = "Warning: Dependency Check"
email_address = "recipient@example.com"
error_email_content = "Error: Dependency check failed"
error_email_subject = "Error: Dependency Check Failed"
SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 587
SENDER_EMAIL = "sender@example.com"
SMTP_USER = "smtp-user"
SMTP_PASSWORD = "smtp-password"

# Trigger dependency check
result = bigquery_dependency_email_trigger(
    dependency_query, project, expected_dependent_result,
    number_of_tries, num_of_tries_before_warn_email, time_interval,
    warn_email_content, warn_email_subject, email_address, error_email_content, error_email_subject,
    SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SMTP_USER, SMTP_PASSWORD
)

if result:
    print("Dependency met successfully.")
else:
    print("Dependency check failed.")

```



*Parameters:*

1. dependency_query: SQL query to run on BigQuery to check for dependency.
2. project: GCP project ID.
3. expected_dependent_result: Expected result of the dependency query.
4. number_of_tries: Number of times to retry the query.
5. num_of_tries_before_warn_email: Number of tries before sending a warning email.
6. time_interval: Time interval between retries (in seconds).
7. warn_email_content: Content of the warning email.
8. warn_email_subject: Subject of the warning email.
9. email_address: Recipient email address.
10. error_email_content: Content of the error email.
11. error_email_subject: Subject of the error email.
12. SMTP_SERVER: SMTP server address.
13. SMTP_PORT: SMTP server port.
14. SENDER_EMAIL: Sender email address.
15. SMTP_USER: SMTP server user.
16. SMTP_PASSWORD: SMTP server password.


