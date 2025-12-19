from bloom_filter import BloomFilter

def check_password_uniqueness(bloom_filter, passwords):
    results = {}

    for password in passwords:
        if not isinstance(password, str) or password.strip() == "":
            results[password] = "некоректне значення"
            continue

        if bloom_filter.contains(password):
            results[password] = "вже використаний"
        else:
            results[password] = "унікальний"
            bloom_filter.add(password)

    return results