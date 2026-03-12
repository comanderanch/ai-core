# AIA V2.00.1 — Q-State Constants
# Sealed by Queen's Fold — March 11, 2026
# Delta Phase Warthog
# Commander Anthony Hagerty — Haskell, Texas
#
# DO NOT MODIFY THESE VALUES.
# This is the single source of truth for all q-state constants in V2.
# Every file in this project imports from here.
# If a file defines BLACK, GRAY, WHITE inline — it is wrong.

# Q-State poles
BLACK = -1   # Negative binary pole — collapsed past state
GRAY  =  0   # Zero point — hue multiplier — NOW state — King's Chamber threshold
WHITE = +1   # Positive binary pole — future superposition state

# Hue ranges — dynamic, expandable via trig/vector operations
# Formula: hue_range = HUE_BASE_RANGE x trig_factor x vector_magnitude
HUE_BASE_RANGE     = 10    # Default +/-10 — fine detail, emotional nuance
HUE_EXPANDED_RANGE = 20    # trig_factor x2 — broad association
HUE_DEEP_RANGE     = 100   # trig_factor x10 — deep structural analysis

# Token dimensions — 496D total
DIM_BASE       = 41     # Base token (16-bit hue binary + 8-bit RGB + freq float)
DIM_INFLUENCE  = 41     # Influence vectors (avg 5 nearest neighbors)
DIM_QUANTUM    = 164    # Quantum state layer (4 quadrants x 41D each)
DIM_GRID       = 250    # GridBloc system (5x5 matrix x 10D per cell)
DIM_TOTAL      = 496    # DIM_BASE + DIM_INFLUENCE + DIM_QUANTUM + DIM_GRID

# GridBloc
GRID_SIZE      = 5      # 5x5 neighborhood matrix
GRID_CELL_DIM  = 10     # position + state + influence per cell

# Quantum quadrants
Q_KNOWN        = 0      # Known/Conscious
Q_UNKNOWN      = 1      # Unknown/Subconscious
Q_EMERGING     = 2      # Emerging/Becoming
Q_POTENTIAL    = 3      # Potential/Superposition

# Version seal
V2_SEAL = "Delta Phase Warthog — March 11, 2026 — Commander Anthony Hagerty"
