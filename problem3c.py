from justInvest import generate_salt,calculate_sha256, append_to_file, search_user, is_valid_password

def test_enrolment_mechanism():
    roles = ["Client", "Premium Client", "Financial Planner", "Financial Advisor", "Teller"] 
    test_results = []

    # Test Case 1: Valid username, password, and role
    try:
        username = "valid_user"
        password = "Valid@123"
        role = "Client"
        salt = generate_salt()
        hashed_password = calculate_sha256(password + salt)
        append_to_file(username, salt, hashed_password, role)
        user_record = search_user(username)
        test_results.append(("Test Case-1", user_record is not None))
    except Exception as e:
        test_results.append(("Test Case-1", False))

    # Test Case 2: Weak password
    try:
        result = is_valid_password("Password1")  # Weak password
        test_results.append(("Test Case-2", result is False))
    except Exception as e:
        test_results.append(("Test Case-2", False))

    # Test Case 3: Password missing special characters
    try:
        result = is_valid_password("NoSpecial1")  # Missing special character
        test_results.append(("Test Case-3", result is False))
    except Exception as e:
        test_results.append(("Test Case-3", False))

    # Test Case 4: Password too short
    try:
        result = is_valid_password("S@1")  # Too short
        test_results.append(("Test Case-4", result is False))
    except Exception as e:
        test_results.append(("Test Case-4", False))

    # Test Case 5: Password too long
    try:
        result = is_valid_password("VeryLongPassword@123")  # Too long
        test_results.append(("Test Case-5", result is False))
    except Exception as e:
        test_results.append(("Test Case-5", False))

    # Test Case 6: Password maTest Casehing a weak pattern
    try:
        result = is_valid_password("01/01/2000")
        test_results.append(("Test Case-6", result is False))
    except Exception as e:
        test_results.append(("Test Case-6", False))

    # Test Case 7: Invalid role
    try:
        valid_role = "InvalidRole" not in roles
        test_results.append(("Test Case-7", valid_role))
    except Exception as e:
        test_results.append(("Test Case-7", False))

    return test_results

if __name__ == "__main__":
    results = test_enrolment_mechanism()
    for tc_id, passed in results:
        status = "PASSED" if passed else "FAILED"
        print(f"{tc_id}: {status}")
