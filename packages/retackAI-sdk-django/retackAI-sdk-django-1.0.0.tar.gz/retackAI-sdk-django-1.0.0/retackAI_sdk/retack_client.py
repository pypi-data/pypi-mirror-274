import json
import requests

class RetackClient:
    def __init__(self, retack_config):
        self.retrack_config = retack_config

    # async def report_error_async(self, error_report_request):
    def report_error_async(self, error_report):
        # Base URL
        base_url = "https://api.retack.ai"
        endpoint = "/observe/error-log/"

        headers = {
            "Content-Type": "application/json",
            "ENV-KEY": self.retrack_config.api_key
        }

        body = {
            "title": error_report.error,
            "stack_trace": error_report.stack_trace,
            "user_context": error_report.user_context.to_json() if error_report.user_context else None
        }

        try:
            response = requests.post(base_url + endpoint, headers=headers, json=body)
            response.raise_for_status()
            return True
        except Exception as e:
            print("Unable to report error to Retack AI.")
            print(e)
            return False

class RetackConfig:
    def __init__(self, api_key):
        self.api_key = api_key

class UserContext:
    def __init__(self, username, extras):
        self.username = username
        self.extras = extras

    def to_json(self):
        return json.dumps(self.__dict__)
    
class ErrorReportRequest:
    def __init__(self, error, stack_trace, user_context=None):
        self.error = error
        self.stack_trace = self.format_stack_trace(stack_trace) if stack_trace else None
        self.user_context = user_context

    def format_stack_trace(self, stack_trace):
        # Initialize an empty list to store stack trace details
        stack_trace_details = []

        # Iterate through the traceback frames
        while stack_trace is not None:
            frame = stack_trace.tb_frame
            code_context = frame.f_code.co_name
            if frame.f_locals:
                code_context += f" (locals: {frame.f_locals})"
            frame_info = {
                'filename': frame.f_code.co_filename,
                'lineno': stack_trace.tb_lineno,
                'function': frame.f_code.co_name,
                'line': stack_trace.tb_frame.f_lineno,
                'code_context': code_context,
                'module_name': frame.f_globals['__name__']
            }
            stack_trace_details.append(frame_info)
            stack_trace = stack_trace.tb_next

        # Convert stack trace details to a string
        return '\n'.join(
            f"File '{frame['filename']}', line {frame['lineno']}, in {frame['function']}, at line {frame['line']}\n{frame['code_context']}\nModule: {frame['module_name']}"
            for frame in stack_trace_details
        )