# O365 CIS SCAN

The Python based O365 CIS Scan helps to identify the O365 resources that are non-compliant with the controls specified in CIS Benchmarks version 1.3


## **Steps**

1. Zip all the dependencies along with the .py files and configure the environment variables and IAM permissions as specified in the AWS Lambda Functions Section and upload to AWS Lambda.

## **AWS Services Used**

1. AWS Lambda – Two lambda functions named request function and scan function, are used where request function is used to validate the credentials provided, check if the required permissions are given and upon validations invokes the scan function which performs the actual CIS scan on your AWS infrastructure and sends the report to the specified email id.
1. Amazon DynamoDB – The DynamoDB table contains information like scan status for the associated request id.
1. Amazon SES – Amazon SES is configured to send the generated reports to the user on the provided email.

## **AWS Lambda Functions**

### A. **Lambda Request Function:** 

This function performs validation on the input and invokes the “Lambda Scan Function” upon successful validation.

This function includes request.py, session.py files in the package along with the required dependencies.zip all the files and upload to AWS lambda.

#### **IAM Role Permissions for Lambda Request Function:**

The Lambda Request Function should have permission to invoke Lambda Scan Function, assume role permissions to assume any user provided roles, DynamoDB permissions to access tables, along with the default lambda permissions.

#### **File Info:**

1) **request.py:** The request function is used to validate the credentials provided, check if the required permissions are given to run the scan.


The Environment variables to be configured at Lambda Request Function are as follows

|**Environment Variable Name**|**Description**|
| :-: | :-: |
|DB\_TABLE\_NAME|DynamoDB table name|



### B. **Lambda Scan Function:**

This function performs the actual CIS scan and sends the report to the user email using the configured SMTP credentials and saves the can status to DynamoDB.

This function includes lambda_function.py, mailer.py, o365_cis_db.py files in the package along with the required dependencies. zip all the files and upload to AWS lambda.

#### **IAM Role Permissions for Lambda Scan Function:**

The Lambda Scan Function should have assume role permissions to assume any user provided roles, DynamoDB permissions to access tables, along with the default lambda permissions.

#### **File Info:**

1) **lambda_function.py:** The scan file has the functions that performs the actual CIS scan on your O365 infrastructure and sends the generated report to the specified email id.
2) **o365_cis_db.py:** This file contains the functions that perform database operations.
4) **mailer.py:** This file contains the functions that sends the report to user specified email

The Environment variables to be configured at Lambda Scan Function are as follows


|**Environment Variable Name**|**Description**|
| :-: | :-: |
|DB\_TABLE\_NAME|DynamoDB table name|
|MAIL\_USERNAME|Email UserName|
|MAIL\_PASSWORD|Email Password|
|MAIL\_PORT|Email Port (for eg: 587)|
|MAIL\_SERVER|SMTP Email Server (for eg: email-smtp.us-east-1.amazonaws.com)|
|MAIL\_USE\_SSL|to use SSL for communication (value can be True/False)|
|MAIL\_USE\_TLS|to use SSL for communication (value can be True/False)|
|TEMP\_PATH|temporary path to be used by lambda (eg : /tmp/)|
|USE\_RATE\_LIMITER|False/True|
|FROM\_ADDR|Sender Email Address|

### **Input Format for Lambda Functions:**

#### 1. **Lambda Request Function Input Format:**

The Lambda Request Function can be executed by providing the required O365 credentials in Client Id, Client Secret and Tenant ID format using the lambda event object. 

##### 1. The Input format using Client Id, Client Secret and Tenant ID:

```json
{
  "body": {
    "requestId": "unique_scan_value",
    "scan_input": [
      {
        "access_type": "credentials",
        "access_input": {
          "client_id": "",
          "client_secret": "",
          "tenant_id":""
        }
      }
    ],
    "email": "<user-email> "
  }
}


```
#### 2. **Lambda Scan Function Input Format**

By default, the Lambda Scan Function is invoked by Lambda Request Function, but in cases where the Lambda Scan Function must be executed then the input format is as follows:

##### 1. The Input format using access key and secret key:
```json
{
    "requestId": "unique_scan_value",
        "access_type": "credentials",
        "access_input": {
          "client_id": "<client id>",
          "client_secret": "<client secret>",
          "tenant_id":"<tenant id>"
        },
    "email": "<user-email> "
  }
```

#### Steps to Create Client Id, Client Secret and Tenant ID:
#### Instructions:

#### **Step-1: Register your App**
1.	Sign in to the [Microsoft Admin portal](https://admin.microsoft.com/)
2.	On the left side of, menu Click on Show All
3.	now click on Azure Active Directory Which will redirect you to the Azure Active Directory Admin Center portal
4.	In Azure Active Directory Admin Center in the left side menu in the favorites, tab Click on Azure Active Directory
5.	In the Azure Active Directory sub-menu search for App Registration
6.	Now click on New Registrations
7.	Name the App and click on Register.
8.	Your App has been successfully registered
9.	For detailed information [Click Here](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app#register-an-application).
10.	Now move to the next step to generate Client Id/Client Secret/Tenant Id.
#### **Step-2: Generating App Credentials**
1)	Now In the sub-menu search for Credentials and Secrets, Now go to the Client Secret tab
2)	Now, click on New Client Secret
3)	Give the required description and select 24 months for expired field
**Note: "these details cannot be edited further so recheck your given details".**
4)	Click on Add to generate client secret.
5)	Once the Client Secret is generated. copy the value and save the value.
**Note: Copy and save the Client Secret immediately, as "Client secret values cannot be viewed, except for immediately after creation. Be sure to save the secret when created before leaving the page."**
6)	Now in the sub menu search for Overview, copy Client Id & Tenant Id from the essentials Sections.
7)	For detailed information [Click Here](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app#add-credentials).
8)	Now move to the next step to Set App Permissions.
#### **Step-3: Set App Permissions**
1)	In the sub-menu search for API Permissions, Check for Configured Permissions tab
2)	Now, click on Add a Permissions, Select Microsoft Graph --> Application Permissions
3)	Search for Basic Permissions:
          a)	Directory.Read.All
          b)	Domain.Read.All
          c)	IdentityRiskEvent.Read.All
          d)	Policy.Read.All
          e)	SecurityEvents.Read.All
          f)	User.Read.All
4)	Check the Permissions and click on Add Permissions.
5)	Once All the Permissions are added, Click on Grant admin consent and click on Yes
6)	For detailed information [Click Here](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-configure-app-access-web-apis#application-permission-to-microsoft-graph).
7)	Now your account is ready for scan.

