import time
import pandas_gbq
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib



def bigquery_dependency_email_trigger(dependency_query, project, expected_dependent_result,
                          number_of_tries, num_of_tries_before_warn_email, time_interval,
                          warn_email_content, warn_email_subject, email_address, error_email_content, error_email_subject,
                          SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SMTP_USER, SMTP_PASSWORD):
    
    """
    This function checks the result of a BigQuery dependency query and sends email notifications 
    based on the outcome.

    Parameters:
    - dependency_query: SQL query to run on BigQuery to check for dependency.
    - project: GCP project ID.
    - expected_dependent_result: Expected result of the dependency query.
    - number_of_tries: Number of times to retry the query.
    - num_of_tries_before_warn_email: Number of tries before sending a warning email.
    - time_interval: Time interval between retries.
    - warn_email_content: Content of the warning email.
    - warn_email_subject: Subject of the warning email.
    - email_address: Recipient email address.
    - error_email_content: Content of the error email.
    - error_email_subject: Subject of the error email.
    - SMTP_SERVER: SMTP server address.
    - SMTP_PORT: SMTP server port.
    - SENDER_EMAIL: Sender email address.
    - SMTP_USER: SMTP server user.
    - SMTP_PASSWORD: SMTP server password.
    """
    wait_period = 0  # Initialize wait period
    tries = 1  # Initialize tries counter
    tries_before_warn_email = 1  # Initialize tries before warning email counter
    dependency_result = False  # Initialize dependency result
    
    while tries <= int(number_of_tries):   # Loop until number of tries is exceeded

        print("Try Number : ", tries)

        if dependency_query != 'None':   # Check if there is a dependency query
            df = pandas_gbq.read_gbq(dependency_query, project_id=project)   # Execute the query
            print("Dependency Query ->",dependency_query)
            print("Dependency Query Result ->",df.iloc[0,0])
            dependency_result = str(df.iloc[0,0]).casefold()    # Get the query result
        
        expected_dependent_result = str(expected_dependent_result).casefold()   # Normalize the expected result

        tries = tries + 1   # Increment tries

        if dependency_result != expected_dependent_result:     # Check if result matches expected result        
            
            ### wait before sending warn email
            if tries_before_warn_email <= int(num_of_tries_before_warn_email):  # Check if warning email should be sent
                time.sleep(int(time_interval))      # Wait for the specified time interval
                wait_period = wait_period + int(time_interval)   # Increment wait period
                tries_before_warn_email = tries_before_warn_email + 1   # Increment tries before warning email counter
                continue
            
            tries_before_warn_email = 1     # Reset tries before warning email counter
            print("Wait Duration : ", wait_period, " seconds.")
            
            # Prepare and send the warning email
            email_content = warn_email_content + ', since ' + str(int(wait_period/60)) + ' minutes.'
            send_email(email_address, SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SMTP_USER, SMTP_PASSWORD, warn_email_subject, email_content)
            print("Sent warning email")

            time.sleep(int(time_interval))      # Wait for the specified time interval
            wait_period = wait_period + int(time_interval)    # Increment wait period
            continue

        else:
            print("Dependency has been completed.")
            tries = 1
            return True     # Return True if dependency is completed
            

    if tries > int(number_of_tries):    # Check if number of tries is exceeded
        print("Number of tries : ", tries)
        email_content = error_email_content     # Prepare error email content
        send_email(email_address, SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SMTP_USER, SMTP_PASSWORD, error_email_subject, email_content)

        print('Number of tries for the expected result from Bigquery has exceeded. Sent an error email.')
        return False    # Return False if the dependency is not completed

def send_email(RECIPIENT_EMAIL, SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SMTP_USER, SMTP_PASSWORD, EMAIL_SUBJECT, EMAIL_BODY, ATTACHMENT_FILENAME = None, csv_content = None):

    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = EMAIL_SUBJECT
    
    # Attach the body with the msg instance
    msg.attach(MIMEText(EMAIL_BODY, 'plain'))
    
    # Create a MIMEBase instance for the attachment
    part = MIMEBase('application', 'octet-stream')
    if csv_content != None:
        part.set_payload(csv_content)
        encoders.encode_base64(part)
    if ATTACHMENT_FILENAME != None:
        part.add_header('Content-Disposition', f'attachment; filename={ATTACHMENT_FILENAME}')
        # Attach the attachment to the MIMEMultipart object
        msg.attach(part)
    
    # Send the email using the SMTP server
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(msg['From'], msg['To'], msg.as_string())
            print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

