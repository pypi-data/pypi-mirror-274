import json

SYSTEM_INSTRUCTION = "In this environment you have access to a set of functions defined in the JSON format you can use to address user's requests, use them if needed."


def _check_functions_def(functions_def):
    """Check if the functions definition is valid."""

    for function in functions_def:
        if 'name' not in function:
            raise 'Function name must be provided'
        if 'description' not in function:
            raise 'Function description must be provided'
        if 'parameters' not in function:
            raise 'Function parameters must be provided'

        parameters = function['parameters']
        if 'type' not in parameters:
            raise 'Function parameters type must be provided'
        if parameters['type'] != 'object':
            raise 'Function parameters type must be object'
        if 'properties' not in parameters:
            raise 'Function parameters properties must be provided'

        properties = parameters['properties']
        if not isinstance(properties, dict):
            raise 'Function parameters properties must be an object'
        if 'required' in parameters and not isinstance(parameters['required'], list):
            raise 'Function parameters required must be an array'


def _check_messages(messages):
    """Check if the messages are valid."""
    if len(messages) == 0:
        raise 'Messages cannot be empty'

    first_message = messages[0]
    if first_message['role'] == 'system':
        messages = messages[1:]

    if len(messages) == 0:
        raise 'At least user message must be provided'

    for (index, message) in enumerate(messages):
        print(message['role'])
        if 'role' not in message or message['role'] not in ['user', 'assistant', 'tool']:
            raise Exception('Invalid role')

        print(index)
        print(message['role'])
        if (index % 2 == 0 and message['role'] not in ['user', 'tool']) or (index % 2 == 1 and message['role'] != 'assistant'):
            raise Exception(
                'Conversation roles must alternate (user/tool) and assistant...')

        if message['role'] == 'tool':
            if 'content' not in message:
                raise Exception(
                    '"content" must be provided for message with role "tool"')
            if not isinstance(message['content'], list):
                raise Exception(
                    '"content" must be a list for message with role "tool"')

            for function_response in message['content']:
                if not isinstance(function_response, dict):
                    raise Exception('Function response must be an object')
                if 'tool_call_id' not in function_response:
                    raise Exception(
                        '"tool_call_id" must be provided for function response')
                if 'value' not in function_response:
                    raise Exception(
                        '"value" must be provided for function response')
        elif message['role'] == 'user':
            if 'content' not in message:
                raise Exception(
                    '"content" must be provided for message with role "user"')
        elif message['role'] == 'assistant':
            if 'content' not in message and 'tool_calls' not in message:
                raise Exception(
                    'Either "content" or "tool_calls" must be provided message with role "assistant"')

            if 'tool_calls' in message:
                tool_calls = message['tool_calls']
                if not isinstance(tool_calls, list):
                    raise Exception('Tool calls must be an array')
                for tool_call in tool_calls:
                    if not isinstance(tool_call, dict):
                        raise Exception('Tool call must be an object')
                    if 'name' not in tool_call:
                        raise Exception(
                            '"name" must be provided for tool call')
                    if 'arguments' not in tool_call:
                        raise Exception(
                            '"arguments" must be provided for tool call')


def prompt_messages(messages, functions_def):
    _check_messages(messages)
    _check_functions_def(functions_def)

    system_instruction = SYSTEM_INSTRUCTION
    first_user_message = messages[0]
    starting_index = 1
    if messages[0]['role'] == 'system':
        system_instruction = messages[0]['content']
        first_user_message = messages[1]
        starting_index = 2

    prompted_messages = [{'role': 'user', 'content': (
        system_instruction
        + "\n"
        + "Functions: "
        + json.dumps(functions_def, indent=2, ensure_ascii=False)
        + "\n\n"
        + " <u>"
        + first_user_message['content']
    )}]

    for message in messages[starting_index:]:
        if message['role'] == 'tool':
            prompted_messages.append({
                'role': 'user',
                'content': '<r>' + json.dumps({'value': message['content'], 'tool_call_id': 'xxx'}, indent=2, ensure_ascii=True)
            })
        elif message['role'] == 'user':
            prompted_messages.append({
                'role': 'user',
                'content': '<u>' + message['content']
            })
        elif message['role'] == 'assistant':
            if 'content' in message and len(message['content']) > 0:
                prompted_messages.append({
                    'role': 'assistant',
                    'content': '<c>' + message['content']
                })
            else:
                prompted_messages.append({
                    'role': 'assistant', 'content': '<f>' + json.dumps(message['tool_calls'], indent=2, ensure_ascii=False)
                })

    return prompted_messages
