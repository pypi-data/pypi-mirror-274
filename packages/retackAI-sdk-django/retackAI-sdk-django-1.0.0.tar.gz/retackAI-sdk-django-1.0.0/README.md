# Retack SDK for Django

The Retack SDK for Django allows you to easily report errors to the Retack AI service from your Django applications.

## Installation

You can install the Retack SDK using pip:

    pip install retack-sdk-django==1.0.0

## Usage

    from retackAI_sdk import retack_client

    # Initialize RetackConfig and RetackClient
    retack_config = retack_client.RetackConfig(api_key="V-oJTkB3fF2Hdnqz40jDOtEn")
    retack_client_instance = retack_client.RetackClient(retack_config)

    try:
        # use your code 
        pass

    except Exception as e:
        # Create an ErrorReportRequest
        error_report = retack_client.ErrorReportRequest(
            error=f"Member retrieval failed: {str(e)}",
            stack_trace=e.__traceback__,
            user_context=retack_client.UserContext(username="user", extras={"key": "value"})
        )
        # Report the error
        retack_client.report_error(error_report)

