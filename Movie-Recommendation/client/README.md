# Movie Recommendation System - Frontend

A modern React frontend for the Movie Recommendation System built with Vite, Tailwind CSS, and React Router.

## Features

- **Authentication**: User login and signup with JWT tokens
- **Movie Browsing**: Browse movies with advanced filtering and search
- **Movie Details**: Detailed movie pages with rating functionality
- **Recommendations**: AI-powered movie recommendations with multiple algorithms
- **User Profile**: User profile management and activity tracking
- **Responsive Design**: Mobile-first responsive design with Tailwind CSS

## Tech Stack

- **React 18** - Frontend framework
- **Vite** - Build tool and development server
- **Tailwind CSS** - Utility-first CSS framework
- **React Router** - Client-side routing
- **Axios** - HTTP client for API calls
- **Lucide React** - Icon library
- **React Hot Toast** - Toast notifications

## Installation

1. Navigate to the client directory:
   ```bash
   cd client
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open your browser and navigate to `http://localhost:3000`

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build

## Project Structure

```
client/
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── MovieCard.jsx   # Movie card component
│   │   ├── Navbar.jsx      # Navigation bar
│   │   └── SearchBox.jsx   # Search input component
│   ├── contexts/           # React contexts
│   │   └── AuthContext.jsx # Authentication context
│   ├── pages/              # Page components
│   │   ├── Home.jsx        # Home page
│   │   ├── Login.jsx       # Login page
│   │   ├── Signup.jsx      # Signup page
│   │   ├── Movies.jsx      # Movies listing page
│   │   ├── MovieDetail.jsx # Movie detail page
│   │   ├── Recommendations.jsx # Recommendations page
│   │   └── Profile.jsx     # User profile page
│   ├── services/           # API services
│   │   └── api.js          # API client configuration
│   ├── App.jsx             # Main app component
│   ├── main.jsx            # App entry point
│   └── index.css           # Global styles
├── index.html              # HTML template
├── package.json            # Dependencies and scripts
├── tailwind.config.js      # Tailwind configuration
├── vite.config.js          # Vite configuration
└── postcss.config.js       # PostCSS configuration
```

## API Integration

The frontend integrates with the following backend endpoints:

### Authentication
- `POST /auth/login` - User login
- `POST /auth/signup` - User registration

### Movies
- `GET /movies` - Get movies with filtering and pagination
- `GET /movies/:id` - Get movie details
- `GET /movies/search` - Search movies
- `POST /movies/rate` - Rate a movie

### Recommendations
- `GET /recommendations` - Get movie recommendations
- `GET /recommendations/profile` - Get user recommendation profile
- `GET /recommendations/similarity` - Get movie similarity
- `GET /recommendations/explain` - Explain recommendations

## Configuration

The API base URL is configured in `src/services/api.js`. By default, it's set to `/api` which is proxied to `http://localhost:5000` in the Vite configuration.

To change the API URL, update the `API_BASE_URL` constant in `src/services/api.js`.

## Features Overview

### Home Page
- Welcome message with user's name
- Search functionality
- Featured movies
- Recommended movies
- Recent movies
- Quick stats

### Movies Page
- Advanced filtering (genre, year, rating)
- Search functionality
- Grid and list view modes
- Pagination
- Movie rating

### Movie Detail Page
- Movie information and poster
- User rating functionality
- Similar movies
- External links (IMDb, TMDb)
- Recommendation explanation

### Recommendations Page
- Multiple recommendation algorithms
- Method selection
- Recommendation ranking
- User profile insights

### Profile Page
- User information management
- Activity history
- Recommendation profile
- Statistics

## Styling

The application uses Tailwind CSS for styling with a custom color palette:

- **Primary**: Blue shades (primary-50 to primary-900)
- **Secondary**: Gray shades (secondary-50 to secondary-900)
- **Accent**: Yellow for ratings, Red for favorites, etc.

Custom components are defined in `src/index.css` using Tailwind's `@layer components` directive.

## Development

1. Make sure the backend server is running on `http://localhost:5000`
2. Start the frontend development server with `npm run dev`
3. The application will be available at `http://localhost:3000`
4. Hot reload is enabled for development

## Production Build

To build for production:

```bash
npm run build
```

The built files will be in the `dist` directory.

## Troubleshooting

If you encounter issues with npm installation:

1. Clear npm cache: `npm cache clean --force`
2. Delete `node_modules` and `package-lock.json`
3. Run `npm install` again
4. If still having issues, try using `yarn` instead of `npm`

## Contributing

1. Follow the existing code style
2. Use meaningful component and variable names
3. Add comments for complex logic
4. Test your changes thoroughly
5. Ensure responsive design works on all screen sizes
