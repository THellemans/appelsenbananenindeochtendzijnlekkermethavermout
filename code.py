import math
import random
import time

GRAVITY = 1.625  # m/s^2 lunar gravity
TIME_STEP = 0.1  # seconds per simulation tick

class LunarModule:
    def __init__(self, mass, fuel_mass, thrust, burn_rate):
        self.mass = mass  # dry mass
        self.fuel_mass = fuel_mass
        self.thrust = thrust
        self.burn_rate = burn_rate  # kg/s
        self.altitude = 1500.0  # meters
        self.velocity = -10.0  # m/s (negative = downward)
        self.angle = 90.0  # degrees from horizontal
        self.time_elapsed = 0.0
        self.logs = []

    def current_mass(self):
        return self.mass + self.fuel_mass

    def apply_thrust(self, dt):
        """Apply thrust for dt seconds if fuel available."""
        if self.fuel_mass > 0:
            fuel_used = min(self.burn_rate * dt, self.fuel_mass)
            self.fuel_mass -= fuel_used
            acc = (self.thrust / self.current_mass())
            # Resolve thrust in vertical direction (assuming angle=90 is up)
            self.velocity += acc * math.sin(math.radians(self.angle)) * dt
        else:
            self.logs.append(f"No fuel at t={self.time_elapsed:.2f}s")

    def update_physics(self, dt):
        # Gravity effect
        self.velocity -= GRAVITY * dt
        self.altitude += self.velocity * dt
        self.time_elapsed += dt

    def status_report(self):
        return {
            "time": self.time_elapsed,
            "altitude": self.altitude,
            "velocity": self.velocity,
            "fuel": self.fuel_mass
        }

    def log_status(self):
        status = self.status_report()
        log_line = (
            f"T={status['time']:.1f}s | Alt={status['altitude']:.1f}m | "
            f"Vel={status['velocity']:.2f} m/s | Fuel={status['fuel']:.1f} kg"
        )
        self.logs.append(log_line)

    def print_logs(self):
        for line in self.logs:
            print(line)

def simple_autopilot(lm: LunarModule):
    """Simple landing autopilot: burns thrust if falling too quickly."""
    while lm.altitude > 0:
        if lm.velocity < -5 and lm.fuel_mass > 0:
            lm.apply_thrust(TIME_STEP)
        lm.update_physics(TIME_STEP)
        lm.log_status()
        if lm.altitude <= 0:
            break

def main():
    lm = LunarModule(mass=1500, fuel_mass=800, thrust=4500, burn_rate=5)
    simple_autopilot(lm)

    lm.print_logs()
    safe = abs(lm.velocity) < 5
    print("\nLanding result:")
    if safe:
        print("Landing was successful! 🚀")
    else:
        print("Crash landing! 💥")

if __name__ == "__main__":
    main()