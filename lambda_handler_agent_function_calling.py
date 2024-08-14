import json
import datetime

def lambda_handler(event, context):
    agent = event.get('agent', [])
    actionGroup = event.get('actionGroup', [])
    function = event.get('function', [])
    parameters = event.get('parameters', [])

    #Function to get the number of the current hours.
    def get_time():
        return datetime.datetime.utcnow().strftime('%H:%M:%S')
        
    #Function to add two numbers
    def add_two_numbers(number_1, number_2):
        return number_1 + number_2
        
    #Extracting values from parameters
    param_dict = {param['name'].lower(): int(param['value']) for param in parameters if param['type']=='number'}
    
    #Check the function name and execute the corresponding action
    if function == "add_two_numbers":
        #Safe extraction of number_1 and number_2 from parameters
        number_1 = param_dict.get('number_1')
        number_2 = param_dict.get('number_2')
        
        #Ensure both numbers are provided and are of the correct type
        if number_1 is not None and number_2 is not None:
            try:
                number_1 = int(number_1)
                number_2 = int(number_2)
                result = add_two_numbers(number_1, number_2)
                result_text = "The result of adding {} and {} is {}".format(number_1, number_2, result)
            except ValueError:
                result_text = "Error: Non-integer parameters."
        else:
            result_text = "Error: Missing one or more required parameters."
            
        responseBody = {
            "TEXT": {
                "body": result_text
            }
        }
    elif function == "get_time":
        result = get_time()
        result_text = "The time is {}".format(result)
        
        responseBody = {
            "TEXT": {
                "body": result_text
            }
        }
            
    else:
        responseBody = {
            "TEXT": {
                "body": "The function {} was called successfully".format(function)
            }
        }

    action_response = {
        'actionGroup': actionGroup,
        'function': function,
        'functionResponse': {
            'responseBody': responseBody
        }
    }
    
    dummy_function_response = {'response': action_response, 'messageVersion': event.get('messageVersion', [])}
    print("Response: {}".format(dummy_function_response))

    return dummy_function_response