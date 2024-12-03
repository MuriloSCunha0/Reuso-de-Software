from abc import ABC, abstractmethod

# Sujeito (Subject)
class WeatherStation:
    def __init__(self):
        self._observers = []  # Lista de observadores
        self._temperature = 0

    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self):
        for observer in self._observers:
            observer.update(self._temperature)

    def set_temperature(self, temperature):
        print(f"[Estação] Nova temperatura registrada: {temperature}°C")
        self._temperature = temperature
        self.notify_observers()

# Observador (Observer)
class Observer(ABC):
    @abstractmethod
    def update(self, temperature):
        pass

# Painel Digital
class DigitalPanel(Observer):
    def update(self, temperature):
        print(f"[Painel Digital] Temperatura atualizada: {temperature}°C")

# Aplicativo Mobile
class MobileApp(Observer):
    def __init__(self, alert_threshold):
        self.alert_threshold = alert_threshold

    def update(self, temperature):
        if temperature > self.alert_threshold:
            print(f"[App Mobile] Alerta! Temperatura ultrapassou {self.alert_threshold}°C: {temperature}°C")

# Simulação
if __name__ == "__main__":
    # Instância do sujeito
    weather_station = WeatherStation()

    # Instâncias dos observadores
    panel = DigitalPanel()
    app = MobileApp(alert_threshold=30)

    # Registrar observadores
    weather_station.add_observer(panel)
    weather_station.add_observer(app)

    # Atualizar temperatura
    weather_station.set_temperature(25)  # Notifica painel e app
    weather_station.set_temperature(32)  # Notifica painel e dispara alerta no app
