# Movie Recommendation System

A comprehensive movie recommendation system with a Flask backend and React frontend, featuring AI-powered recommendations, user authentication, and a modern web interface.

## 🎬 Features

### Backend (Flask)
- **User Authentication**: JWT-based authentication with secure password hashing
- **Movie Management**: CRUD operations for movies with Neo4j database
- **Rating System**: User movie rating functionality
- **Recommendation Engine**: Multiple recommendation algorithms:
  - Collaborative Filtering
  - Content-Based Filtering
  - Hybrid Approach
  - Popular Movies
- **Search & Filtering**: Advanced movie search with genre, year, and rating filters
- **RESTful API**: Well-documented API endpoints

### Frontend (React)
- **Modern UI**: Built with React 18, Vite, and Tailwind CSS
- **Responsive Design**: Mobile-first responsive design
- **User Authentication**: Login and signup forms
- **Movie Browsing**: Advanced filtering and search functionality
- **Movie Details**: Detailed movie pages with rating system
- **Recommendations**: Interactive recommendation system
- **User Profile**: Profile management and activity tracking

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Neo4j Database
- Git

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Movie-Recommendation
   ```

2. **Set up Python environment**
   ```bash
   cd server
   python -m venv venv
   venv\Scripts\activate  # Windows
   # or
   source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Neo4j database**
   - Install Neo4j Desktop or Community Edition
   - Create a new database
   - Update connection details in `database/neo4j_connection.py`

5. **Load sample data**
   ```bash
   python data/scripts/load_data.py
   ```

6. **Start the server**
   ```bash
   python app.py
   ```

The backend will be available at `http://localhost:5000`

### Frontend Setup

1. **Navigate to client directory**
   ```bash
   cd client
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```
   
   If you encounter issues, try:
   ```bash
   # Windows
   install.bat
   
   # Or manually
   npm cache clean --force
   npm install --legacy-peer-deps
   ```

3. **Start the development server**
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:3000`

## 📁 Project Structure

```
Movie-Recommendation/
├── server/                 # Flask backend
│   ├── auth/              # Authentication module
│   ├── movies/            # Movie management
│   ├── recommendation/    # Recommendation engine
│   ├── database/          # Database connections
│   ├── data/              # Data processing scripts
│   └── utils/             # Utility functions
├── client/                # React frontend
│   ├── src/
│   │   ├── components/    # Reusable components
│   │   ├── pages/         # Page components
│   │   ├── contexts/      # React contexts
│   │   ├── services/      # API services
│   │   └── utils/         # Utility functions
│   └── public/            # Static assets
└── README.md
```

## 🔧 API Endpoints

### Authentication
- `POST /auth/login` - User login
- `POST /auth/signup` - User registration

### Movies
- `GET /movies` - Get movies with filtering
- `GET /movies/:id` - Get movie details
- `GET /movies/search` - Search movies
- `POST /movies/rate` - Rate a movie

### Recommendations
- `GET /recommendations` - Get recommendations
- `GET /recommendations/profile` - Get user profile
- `GET /recommendations/similarity` - Get movie similarity
- `GET /recommendations/explain` - Explain recommendations

## 🎨 Frontend Features

### Pages
- **Home**: Dashboard with featured movies and recommendations
- **Movies**: Browse and search movies with advanced filtering
- **Movie Detail**: Detailed movie information with rating
- **Recommendations**: AI-powered movie recommendations
- **Profile**: User profile and activity management

### Components
- **MovieCard**: Reusable movie display component
- **SearchBox**: Advanced search functionality
- **Navbar**: Responsive navigation
- **AuthContext**: Authentication state management

## 🛠️ Technologies Used

### Backend
- **Flask**: Python web framework
- **Neo4j**: Graph database for movie relationships
- **SQLite**: User authentication database
- **JWT**: JSON Web Tokens for authentication
- **Pandas**: Data processing
- **NumPy**: Numerical computations

### Frontend
- **React 18**: Frontend framework
- **Vite**: Build tool and dev server
- **Tailwind CSS**: Utility-first CSS framework
- **React Router**: Client-side routing
- **Axios**: HTTP client
- **Lucide React**: Icon library

## 📊 Recommendation Algorithms

1. **Collaborative Filtering**: Based on similar users' preferences
2. **Content-Based Filtering**: Based on movie features and genres
3. **Hybrid Approach**: Combines collaborative and content-based methods
4. **Popular Movies**: Most popular movies overall

## 🔒 Security Features

- JWT token-based authentication
- Password hashing with bcrypt
- CORS configuration
- Input validation and sanitization
- Secure API endpoints

## 🚀 Deployment

### Backend Deployment
1. Set up production database
2. Configure environment variables
3. Use a WSGI server like Gunicorn
4. Set up reverse proxy with Nginx

### Frontend Deployment
1. Build the production bundle: `npm run build`
2. Serve static files with a web server
3. Configure API proxy for production

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Troubleshooting

### Common Issues

1. **Neo4j Connection Issues**
   - Ensure Neo4j is running
   - Check connection credentials
   - Verify database exists

2. **Frontend Installation Issues**
   - Clear npm cache: `npm cache clean --force`
   - Delete `node_modules` and `package-lock.json`
   - Try `npm install --legacy-peer-deps`

3. **API Connection Issues**
   - Ensure backend is running on port 5000
   - Check CORS configuration
   - Verify API endpoints

## 📞 Support

For support and questions, please open an issue in the repository.

---

**Happy Movie Discovery! 🍿**
