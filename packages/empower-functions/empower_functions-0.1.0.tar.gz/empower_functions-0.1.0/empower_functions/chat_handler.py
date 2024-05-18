import json

from typing import Any, Dict, Iterator, List, Literal, Optional, Tuple, Union, Protocol, cast

import jinja2
from jinja2.sandbox import ImmutableSandboxedEnvironment

import llama_cpp.llama as llama
import llama_cpp.llama_types as llama_types
from llama_cpp.llama_chat_format import LlamaChatCompletionHandler

class EmpowerFunctionsCompletionHandler(LlamaChatCompletionHandler):
    SYSTEM_INSTRUCTION = "In this environment you have access to a set of functions defined in the JSON format you can use to address user's requests, use them if needed."

    def _check_functions_def(self, functions_def: Optional[List[llama_types.ChatCompletionFunction]] = None):
        """Check if the functions definition is valid."""
        
        if functions_def is None:
            return

        for function in functions_def:
            if 'name' not in function:
              raise Exception('Function name must be provided')
            if 'description' not in function:
              raise Exception('Function description must be provided')
            if 'parameters' not in function:
              raise Exception('Function parameters must be provided')

            parameters = function['parameters']
            if 'type' not in parameters:
              raise Exception('Function parameters type must be provided')
            if parameters['type'] != 'object':
              raise Exception('Function parameters type must be object')
            if 'properties' not in parameters:
              raise Exception('Function parameters properties must be provided')

            properties = parameters['properties']
            if not isinstance(properties, dict):
                raise Exception('Function parameters properties must be an object')
            if 'required' in parameters and not isinstance(parameters['required'], list):
                raise Exception('Function parameters required must be an array')


    def _check_messages(self, messages: List[llama_types.ChatCompletionRequestMessage]):
        """Check if the messages are valid."""
        if len(messages) == 0:
          raise Exception('Messages cannot be empty')

        first_message = messages[0]
        if first_message['role'] == 'system':
          messages = messages[1:]

        if len(messages) == 0:
          raise Exception('At least user message must be provided')

        for (index, message) in enumerate(messages):
            if 'role' not in message or message['role'] not in ['user', 'assistant', 'tool']:
                raise Exception('Invalid role')
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

    def prompt_messages(self, messages:  List[llama_types.ChatCompletionRequestMessage], functions_def: Optional[List[llama_types.ChatCompletionFunction]] = None):
        self._check_messages(messages)
        self._check_functions_def(functions_def)

        system_instruction = self.SYSTEM_INSTRUCTION
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
    
    def __call__(
        self,
        llama: llama.Llama,
        messages: List[llama_types.ChatCompletionRequestMessage],
        functions: Optional[List[llama_types.ChatCompletionFunction]] = None,
        function_call: Optional[llama_types.ChatCompletionRequestFunctionCall] = None,
        tools: Optional[List[llama_types.ChatCompletionTool]] = None,
        tool_choice: Optional[llama_types.ChatCompletionToolChoiceOption] = None,
        temperature: float = 0.2,
        top_p: float = 0.95,
        top_k: int = 40,
        min_p: float = 0.05,
        typical_p: float = 1.0,
        stream: bool = False,
        stop: Optional[Union[str, List[str]]] = [],
        response_format: Optional[llama_types.ChatCompletionRequestResponseFormat] = None,
        max_tokens: Optional[int] = None,
        presence_penalty: float = 0.0,
        frequency_penalty: float = 0.0,
        repeat_penalty: float = 1.1,
        tfs_z: float = 1.0,
        mirostat_mode: int = 0,
        mirostat_tau: float = 5.0,
        mirostat_eta: float = 0.1,
        model: Optional[str] = None,
        logits_processor: Optional[llama.LogitsProcessorList] = None,
        grammar: Optional[llama.LlamaGrammar] = None,
        logprobs: Optional[bool] = None,
        top_logprobs: Optional[int] = None,
        **kwargs,  # type: ignore
    ) -> Union[
        llama_types.CreateChatCompletionResponse,
        Iterator[llama_types.CreateChatCompletionStreamResponse],
    ]:        
        template = "{% set loop_messages = messages %}{% for message in loop_messages %}{% set content = '<|start_header_id|>' + message['role'] + '<|end_header_id|>\n\n'+ message['content'] | trim + '<|eot_id|>' %}{% if loop.index0 == 0 %}{% set content = '<|begin_of_text|>' + content %}{% endif %}{{ content }}{% endfor %}{% if add_generation_prompt %}{{ '<|start_header_id|>assistant<|end_header_id|>\n\n' }}{% endif %}"
        template_renderer = ImmutableSandboxedEnvironment(
            autoescape=False,
            undefined=jinja2.StrictUndefined,
        ).from_string(template)

        # Convert legacy function_call to tool_choice
        if function_call is not None:
            if isinstance(function_call, str) and (
                function_call == "none" or function_call == "auto"
            ):
                tool_choice = function_call
            if isinstance(function_call, dict) and "name" in function_call:
                tool_choice = {
                    "type": "function",
                    "function": {
                        "name": function_call["name"],
                    },
                }
        if not tool_choice:
            tool_choice = "auto"
                
        assert tool_choice == "auto"
        
        if functions is None:
            functions = [ tool.get('function') for tool in tools ]

        stop = [stop, "<|eot_id|>"] if isinstance(stop, str) else stop + ["<|eot_id|>"] if stop else ["<|eot_id|>"]

        prompted_messages = self.prompt_messages(messages, functions)
        prompt = template_renderer.render(messages=prompted_messages, add_generation_prompt=True)

        # Case 1: No tool choice by user
        generated = llama.create_completion(
                prompt=prompt,
                temperature=temperature,
                top_p=top_p,
                top_k=top_k,
                min_p=min_p,
                typical_p=typical_p,
                stream=stream,
                stop=stop,
                max_tokens=max_tokens,
                presence_penalty=presence_penalty,
                frequency_penalty=frequency_penalty,
                repeat_penalty=repeat_penalty,
                tfs_z=tfs_z,
                mirostat_mode=mirostat_mode,
                mirostat_tau=mirostat_tau,
                mirostat_eta=mirostat_eta,
                model=model,
                logits_processor=logits_processor,
                grammar=grammar,
                logprobs=top_logprobs if logprobs else None,
            )
        generated_text = generated['choices'][0]['text']
        
        if generated_text.startswith('<f>'):
            json_object = json.loads(generated_text[3:])
            
            return _convert_completion_to_chat_function(
                json_object[0]["name"],
                completion_or_chunks=generated
            )
        elif generated_text.startswith('<c>'):
            generated['choices'][0]['text'] = generated_text[3:]
            return _convert_completion_to_chat(generated, stream=stream)

        return _convert_completion_to_chat(generated, stream=stream)

def _convert_completion_to_chat(
    completion_or_chunks: Union[
        llama_types.CreateCompletionResponse,
        Iterator[llama_types.CreateCompletionStreamResponse],
    ],
    stream: bool = False,
) -> Union[
    llama_types.CreateChatCompletionResponse, Iterator[llama_types.ChatCompletionChunk]
]:
    if stream:
        chunks: Iterator[llama_types.CreateCompletionStreamResponse] = completion_or_chunks  # type: ignore
        return _convert_text_completion_chunks_to_chat(chunks)
    else:
        completion: llama_types.Completion = completion_or_chunks  # type: ignore
        return _convert_text_completion_to_chat(completion)


def _convert_completion_to_chat_function(
    tool_name: str,
    completion_or_chunks: llama_types.CreateCompletionResponse,
):
    completion: llama_types.CreateCompletionResponse = completion_or_chunks  # type: ignore
    assert "usage" in completion
    tool_id = "call_" + "_0_" + tool_name + "_" + completion["id"]
    # TODO: Fix for legacy function calls
    
    json_object = json.loads(completion["choices"][0]["text"][3:])
    
    chat_completion: llama_types.CreateChatCompletionResponse = {
        "id": "chat" + completion["id"],
        "object": "chat.completion",
        "created": completion["created"],
        "model": completion["model"],
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": None,
                    "function_call": {
                        "name": tool_name,
                        "arguments": str(json_object[0]['arguments']),
                    },
                    "tool_calls": [
                        {
                            "id": tool_id,
                            "type": "function",
                            "function": {
                                "name": tool_name,
                                "arguments": str(json_object[0]['arguments']),
                            },
                        }
                    ],
                },
                "logprobs": completion["choices"][0]["logprobs"],
                "finish_reason": "tool_calls",
            }
        ],
        "usage": completion["usage"],
    }
    return chat_completion

def _convert_text_completion_chunks_to_chat(
    chunks: Iterator[llama_types.CreateCompletionStreamResponse],
) -> Iterator[llama_types.ChatCompletionChunk]:
    for i, chunk in enumerate(chunks):
        if i == 0:
            yield {
                "id": "chat" + chunk["id"],
                "model": chunk["model"],
                "created": chunk["created"],
                "object": "chat.completion.chunk",
                "choices": [
                    {
                        "index": 0,
                        "delta": {
                            "role": "assistant",
                        },
                        "logprobs": None,
                        "finish_reason": None,
                    }
                ],
            }
        yield {
            "id": "chat" + chunk["id"],
            "model": chunk["model"],
            "created": chunk["created"],
            "object": "chat.completion.chunk",
            "choices": [
                {
                    "index": 0,
                    "delta": (
                        {
                            "content": chunk["choices"][0]["text"],
                        }
                        if chunk["choices"][0]["finish_reason"] is None
                        else {}
                    ),
                    "logprobs": chunk["choices"][0]["logprobs"],
                    "finish_reason": chunk["choices"][0]["finish_reason"],
                }
            ],
        }


def _convert_completion_to_chat(
    completion_or_chunks: Union[
        llama_types.CreateCompletionResponse,
        Iterator[llama_types.CreateCompletionStreamResponse],
    ],
    stream: bool = False,
) -> Union[
    llama_types.CreateChatCompletionResponse, Iterator[llama_types.ChatCompletionChunk]
]:
    if stream:
        chunks: Iterator[llama_types.CreateCompletionStreamResponse] = completion_or_chunks  # type: ignore
        return _convert_text_completion_chunks_to_chat(chunks)
    else:
        completion: llama_types.Completion = completion_or_chunks  # type: ignore
        return _convert_text_completion_to_chat(completion)

def _convert_text_completion_to_chat(
    completion: llama_types.Completion,
) -> llama_types.ChatCompletion:
    assert "usage" in completion
    return {
        "id": "chat" + completion["id"],
        "object": "chat.completion",
        "created": completion["created"],
        "model": completion["model"],
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": completion["choices"][0]["text"],
                },
                "logprobs": completion["choices"][0]["logprobs"],
                "finish_reason": completion["choices"][0]["finish_reason"],
            }
        ],
        "usage": completion["usage"],
    }


def _convert_text_completion_chunks_to_chat(
    chunks: Iterator[llama_types.CreateCompletionStreamResponse],
) -> Iterator[llama_types.ChatCompletionChunk]:
    for i, chunk in enumerate(chunks):
        if i == 0:
            yield {
                "id": "chat" + chunk["id"],
                "model": chunk["model"],
                "created": chunk["created"],
                "object": "chat.completion.chunk",
                "choices": [
                    {
                        "index": 0,
                        "delta": {
                            "role": "assistant",
                        },
                        "logprobs": None,
                        "finish_reason": None,
                    }
                ],
            }
        yield {
            "id": "chat" + chunk["id"],
            "model": chunk["model"],
            "created": chunk["created"],
            "object": "chat.completion.chunk",
            "choices": [
                {
                    "index": 0,
                    "delta": (
                        {
                            "content": chunk["choices"][0]["text"],
                        }
                        if chunk["choices"][0]["finish_reason"] is None
                        else {}
                    ),
                    "logprobs": chunk["choices"][0]["logprobs"],
                    "finish_reason": chunk["choices"][0]["finish_reason"],
                }
            ],
        }
