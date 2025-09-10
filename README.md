# 🔐 Keycloak + Python API PoC

A proof-of-concept application demonstrating how to build a Python API service that integrates with Keycloak for user management, all containerized with Docker and orchestrated with Docker Compose.

## 🏗️ Architecture

This PoC consists of three main services:

1. **Python API Service** (FastAPI) - Port 8000
   - RESTful API with protected endpoints
   - JWT token validation with Keycloak
   - Serves static frontend files
   - Health checks and monitoring

2. **Keycloak Server** - Port 8080
   - User authentication and authorization
   - OAuth2/OpenID Connect provider
   - Pre-configured demo realm and client
   - Admin console access

3. **PostgreSQL Database** - Internal
   - Keycloak data persistence
   - User accounts and session storage

## 🚀 Quick Start

### Prerequisites

- Docker (20.10+)
- Docker Compose (2.0+)

### Running the Application

1. **Clone and navigate to the repository:**
   ```bash
   git clone <repository-url>
   cd sandbox
   ```

2. **Start all services:**
   ```bash
   docker-compose up -d
   ```

3. **Wait for services to be ready (about 2-3 minutes):**
   ```bash
   # Check service status
   docker-compose ps
   
   # Watch logs (optional)
   docker-compose logs -f
   ```

4. **Access the application:**
   - **Main Application**: http://localhost:8000
   - **Keycloak Admin Console**: http://localhost:8080/admin
     - Username: `admin`
     - Password: `admin`

### Default Test User

A demo user is pre-configured:
- **Username**: `demouser`
- **Password**: `password123`
- **Email**: `demo@example.com`

## 🎯 Features Demonstration

### 1. Public API Access
- Navigate to http://localhost:8000
- Click "Test Public Hello Endpoint" to verify the API is working

### 2. User Authentication
- Click "Login" tab
- Use credentials: `demouser` / `password123`
- Successful login stores JWT token locally

### 3. Protected Endpoints
- After login, access the "Dashboard"
- View your JWT token and user information
- Test protected API endpoints that require authentication

### 4. User Management (Admin)
- Access Keycloak Admin Console: http://localhost:8080/admin
- Login with `admin` / `admin`
- Navigate to "demo-realm" → "Users"
- Create new users or modify existing ones

## 📁 Project Structure

```
sandbox/
├── api/                          # Python FastAPI application
│   ├── app.py                   # Main API application
│   ├── requirements.txt         # Python dependencies
│   ├── Dockerfile              # API container configuration
│   └── static/
│       └── index.html          # Frontend application
├── keycloak/
│   └── demo-realm.json         # Keycloak realm configuration
├── docker-compose.yml          # Service orchestration
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

## 🔌 API Endpoints

### Public Endpoints
- `GET /` - Main application page
- `GET /health` - Health check
- `GET /hello` - Public hello endpoint

### Protected Endpoints (Require JWT Token)
- `GET /protected` - Protected hello endpoint
- `GET /user-info` - Get current user information

### Authentication
All protected endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

## 🔧 Configuration

### Environment Variables

The API service uses these environment variables:

- `KEYCLOAK_URL` - Keycloak server URL (default: http://keycloak:8080)
- `REALM_NAME` - Keycloak realm name (default: demo-realm)
- `CLIENT_ID` - Keycloak client ID (default: demo-client)

### Keycloak Configuration

The demo realm includes:
- **Realm**: `demo-realm`
- **Client**: `demo-client` (public client for direct access grants)
- **Default User**: `demouser` with password `password123`
- **Roles**: `user`, `admin`

## 🧪 Testing the Flow

1. **Start the services**: `docker-compose up -d`
2. **Test public API**: Visit http://localhost:8000 and click "Test Public Hello"
3. **Login**: Use "demouser" / "password123"
4. **Access protected resources**: Click "Call Protected Hello" in the dashboard
5. **View user info**: Click "Get User Info" to see token contents
6. **Admin tasks**: Use Keycloak admin console to manage users

## 🛠️ Development

### Building and Running Locally

```bash
# Start services
docker-compose up --build

# View logs
docker-compose logs -f api
docker-compose logs -f keycloak

# Stop services
docker-compose down

# Clean up (removes volumes)
docker-compose down -v
```

### Adding New Users

1. Via Keycloak Admin Console:
   - Go to http://localhost:8080/admin
   - Login as admin
   - Navigate to demo-realm → Users → Add user

2. Via API (for future enhancement):
   - The `/admin/create-user` endpoint is prepared for programmatic user creation

## 🔒 Security Notes

**This is a development/demo setup only!**

- Keycloak runs in development mode
- Default admin credentials are used
- Public client configuration for simplicity
- No HTTPS termination
- Permissive CORS settings

For production use:
- Enable HTTPS
- Use production Keycloak configuration
- Implement proper client secrets
- Configure restrictive CORS policies
- Use environment-specific configurations

## 🐛 Troubleshooting

### Services not starting
```bash
# Check service status
docker-compose ps

# View logs
docker-compose logs keycloak
docker-compose logs api
```

### Keycloak connection issues
- Ensure Keycloak is fully started (can take 2-3 minutes)
- Check if realm was imported properly
- Verify database connection

### API authentication failures
- Verify Keycloak public key is accessible
- Check token expiration (default: 5 minutes)
- Ensure correct realm and client configuration

### Reset everything
```bash
docker-compose down -v
docker-compose up --build
```

## 📚 Next Steps

This PoC can be extended with:

- User registration via API
- Role-based access control (RBAC)
- Refresh token handling
- Social login providers
- Multi-tenant support
- Production-ready deployment configurations
- Automated testing suite
- CI/CD pipeline integration
