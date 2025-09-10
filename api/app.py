from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import requests
from jose import jwt, JWTError
from typing import Optional
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Keycloak PoC API", version="1.0.0")

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security scheme
security = HTTPBearer()

# Keycloak configuration
KEYCLOAK_URL = os.getenv("KEYCLOAK_URL", "http://keycloak:8080")
REALM_NAME = os.getenv("REALM_NAME", "demo-realm")
CLIENT_ID = os.getenv("CLIENT_ID", "demo-client")

def get_keycloak_public_key():
    """Get Keycloak public key for token validation"""
    try:
        url = f"{KEYCLOAK_URL}/realms/{REALM_NAME}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()["public_key"]
    except Exception as e:
        logger.error(f"Failed to get Keycloak public key: {e}")
        return None

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token from Keycloak"""
    token = credentials.credentials
    
    try:
        # Get public key
        public_key = get_keycloak_public_key()
        if not public_key:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Cannot verify token - Keycloak unavailable"
            )
        
        # Format the public key
        public_key_formatted = f"-----BEGIN PUBLIC KEY-----\n{public_key}\n-----END PUBLIC KEY-----"
        
        # Decode and verify the token
        payload = jwt.decode(
            token, 
            public_key_formatted, 
            algorithms=["RS256"],
            audience="account"
        )
        
        return payload
    except JWTError as e:
        logger.error(f"Token verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    except Exception as e:
        logger.error(f"Token verification error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token verification failed"
        )

# Mount static files for frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main page"""
    try:
        with open("static/index.html", "r") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="""
        <html>
            <body>
                <h1>Keycloak PoC API</h1>
                <p>API is running! Frontend files not found.</p>
                <p>Available endpoints:</p>
                <ul>
                    <li>GET /health - Health check</li>
                    <li>GET /hello - Public hello endpoint</li>
                    <li>GET /protected - Protected endpoint (requires token)</li>
                    <li>GET /user-info - Get user info from token</li>
                </ul>
            </body>
        </html>
        """)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running"}

@app.get("/hello")
async def public_hello():
    """Public hello endpoint"""
    return {"message": "Hello from the public API!"}

@app.get("/protected")
async def protected_hello(user_data: dict = Depends(verify_token)):
    """Protected endpoint that requires authentication"""
    username = user_data.get("preferred_username", "unknown")
    return {
        "message": f"Hello {username}! This is a protected endpoint.",
        "user_id": user_data.get("sub"),
        "email": user_data.get("email")
    }

@app.get("/user-info")
async def get_user_info(user_data: dict = Depends(verify_token)):
    """Get user information from the token"""
    return {
        "user_id": user_data.get("sub"),
        "username": user_data.get("preferred_username"),
        "email": user_data.get("email"),
        "first_name": user_data.get("given_name"),
        "last_name": user_data.get("family_name"),
        "roles": user_data.get("realm_access", {}).get("roles", [])
    }

@app.post("/admin/create-user")
async def create_user_endpoint():
    """Endpoint for creating users - placeholder for now"""
    return {"message": "User creation endpoint - to be implemented"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)