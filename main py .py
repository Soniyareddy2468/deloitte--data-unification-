# Deloitte Technology Job Simulation - Data Unification Algorithm
import json
from datetime import datetime

def convertFromFormat1(jsonObject):
    """
    Converts telemetry data from Format 1 to the unified target format.
    Format 1 has a slash-separated 'location' string and 'operationStatus', 'temp'.
    """
    location_parts = jsonObject["location"].split("/")
    
    return {
        "deviceID": jsonObject["deviceID"],
        "deviceType": jsonObject["deviceType"],
        "timestamp": jsonObject["timestamp"],
        "location": {
            "country": location_parts[0],
            "city": location_parts[1],
            "area": location_parts[2],
            "factory": location_parts[3],
            "section": location_parts[4]
        },
        "data": {
            "status": jsonObject["operationStatus"],
            "temperature": jsonObject["temp"]
        }
    }

def convertFromFormat2(jsonObject):
    """
    Converts telemetry data from Format 2 to the unified target format.
    Format 2 has nested device/data objects and an ISO timestamp string.
    """
    # Parse ISO 8601 timestamp string to milliseconds since epoch
    dt = datetime.fromisoformat(jsonObject["timestamp"].replace("Z", "+00:00"))
    timestamp_ms = int(dt.timestamp() * 1000)
    
    return {
        "deviceID": jsonObject["device"]["id"],
        "deviceType": jsonObject["device"]["type"],
        "timestamp": timestamp_ms,
        "location": {
            "country": jsonObject["country"],
            "city": jsonObject["city"],
            "area": jsonObject["area"],
            "factory": jsonObject["factory"],
            "section": jsonObject["section"]
        },
        "data": {
            "status": jsonObject["data"]["status"],
            "temperature": jsonObject["data"]["temperature"]
        }
    }

def run_tests():
    # Load input and expected result files
    with open("./data-1.json", "r") as f:
        data1 = json.load(f)
    with open("./data-2.json", "r") as f:
        data2 = json.load(f)
    with open("./data-result.json", "r") as f:
        expected_result = json.load(f)

    # Test Format 1 conversion
    res1 = convertFromFormat1(data1)
    print("Format 1 Conversion Result:")
    print(json.dumps(res1, indent=2))
    
    # Test Format 2 conversion
    res2 = convertFromFormat2(data2)
    print("\nFormat 2 Conversion Result:")
    print(json.dumps(res2, indent=2))
    
    # Assertions / Unit Test check
    assert res1 == expected_result, "Format 1 output does not match expected result!"
    assert res2 == expected_result, "Format 2 output does not match expected result!"
    print("\n✨ All unit tests passed successfully!")

if __name__ == "__main__":
    run_tests()
