import os

# direktori utama backend
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# folder data CSV
DATA_DIR = os.path.join(BASE_DIR, "data")

# path lengkap untuk CSV hasil labeling
DATA_PATH = os.path.join(DATA_DIR, "questions_labeled.csv")

# alamat frontend (untuk CORS)
FRONTEND_ORIGIN = "http://localhost:5173"
import os

# direktori utama backend
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# folder data CSV
DATA_DIR = os.path.join(BASE_DIR, "data")

# path lengkap untuk CSV hasil labeling
DATA_PATH = os.path.join(DATA_DIR, "questions_labeled.csv")

# alamat frontend (untuk CORS)
FRONTEND_ORIGIN = "http://localhost:5173"
