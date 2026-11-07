from abc import ABC, abstractmethod

class Employee(ABC):

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def calculate_pay(self):
        pass

class SalariedEmployee(Employee):

    def __init__(self, name, salary):
        super().__init__(name)
        self.salary = salary

    def calculate_pay(self):
        return self.salary

emp1 = SalariedEmployee("Ali", 50000)

print(emp1.name)
print(emp1.calculate_pay())