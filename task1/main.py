from bloom_filter import BloomFilter
from password_checker import check_password_uniqueness

if __name__ == "__main__":
    bloom = BloomFilter(size=1000, num_hashes=3)

    existing_passwords = ["password123", "admin123", "qwerty123"]
    for password in existing_passwords:
        bloom.add(password)

    new_passwords_to_check = ["password123", "newpassword", "admin123", "guest"]
    results = check_password_uniqueness(bloom, new_passwords_to_check)

    for password, status in results.items():
        print(f"Пароль '{password}' — {status}.")
        
# Результат виконання:
# Пароль 'password123' — вже використаний.
# Пароль 'newpassword' — унікальний.
# Пароль 'admin123' — вже використаний.
# Пароль 'guest' — унікальний.
