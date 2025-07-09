from .Fighter import Fighter

import numpy as np

class EloSystem:
    def __init__(self, K: int) -> None:
        self.K = K

    def softmax(self, x: np.ndarray) -> np.ndarray:
        e_x = np.exp(x)
        return e_x / e_x.sum()

    def expected_domain_win_probability(self, B_s: np.ndarray, A_s: np.ndarray) -> np.ndarray:
        assert isinstance(B_s, np.ndarray), "B_s must be a NumPy array"
        assert isinstance(A_s, np.ndarray), "A_s must be a NumPy array"
        assert B_s.shape == A_s.shape, "A_s and B_s must have the same shape"

        return 1 / (1 + 10**((B_s - A_s) / 400))
    
    def update_fighter_elos(self,
                            winner: str,

                            fighter_a     : Fighter,
                            A_Sgn_strikes : float,
                            A_Td          : float,
                            A_Ctrl        : float,


                            fighter_b     : Fighter,
                            B_Sgn_strikes : float,
                            B_Td          : float,
                            B_Ctrl        : float,
                            ) -> None:
        
        # Get each fighters domain vectors
        A_domain_vector: np.ndarray = fighter_a.get_elo_vector()
        B_domain_vector: np.ndarray = fighter_b.get_elo_vector()

        # Find domain win probabilities
        A_domain_win_prob: np.ndarray = self.expected_domain_win_probability(A_domain_vector, B_domain_vector)
        B_domain_win_prob: np.ndarray = 1 - A_domain_win_prob

        # Build the domain heuristics
        A_domain_heuristics: np.ndarray = np.array([A_Sgn_strikes, A_Td, A_Ctrl], dtype=np.float64)
        B_domain_heuristics: np.ndarray = np.array([B_Sgn_strikes, B_Td, B_Ctrl], dtype=np.float64)

        # Find the S_A vector for both fighters
        winning_vector: np.ndarray = np.array([1, 1, 1], dtype=np.float64)
        lose_vector   : np.ndarray = np.array([0, 0, 0], dtype=np.float64)

        fighter_a_S_A : np.ndarray
        fighter_b_S_A : np.ndarray

        if fighter_a.name == winner:
            fighter_a_S_A = winning_vector
            fighter_b_S_A = lose_vector
        elif fighter_b.name == winner:
            fighter_b_S_A = winning_vector
            fighter_a_S_A = lose_vector
        else:
            raise RuntimeError(f"[ELO SYSTEM] NO WINNER NAME MATCHES ANY FIGHTER: winner: {winner}, fighter a: {fighter_a}, fighter_b: {fighter_b}")
        
        # Finally compute the updated Elo Vectors
        fighter_a.update_elo((A_domain_vector + self.K * self.softmax(A_domain_heuristics) * (fighter_a_S_A - A_domain_win_prob)))
        fighter_b.update_elo((B_domain_vector + self.K * self.softmax(B_domain_heuristics) * (fighter_b_S_A - B_domain_win_prob)))


