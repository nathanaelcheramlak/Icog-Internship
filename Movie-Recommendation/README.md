# Movie Recommendation System

## Overview
This project is a full-stack Movie Recommendation System designed to provide personalized movie suggestions to users. It leverages modern web technologies for the frontend and robust Python-based APIs and data processing for the backend. The system supports user authentication, movie browsing, rating, and advanced recommendation algorithms.

## Features
- **User Authentication:** Secure signup, login, and profile management.
- **Movie Search & Browse:** Explore movies, view details, and search by title or genre.
- **Rating & Reviews:** Users can rate movies and view their rated list.
- **Personalized Recommendations:** Multiple recommendation engines including collaborative filtering, context-based, and new user suggestions.
- **Data Management:** Efficient handling and cleaning of movie, ratings, and tags datasets.
- **Modern UI:** Responsive React frontend with Tailwind CSS for a seamless user experience.

## Project Structure
```
Movie-Recommendation/
├── client/           # Frontend (React, Vite, Tailwind)
│   ├── src/
│   │   ├── components/   # Reusable UI components
│   │   ├── pages/        # App pages (Home, Login, Profile, etc.)
│   │   ├── contexts/     # React Contexts (e.g., Auth)
│   │   ├── services/     # API service layer
│   │   └── utils/        # Utility functions
│   └── ...
├── server/           # Backend (Python, FastAPI/Flask, Neo4j, SQLite)
│   ├── auth/         # Authentication logic
│   ├── data/         # Raw and cleaned datasets
│   ├── database/     # Database connectors and utilities
│   ├── movies/       # Movie routes and logic
│   ├── recommendation/ # Recommendation engines
│   ├── utils/        # Shared utilities
│   └── app.py        # Main backend entry point
└── README.md         # Project documentation
```

## Setup Instructions
### Prerequisites
- Node.js & pnpm (for frontend)
- Python 3.10+ (for backend)
- Neo4j (for graph-based recommendations)
- SQLite (for relational data)

### Backend Setup
1. Navigate to the backend folder:
   ```powershell
   cd server
   ```
2. Install Python dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
3. Configure environment variables in `.env` as needed.
4. Start the backend server:
   ```powershell
   python app.py
   ```

### Frontend Setup
1. Navigate to the client folder:
   ```powershell
   cd client
   ```
2. Install dependencies:
   ```powershell
   pnpm install
   ```
3. Start the development server:
   ```powershell
   pnpm run dev
   ```

## Data Sources
- [MovieLens Dataset](https://grouplens.org/datasets/movielens/)
  - `movies.csv`, `ratings.csv`, `tags.csv`, `links.csv`
- Cleaned versions available in `server/data/clean/`

## Recommendation Algorithms
- **Collaborative Filtering:** Suggests movies based on user similarity.
- **Context-Based:** Uses user context and preferences.
- **New User Recommendations:** Handles cold-start problem for new users.
- **Additional Engines:** Extensible architecture for more algorithms.

## Technologies Used
- **Frontend:** React, Vite, Tailwind CSS
- **Backend:** Python, FastAPI/Flask, Neo4j, SQLite
- **Data:** Pandas, CSV, Graph Databases

## Contributing
Contributions are welcome! Please fork the repository, create a feature branch, and submit a pull request. For major changes, open an issue first to discuss your ideas.

## License
This project is licensed under the MIT License.

## Acknowledgements
- [MovieLens](https://grouplens.org/datasets/movielens/) for the dataset
- All contributors and open-source libraries used

---
For questions or support, please open an issue or contact the maintainer.
