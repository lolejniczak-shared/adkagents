_AGENT_ENGINE_CLASS_METHODS = [
    {
        'name': 'get_session',
        'description': (
            'Deprecated. Use async_get_session instead.\n\n        Get a'
            ' session for the given user.\n        '
        ),
        'parameters': {
            'properties': {
                'user_id': {'type': 'string'},
                'session_id': {'type': 'string'},
            },
            'required': ['user_id', 'session_id'],
            'type': 'object',
        },
        'api_mode': '',
    },
    {
        'name': 'list_sessions',
        'description': (
            'Deprecated. Use async_list_sessions instead.\n\n        List'
            ' sessions for the given user.\n        '
        ),
        'parameters': {
            'properties': {'user_id': {'type': 'string'}},
            'required': ['user_id'],
            'type': 'object',
        },
        'api_mode': '',
    },
    {
        'name': 'create_session',
        'description': (
            'Deprecated. Use async_create_session instead.\n\n        Creates a'
            ' new session.\n        '
        ),
        'parameters': {
            'properties': {
                'user_id': {'type': 'string'},
                'session_id': {'type': 'string', 'nullable': True},
                'state': {'type': 'object', 'nullable': True},
            },
            'required': ['user_id'],
            'type': 'object',
        },
        'api_mode': '',
    },
    {
        'name': 'delete_session',
        'description': (
            'Deprecated. Use async_delete_session instead.\n\n        Deletes a'
            ' session for the given user.\n        '
        ),
        'parameters': {
            'properties': {
                'user_id': {'type': 'string'},
                'session_id': {'type': 'string'},
            },
            'required': ['user_id', 'session_id'],
            'type': 'object',
        },
        'api_mode': '',
    },
    {
        'name': 'async_get_session',
        'description': (
            'Get a session for the given user.\n\n        Args:\n           '
            ' user_id (str):\n                Required. The ID of the user.\n  '
            '          session_id (str):\n                Required. The ID of'
            ' the session.\n            **kwargs (dict[str, Any]):\n           '
            '     Optional. Additional keyword arguments to pass to the\n      '
            '          session service.\n\n        Returns:\n           '
            ' Session: The session instance (if any). It returns None if the\n '
            '           session is not found.\n\n        Raises:\n           '
            ' RuntimeError: If the session is not found.\n        '
        ),
        'parameters': {
            'properties': {
                'user_id': {'type': 'string'},
                'session_id': {'type': 'string'},
            },
            'required': ['user_id', 'session_id'],
            'type': 'object',
        },
        'api_mode': 'async',
    },
    {
        'name': 'async_list_sessions',
        'description': (
            'List sessions for the given user.\n\n        Args:\n           '
            ' user_id (str):\n                Required. The ID of the user.\n  '
            '          **kwargs (dict[str, Any]):\n                Optional.'
            ' Additional keyword arguments to pass to the\n               '
            ' session service.\n\n        Returns:\n           '
            ' ListSessionsResponse: The list of sessions.\n        '
        ),
        'parameters': {
            'properties': {'user_id': {'type': 'string'}},
            'required': ['user_id'],
            'type': 'object',
        },
        'api_mode': 'async',
    },
    {
        'name': 'async_create_session',
        'description': (
            'Creates a new session.\n\n        Args:\n            user_id'
            ' (str):\n                Required. The ID of the user.\n          '
            '  session_id (str):\n                Optional. The ID of the'
            ' session. If not provided, an ID\n                will be be'
            ' generated for the session.\n            state (dict[str, Any]):\n'
            '                Optional. The initial state of the session.\n     '
            '       **kwargs (dict[str, Any]):\n                Optional.'
            ' Additional keyword arguments to pass to the\n               '
            ' session service.\n\n        Returns:\n            Session: The'
            ' newly created session instance.\n        '
        ),
        'parameters': {
            'properties': {
                'user_id': {'type': 'string'},
                'session_id': {'type': 'string', 'nullable': True},
                'state': {'type': 'object', 'nullable': True},
            },
            'required': ['user_id'],
            'type': 'object',
        },
        'api_mode': 'async',
    },
    {
        'name': 'async_delete_session',
        'description': (
            'Deletes a session for the given user.\n\n        Args:\n          '
            '  user_id (str):\n                Required. The ID of the user.\n '
            '           session_id (str):\n                Required. The ID of'
            ' the session.\n            **kwargs (dict[str, Any]):\n           '
            '     Optional. Additional keyword arguments to pass to the\n      '
            '          session service.\n        '
        ),
        'parameters': {
            'properties': {
                'user_id': {'type': 'string'},
                'session_id': {'type': 'string'},
            },
            'required': ['user_id', 'session_id'],
            'type': 'object',
        },
        'api_mode': 'async',
    },
    {
        'name': 'async_add_session_to_memory',
        'description': (
            'Generates memories.\n\n        Args:\n            session'
            ' (Dict[str, Any]):\n                Required. The session to use'
            ' for generating memories. It should\n                be a'
            ' dictionary representing an ADK Session object, e.g.\n            '
            '    session.model_dump(mode="json").\n        '
        ),
        'parameters': {
            'properties': {
                'session': {'additionalProperties': True, 'type': 'object'}
            },
            'required': ['session'],
            'type': 'object',
        },
        'api_mode': 'async',
    },
    {
        'name': 'async_search_memory',
        'description': (
            'Searches memories for the given user.\n\n        Args:\n          '
            '  user_id: The id of the user.\n            query: The query to'
            ' match the memories on.\n\n        Returns:\n            A'
            ' SearchMemoryResponse containing the matching memories.\n        '
        ),
        'parameters': {
            'properties': {
                'user_id': {'type': 'string'},
                'query': {'type': 'string'},
            },
            'required': ['user_id', 'query'],
            'type': 'object',
        },
        'api_mode': 'async',
    },
    {
        'name': 'stream_query',
        'description': (
            'Deprecated. Use async_stream_query instead.\n\n        Streams'
            ' responses from the ADK application in response to a message.\n\n '
            '       Args:\n            message (Union[str, Dict[str, Any]]):\n '
            '               Required. The message to stream responses for.\n   '
            '         user_id (str):\n                Required. The ID of the'
            ' user.\n            session_id (str):\n                Optional.'
            ' The ID of the session. If not provided, a new\n               '
            ' session will be created for the user.\n            run_config'
            ' (Optional[Dict[str, Any]]):\n                Optional. The run'
            ' config to use for the query. If you want to\n                pass'
            ' in a `run_config` pydantic object, you can pass in a dict\n      '
            '          representing it as'
            ' `run_config.model_dump(mode="json")`.\n            **kwargs'
            ' (dict[str, Any]):\n                Optional. Additional keyword'
            ' arguments to pass to the\n                runner.\n\n       '
            ' Yields:\n            The output of querying the ADK'
            ' application.\n        '
        ),
        'parameters': {
            'properties': {
                'message': {
                    'anyOf': [
                        {'type': 'string'},
                        {'additionalProperties': True, 'type': 'object'},
                    ]
                },
                'user_id': {'type': 'string'},
                'session_id': {'type': 'string', 'nullable': True},
                'run_config': {'type': 'object', 'nullable': True},
            },
            'required': ['message', 'user_id'],
            'type': 'object',
        },
        'api_mode': 'stream',
    },
    {
        'name': 'async_stream_query',
        'description': (
            'Streams responses asynchronously from the ADK application.\n\n    '
            '    Args:\n            message (str):\n                Required.'
            ' The message to stream responses for.\n            user_id'
            ' (str):\n                Required. The ID of the user.\n          '
            '  session_id (str):\n                Optional. The ID of the'
            ' session. If not provided, a new\n                session will be'
            ' created for the user.\n            run_config (Optional[Dict[str,'
            ' Any]]):\n                Optional. The run config to use for the'
            ' query. If you want to\n                pass in a `run_config`'
            ' pydantic object, you can pass in a dict\n               '
            ' representing it as `run_config.model_dump(mode="json")`.\n       '
            '     **kwargs (dict[str, Any]):\n                Optional.'
            ' Additional keyword arguments to pass to the\n               '
            ' runner.\n\n        Yields:\n            Event dictionaries'
            ' asynchronously.\n        '
        ),
        'parameters': {
            'properties': {
                'message': {
                    'anyOf': [
                        {'type': 'string'},
                        {'additionalProperties': True, 'type': 'object'},
                    ]
                },
                'user_id': {'type': 'string'},
                'session_id': {'type': 'string', 'nullable': True},
                'run_config': {'type': 'object', 'nullable': True},
            },
            'required': ['message', 'user_id'],
            'type': 'object',
        },
        'api_mode': 'async_stream',
    },
    {
        'name': 'streaming_agent_run_with_events',
        'description': (
            'Streams responses asynchronously from the ADK application.\n\n    '
            '    In general, you should use `async_stream_query` instead, as it'
            ' has a\n        more structured API and works with the respective'
            ' ADK services that\n        you have defined for the AdkApp. This'
            ' method is primarily meant for\n        invocation from'
            ' AgentSpace.\n\n        Args:\n            request_json (str):\n  '
            '              Required. The request to stream responses for.\n   '
            '     '
        ),
        'parameters': {
            'properties': {'request_json': {'type': 'string'}},
            'required': ['request_json'],
            'type': 'object',
        },
        'api_mode': 'async_stream',
    },
]