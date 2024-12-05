#!/usr/bin/env python3

from justInvest import check_permission
from problem1c import mock_current_time
import justInvest

def test_login_and_access_control():
    results = []

    # Test Case 1: Role-Based Access                                                                                        
    try:
        username = "Jordan Riley"  # Financial Advisor
        # role = "Financial Advisor"
        authorized_action = "View account balance"
        unauthorized_action = "View money market instruments"
        can_access = check_permission(username, authorized_action) == "ACCESS GRANTED"
        cannot_access = check_permission(username, unauthorized_action) == "ACCESS DENIED"
        results.append(("Test Case 1", can_access and cannot_access))
    except Exception as e:
        results.append(("Test Case 1", False))

    try:
        username = "Alex Hayes"  # A Teller

        # Test during business hours
        justInvest.datetime = mock_current_time(10)  # Mock 10:00 AM
        result_during_hours = check_permission(username, "View account balance") == "ACCESS GRANTED"

        results.append(("Test Case 2", result_during_hours))
    except Exception as e:
        results.append(("Test Case 2", False))

    # Test Case 3: Unauthorized Role Actions
    try:
        username = "Noor Abbasi"  # Premium Client
        unauthorized_action = "View money market instruments"
        results.append(("Test Case 3", check_permission(username, unauthorized_action) 
                        == "ACCESS DENIED"))
    except Exception as e:
        results.append(("Test Case 3", False))

    return results                                                                                                                                                           
if __name__ == "__main__":
    test_results = test_login_and_access_control()
    for tc_id, passed in test_results:
        status = "PASSED" if passed else "FAILED"
        print(f"{tc_id}: {status}")

