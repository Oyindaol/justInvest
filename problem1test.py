from justInvest import check_permission
from datetime import datetime

# Mock the current time for testing
def mock_current_time(hour):
    class MockDateTime(datetime):
        @classmethod
        def now(cls):
            return cls(2024, 11, 15, hour, 0, 0)  # Mock a specific hour
    return MockDateTime

# Define a helper function to test the access control mechanism
def test_access_control():
    test_results = []

    # Test Case 1: Client attempting to view balance
    result = check_permission("Sasha Kim", "View account balance")
    test_results.append(("Test Case-1", result == "ACCESS GRANTED"))

    # Test Case 2: Client attempting to modify portfolio
    result = check_permission("Sasha Kim", "Modify investment portfolio")
    test_results.append(("Test Case-2", result == "ACCESS DENIED"))

    # Test Case 3: Premium Client attempting to modify portfolio
    result = check_permission("Noor Abbasi", "Modify investment portfolio")
    test_results.append(("Test Case-3", result == "ACCESS GRANTED"))

    # Test Case 4: Premium Client attempting to view planner contact
    result = check_permission("Noor Abbasi", "View Financial Planner contact info")
    test_results.append(("Test Case-4", result == "ACCESS GRANTED"))

    # Test Case 5: Financial Advisor modifying portfolio
    result = check_permission("Mikael Chen", "Modify investment portfolio")
    test_results.append(("Test Case-5", result == "ACCESS GRANTED"))

    # Test Case 6: Financial Advisor viewing money market instruments
    result = check_permission("Mikael Chen", "View money market instruments")
    test_results.append(("Test Case-6", result == "ACCESS DENIED"))

    # Test Case 7: Mock Teller time-based test: Inside business hours
    datetime = mock_current_time(10)  # Mock 10:00 AM
    result = check_permission("Alex Hayes", "View account balance")
    test_results.append(("Test Case-7", result == "ACCESS GRANTED"))

    # Test Case 8: Mock Teller time-based test: Outside business hours
    datetime = mock_current_time(18)  # Mock 6:00 PM
    result = check_permission("Alex Hayes", "View investment portfolio")
    test_results.append(("Test Case-8", result == "ACCESS DENIED"))

    # Test Case 9: Unknown user attempting to view balance
    result = check_permission("Test User", "View account balance")
    test_results.append(("Test Case-9", result == "User Test User does not exist."))

    return test_results

if __name__ == "__main__":
    results = test_access_control()
    for tc_id, passed in results:
        status = "PASSED" if passed else "FAILED"
        print(f"{tc_id}: {status}")

