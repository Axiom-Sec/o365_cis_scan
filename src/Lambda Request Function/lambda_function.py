import boto3
import json
import requests
import jwt


roles = ['Directory.Read.All','Domain.Read.All','IdentityRiskEvent.Read.All','Policy.Read.All','SecurityEvents.Read.All']
def get_accesstoken(client_id, client_secret, tenant_id):
    try:
        headers = {"ContentType": "application/x-www-form-urlencoded"}
        resource_id = "https://graph.microsoft.com"
        Body = {
            "client_id": client_id,
            "client_secret": client_secret,
            "RedirectUri": "",
            "grant_type": "client_credentials",
            "TenantId": tenant_id,
            "resource": resource_id
        }
        TenantId = tenant_id
        URL = "https://login.microsoftonline.com/"+TenantId+"/oauth2/token"
        response = requests.post(URL, data=Body, headers=headers)
        output = json.loads(response.text)
        if 'error' in output:
            return False
        else:
            return output
    except Exception as e:
        print(str(e))
        return False


def check_permission(token):
    try:
        
        # for the above statement use mapping template in integration request
        decodedAccessToken = jwt.decode(token, options={"verify_signature": False})
        accessTokenFormatted = json.dumps(decodedAccessToken, indent=2)
        # base64_bytes = jwt.decode("ascii")
        rolepermissions = decodedAccessToken["roles"]
        if len(roles) <= len(rolepermissions):
            for i in roles:
                count = 0
                for j in rolepermissions:
                    if str(i) == str(j):
                        break;
                    else:
                        count = count + 1
                        if len(rolepermissions) == count:
                            return False
        else:
            return False
        return True
    except Exception as e:
        print(str(e))
        return {
            'error': 'Cannot process the request'
        }



def o365_cis_scan_request_handler(event, context):

        lam = boto3.client('lambda')
        cis_scan_function = os.environ['CIS_Scan_LambdaFunction']
        try:
                
                    try:    
                        accounts = 0
                        user_input = []
                        reqid = event['body']['requestId']
                        
                        if len(event['body']['scan_input']) == 1:
                                accounts = 1
                        if accounts == 0:
                                return{
                                'error': 'Invalid Input'
                                }
                        for user_creds in event['body']['scan_input']:
                                client_id = user_creds['access_input']['client_id']
                                client_secret = user_creds['access_input']['client_secret']
                                tenant_id = user_creds['access_input']['tenant_id']
                                access_token = get_accesstoken(
                                client_id, client_secret, tenant_id)
                                if access_token:
                                        token = access_token['access_token']
                                        check_permission(token)
                                        if not check_permission(token):
                                            return{
                                                'error': 'Required Permissions are not attached.'
                                            }
                                else:
                                        return{
                                                'error': 'Invalid ClientId/ClientSecret/TenantID Provided.'
                                        }

                                user_input.append(user_creds)
                       
                        for input in user_input :
                                if 'access_type' in input and 'access_input' in input:
                                        if input['access_type'].lower() != "client_credentials" and input['access_type'].lower() !="crossaccount":
                                                return{
                                                        'error': 'Unknown Access Type' 
                                                }
                                        else:  
                                                lambda_input={
                                                "access_type": input['access_type'],
                                                "client_id":input['access_input']['client_id'],
                                                "client_secret":input['access_input']['client_secret'],
                                                "tenant_id":input['access_input']['tenant_id'],
                                                "requestId" : reqid,
                                                "access_token":token,
                                                "email":event['body']['email']
                                                }
                                                invoked = lam.invoke(FunctionName=cis_scan_function,InvocationType='Event',Payload=json.dumps(lambda_input))
                        
                        return {  
                                "requestId":reqid,
                                "status": "INPROGRESS"
                        }
                    except Exception as e:
                            print("Exception in O365 scan request ", str(e))
                            return{
                                    'error': 'Invalid Request Parameters'
                            }
                
        except Exception as e:
                print("Exception in O365 scan request : ",str(e))
                return {
                                'error': 'Invalid Request Parameters'
                }
if __name__ == '__main__':
        
        event =  {
    
    "body": {
    "requestId": "unique_scan_value1",
    "scan_input": [
      {
        "access_type": "client_credentials",
        "access_input": {
          "client_id": "",
          "client_secret": "",
          "tenant_id":""
        }
      }

    ],
    "email": "abc@gm.com"
  }
  
}
        
        o365_cis_scan_request_handler(event, "context")

        