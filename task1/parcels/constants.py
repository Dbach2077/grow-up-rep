# --- Модели ---
FULL_NAME_MAX_LENGTH = 255
LOCATION_MAX_LENGTH = 255
PHONE_MAX_LENGTH = 20

# --- Сериализаторы ---

# Константы для сериализаторов
WEIGHT_MAX_DIGITS = 7
WEIGHT_DECIMAL_PLACES = 3
PAYMENT_MAX_DIGITS = 10
PAYMENT_DECIMAL_PLACES = 2

# Значения для валидаторов
POSTCODE_MIN_VALUE = 100000
WEIGHT_MIN_VALUE = 0.001
PAYMENT_MIN_VALUE = 0.0

# Сообщения об ошибках валидации
ERROR_MSG_POSTCODE_LENGTH = "Индекс должен состоять из 6 цифр"
ERROR_MSG_WEIGHT_POSITIVE = "Вес должен быть положительным числом."
ERROR_MSG_PAYMENT_NEGATIVE = "Сумма платежа не может быть отрицательной."
ERROR_MSG_POSTCODE_MATCH = "Индекс отправки и назначения не должны совпадать."
ERROR_MSG_LOCATION_MATCH = "Пункт отправки и назначения не должны совпадать."