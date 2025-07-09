import matplotlib.pyplot as plt
import numpy as np

class Fighter:
    def __init__(self, name: str, init_elo: int=1500) -> None:
        self.name : str = name
        self.elo  : np.ndarray = np.array([init_elo, init_elo, init_elo], dtype=np.float64)

        # This is to track progression over time
        self.historical_elo: list[np.ndarray] = [self.elo.copy()]

    def visualise_progression(self) -> None:
        elos = np.vstack(self.historical_elo)

        plt.plot(elos[:, 0], label="Striking Elo")
        plt.plot(elos[:, 1], label="Grappling Elo")
        plt.plot(elos[:, 2], label="Wrestling Elo")

        plt.title(f"{self.name} Elo Progression Over Time")
        plt.xlabel("Fight Number")
        plt.ylabel("Elo Rating")
        plt.legend()
        plt.grid(True)
        plt.show()

    def get_origin_elo(self) -> np.float64:
        return np.linalg.norm(self.elo)
    
    def get_elo_vector(self) -> np.ndarray:
        return self.elo
    
    def update_elo(self, new_elo_vector: np.ndarray) -> None:
        self.historical_elo.append(self.elo.copy())
        self.elo = new_elo_vector