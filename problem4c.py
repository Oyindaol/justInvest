#!/usr/bin/env python3

from datetime import datetime
from justInvest import check_permission

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

    # Test Case 2: Time-Based Restrictions for Tellers
    try:
        username = "Alex Hayes"  # A Teller
        current_hour = datetime.now().hour
        if 9 <= current_hour <= 17:
            can_access = check_permission(username, "View account balance") == "ACCESS GRANTED"
        else:
            can_access = check_permission(username, "View account balance") == "ACCESS DENIED"
        results.append(("Test Case 2", can_access))
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

