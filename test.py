import db
from pprint import pprint
from util import dict_snake_to_camelCase


NIL_UUID = "00000000-0000-0000-0000-000000000000"


def main():
    db.setup()

    # Create
    receiptId = db.insert_receipt(NIL_UUID, 5, 9.855, 3.499)
    print("Added ID:", receiptId)

    # Retrieve
    receipt = db.select_receipt(receiptId)
    print("Added receipt:", end=" ")
    pprint(receipt)

    # Update
    newStationId = 6
    newGallons = 2.345
    newPPG = 2.599
    succ = db.update_receipt(receiptId, newStationId, newGallons, newPPG)
    if not succ:
        print("Update did not succeed")

        return
    receipt = db.select_receipt(receiptId)
    print("Updated receipt:", end=" ")
    pprint(receipt)
    if receipt["station_id"] != newStationId and receipt["gallons"] != newGallons and receipt["price_per_gallon"] != newPPG:
        print("Update did not occur on server or does not have correct values")

        return

    # Soft delete
    succ = db.update_receipt(receiptId, deleted=True)
    if not succ:
        print("Update did not succeed")

        return
    receipt = db.select_receipt(receiptId)
    print("Soft deleted receipt:", end=" ")
    pprint(receipt)
    if receipt["station_id"] != newStationId and receipt["gallons"] != newGallons and receipt["price_per_gallon"] != newPPG:
        print("Soft delete changed row data when it should not have")

        return

    # No update
    succ = db.update_receipt(receiptId)
    if not succ:
        print("Update did not succeed")

        return
    receipt = db.select_receipt(receiptId)
    print("No update receipt:", end=" ")
    pprint(receipt)
    if receipt["station_id"] != newStationId and receipt["gallons"] != newGallons and receipt["price_per_gallon"] != newPPG:
        print("Soft delete changed row data when it should not have")

        return

    # Un-soft delete
    succ = db.update_receipt(receiptId, deleted=False)
    if not succ:
        print("Update did not succeed")

        return
    receipt = db.select_receipt(receiptId)
    print("Un-soft delete receipt:", end=" ")
    pprint(receipt)
    if receipt["station_id"] != newStationId and receipt["gallons"] != newGallons and receipt["price_per_gallon"] != newPPG:
        print("Soft delete changed row data when it should not have")

        return

    # Hard delete
    succ = db.delete_receipt(receiptId)
    if not succ:
        print("Delete did not succeed")
    receipt = db.select_receipt(receiptId)
    if receipt is not None:
        print("Delete did not occur on server")

        return

    return


if __name__ == "__main__":
    main()
