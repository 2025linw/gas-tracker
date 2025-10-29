from util import is_uuid

def validate_receipt_post(body: dict):
    """
    TODO: docs
    """

    # Check for required values in body
    missing = []
    if "vehicleId" not in body:
        missing.append("vehicleId")
    if "stationId" not in body:
        missing.append("stationId")
    if "gallons" not in body:
        missing.append("gallons")
    if "pricePerGallon" not in body:
        missing.append("pricePerGallon")
    if len(missing) != 0:
        return False, f"Missing values in request body: {", ".join(missing)}"

    # Check type of values in body
    if not is_uuid(body["vehicleId"]):
        return False, "Expected UUID for vehicleId"
    if not isinstance(body["stationId"], int):
        return False, "Expected number (int) for stationId"
    if not isinstance(body["gallons"], (int, float)):
        return False, "Expected number for gallons"
    if not isinstance(body["pricePerGallon"], (int, float)):
        return False, "Expected number for gallons"

    return True, ""

def validate_receipt_get(receiptId: str):
    """
    TODO: docs
    """

    if not is_uuid(receiptId):
        return False, "Expected UUID for receiptId"

    return True, ""

def validate_receipt_patch(receiptId: str, body: dict):
    """
    TODO: docs
    """

    if not is_uuid(receiptId):
        return False, "Expected UUID for receiptId"

    # Check type of values in body
    hasUpdate = False
    if "vehicleId" in body:
        if not is_uuid(body["vehicleId"]):
            return False, "Expected UUID for vehicleId"
        hasUpdate = True
    if "stationId" in body:
        if not isinstance(body["stationId"], int):
            return False, "Expected number (int) for stationId"
        hasUpdate = True
    if "gallons" in body:
        if not isinstance(body["gallons"], (int, float)):
            return False, "Expected number for gallons"
        hasUpdate = True
    if "pricePerGallon" in body:
        if not isinstance(body["pricePerGallon"], (int, float)):
            return False, "Expected number for pricePerGallon"
        hasUpdate = True
    if "deleted" in body:
        if not isinstance(body["deleted"], bool):
            return False, "Expected boolean for deleted"
        hasUpdate = True
    if not hasUpdate:
        return False, "No updates requested"

    return True, ""

def validate_receipt_delete(receiptId: str):
    """
    TODO: docs
    """

    if not is_uuid(receiptId):
        return False, "Expected UUID for receiptId"

    return True, ""

def validate_receipt_query(vehicleId: str | None):
    """
    TODO: docs
    """

    if vehicleId is not None and not is_uuid(vehicleId):
        return False, "Expected UUID for vehicleId"

    return True, ""
