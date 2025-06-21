class Node:

    def __init__(self, value, next_node=None):
        self.value = value  # значение (тип топлива)
        self.next = next_node  # ссылка на следующий узел (ниже по стеку)


class Stack:

    def __init__(self):
        self.top_node = None  # вершина стека (верхняя бочка)
        self.size = 0  # количество элементов в стеке

    def push(self, value):
        # Добавление элемента на вершину стека
        self.top_node = Node(value, self.top_node)
        self.size += 1

    def pop(self):
        # Удаление верхнего элемента стека
        if self.is_empty():
            raise IndexError("Стек пуст")
        value = self.top_node.value
        self.top_node = self.top_node.next
        self.size -= 1
        return value

    def top(self):
        # Получение значения верхнего элемента
        if self.is_empty():
            raise IndexError("Стек пуст")
        return self.top_node.value

    def is_empty(self):
        # Проверка, пуст ли стек
        return self.top_node is None


class Barge:
    def __init__(self, num_compartments, max_capacity):
        # Инициализация баржи с пустыми отсеками, каждый представлен стеком
        self.compartments = [Stack() for _ in range(num_compartments + 1)]  # индексация с 1
        self.capacity = max_capacity  # ёмкость баржи
        self.total_barrels = 0  # текущее количество бочек
        self.max_barrels = 0  # максимальное количество одновременно находившихся на борту
        self.error = False
        self.error_message = ""

    def load(self, compartment, fuel_type):
        # Погрузка бочки в указанный отсек
        self.compartments[compartment].push(fuel_type)
        self.total_barrels += 1

        # Проверка на превышение допустимого количества бочек
        if self.total_barrels > self.capacity:
            self.error = True
            self.error_message = f"Превышено максимальное количество бочек на барже: {self.capacity}"

        self.max_barrels = max(self.max_barrels, self.total_barrels)

    def unload(self, compartment, fuel_type):
        stack = self.compartments[compartment]

        # Проверка: отсек не должен быть пуст
        if stack.is_empty():
            self.error = True
            self.error_message = f"Ошибка: отсек {compartment} пуст, нельзя извлечь бочку."
            return

        # Проверка соответствия типа топлива
        if stack.top() != fuel_type:
            self.error = True
            self.error_message = (
                f"Ошибка: ожидался вид топлива {fuel_type}, но в отсеке {compartment} сверху {stack.top()}."
            )
            return

        # Удаление бочки
        stack.pop()
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
        # Проверка: пуста ли баржа (все бочки выгружены)
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

    barge = Barge(k, p)

    # Последовательная обработка всех операций
    i = 0
    print(f"\nВведите {n} операций:")
    while i < n:
        op = input(f"[{i + 1}] >>> ").strip()
        barge.process(op, i + 1)

        if barge.error:
            print(f"❌ {barge.error_message}")
            print("🔁 Повторите ввод этой строки.\n")
            barge.error = False
            barge.error_message = ""
            continue  # не увеличиваем счётчик — повтор ввода
        else:
            i += 1

    # Проверка на пустоту после маршрута
    if not barge.is_empty():
        print("\n❌ Баржа не пуста после завершения всех операций.")
        return

    # Успешный результат
    print(f"\n✅ Маршрут завершён без ошибок. Максимум бочек на борту: {barge.max_barrels}")


if __name__ == '__main__':
    main()
