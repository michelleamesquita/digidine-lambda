import boto3
import json

def lambda_handler(event, context):
    # Cognito client
    client = boto3.client('cognito-idp')
    user_pool_id = "us-east-2_oywao8wNQ"

    # Extrair CPF dos pathParameters do evento
    target_cpf = event.get('cpf')

    if not target_cpf:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "CPF is required"})
        }

    try:
        # Listar todos os usuários no User Pool
        response = client.list_users(UserPoolId=user_pool_id)
        users = response.get('Users', [])

        # Filtrar por custom:cpf
        matching_users = []
        for user in users:
            cpf_attribute = next((attr for attr in user['Attributes'] if attr['Name'] == 'custom:cpf'), None)
            if cpf_attribute and cpf_attribute['Value'] == target_cpf:
                matching_users.append({"Authorized": True})

        if not matching_users:
            return {
                "statusCode": 404,
                "body": json.dumps({"message": "No users found with the provided CPF."})
            }

        return {
            "statusCode": 200,
            "body": json.dumps({"message": matching_users[0]})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
