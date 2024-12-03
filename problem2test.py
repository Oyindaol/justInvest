from justInvest import append_to_file, generate_salt, calculate_sha256,verify_password, search_user, is_valid_password

def test_password_file():
    test_results = []

    # Test Case 1: Register a new user
    try:
        username = "test_name"
        password = "Pass$123"
        role = "Client"
        salt = generate_salt()
        hashed_password = calculate_sha256(password + salt)
        append_to_file(username, salt, hashed_password, role)
        user_record = search_user(username)
        test_results.append(("Test Case-1", user_record is not None))
    except Exception as e:
        test_results.append(("Test Case-1", False))

    # Test Case 2: Verify an existing user with correct password
    try:
        result = verify_password("test_name", "Pass$123")
        test_results.append(("Test Case-2", result == "ACCESS GRANTED"))
    except Exception as e:
        test_results.append(("Test Case-2", False))

    # Test Case 3: Verify an existing user with incorrect password
    try:
        result = verify_password("test_name", "WrongPass@123")
        test_results.append(("Test Case-3", result == "ACCESS DENIED"))
    except Exception as e:
        test_results.append(("Test Case-3", False))

    # Test Case 4: Search for an existing user
    try:
        user_record = search_user("test_name")
        test_results.append(("Test Case-4", user_record is not None))
    except Exception as e:
        test_results.append(("Test Case-4", False))

    # Test Case 5: Attempt to login with non-existing user
    try:
        user_record = search_user("unknown_user")
        test_results.append(("Test Case-5", user_record is None))
    except Exception as e:
        test_results.append(("Test Case-5", False))

    # Test Case 6: Register a user with invalid password
    try:
        invalid_password = "weakpass"  # Fails password validation
        valid = is_valid_password(invalid_password)
        test_results.append(("Test Case-6", valid is False))
    except Exception as e:
        test_results.append(("Test Case-6", False))

    return test_results


if __name__ == "__main__":
    results = test_password_file()
    for tc_id, passed in results:
        status = "PASSED" if passed else "FAILED"
        print(f"{tc_id}: {status}")

