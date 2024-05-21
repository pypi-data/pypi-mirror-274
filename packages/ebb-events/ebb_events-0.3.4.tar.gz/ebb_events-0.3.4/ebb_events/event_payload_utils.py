import copy
from ebb_events.event_schema import DataSchema
from ebb_events.field_constants import METADATA


def validate_data_event_payload_message(payload_message: dict):
    """
    Helper returns True if data payload_message matches expected structure.
    Helper returns dictionary of error information indicating which fields in the
    payload_message do not follow the expected structure.

    Expected structure:
    {
        "var_name": {
            "value": float,
            "units": str,
        },
        ...
    }
    """
    # Copy of payload_message so that we don't actually alter the raw_payload itself
    payload_message_copy: dict = copy.deepcopy(payload_message)
    payload_message_copy.pop(METADATA, None)
    errors_dict = DataSchema(many=True).validate(list(payload_message_copy.values()))
    return True if errors_dict == {} else errors_dict
