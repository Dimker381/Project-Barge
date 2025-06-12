class Barge:
    def __init__(self, num_compartments, max_capacity):
        # Инициализация баржи с пустыми отсеками и ограничением по бочкам
        self.compartments = [[] for _ in range(num_compartments + 1)]  # индексация с 1
        self.capacity = max_capacity     # ёмкость
        self.total_barrels = 0           # текущее количество бочек
        self.max_barrels = 0             # максимальное количество одновременно
        self.error = False
        self.error_message = ""

    def load(self, compartment, fuel_type):
        # Погрузка бочки в указанный отсек
        self.compartments[compartment].append(fuel_type)
        self.total_barrels += 1

        # Проверка на переполнение
        if self.total_barrels > self.capacity:
            self.error = True
            self.error_message = f"Превышено максимальное количество бочек на барже: {self.capacity}"

        self.max_barrels = max(self.max_barrels, self.total_barrels)

    def unload(self, compartment, fuel_type):
        # Проверка: отсек не должен быть пуст
        if not self.compartments[compartment]:
            self.error = True
            self.error_message = f"Ошибка: отсек {compartment} пуст, нельзя извлечь бочку."
            return

        # Проверка соответствия типа топлива
        top_fuel = self.compartments[compartment][-1]
        if top_fuel != fuel_type:
            self.error = True
            self.error_message = (
                f"Ошибка: ожидался вид топлива {fuel_type}, но в отсеке {compartment} сверху {top_fuel}."
            )
            return

        # Удаление бочки
        self.compartments[compartment].pop()
        self.total_barrels -= 1

    def process(self, operation, line_num=None):
        # Обработка одной строки операции
        parts = operation.strip().split()
        if len(parts) != 3:
            self.error = True
            self.error_message = f"Ошибка в строке {line_num}: неправильный формат команды."
            return

        action, a_str, b_str = parts
        if action not in ('+', '-'):
            self.error = True
            self.error_message = f"Ошибка в строке {line_num}: неизвестное действие '{action}'."
            return

        try:
            compartment = int(a_str)
            fuel_type = int(b_str)
        except ValueError:
            self.error = True
            self.error_message = f"Ошибка в строке {line_num}: номер отсека и вид топлива должны быть целыми числами."
            return

        # Проверка допустимости номера отсека
        if not (1 <= compartment < len(self.compartments)):
            self.error = True
            self.error_message = f"Ошибка: номер отсека {compartment} вне допустимого диапазона."
            return

        # Выполнение действия
        if action == '+':
            self.load(compartment, fuel_type)
        else:
            self.unload(compartment, fuel_type)

    def is_empty(self):
        return self.total_barrels == 0


def main():
    # Приветствие и краткая инструкция
    print("🚢 Добро пожаловать в симулятор работы баржи.")
    print("Введите данные в следующем формате:")
    print("На первой строке: N K P")
    print("Где N — число операций, K — число отсеков, P — максимум бочек.")
    print("Далее N строк вида '+ A B' или '- A B'\n")

    try:
        # Ввод первой строки с параметрами
        n_k_p = input("Введите значения N K P через пробел: ").strip().split()
        if len(n_k_p) != 3:
            print("❌ Ошибка: нужно ввести три целых числа через пробел.")
            return
        n, k, p = map(int, n_k_p)
    except ValueError:
        print("❌ Ошибка: N, K и P должны быть целыми числами.")
        return

    # Проверка допустимых границ
    if not (1 <= n <= 100_000 and 1 <= k <= 100_000 and 1 <= p <= 100_000):
        print("❌ Ошибка: значения N, K и P должны быть от 1 до 100000.")
        return

    operations = []
    print(f"\nВведите {n} операций:")
    for i in range(n):
        try:
            line = input(f"[{i+1}] >>> ").strip()
            operations.append(line)
        except EOFError:
            print("❌ Недостаточно строк ввода.")
            return

    barge = Barge(k, p)

    # Последовательная обработка всех операций
    for idx, op in enumerate(operations, start=1):
        barge.process(op, idx)
        if barge.error:
            print(f"\n❌ {barge.error_message}")
            return

    # Проверка на пустоту после маршрута
    if not barge.is_empty():
        print("\n❌ Баржа не пуста после завершения всех операций.")
        return

    # Успешный результат
    print(f"\n✅ Маршрут завершён без ошибок. Максимум бочек на борту: {barge.max_barrels}")


if __name__ == "__main__":
    main()
