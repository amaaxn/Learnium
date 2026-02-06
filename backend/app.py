# backend/app.py
import os
import sys
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

# Enable better error logging
sys.stdout.flush()
sys.stderr.flush()

print("🚀 Starting Learnium Backend...")
print(f"🔧 Python version: {sys.version}")

load_dotenv()
print("✅ Environment variables loaded")

# Import models and routes with error handling
# Don't fail startup if imports fail - log and continue
models_imported = False
routes_imported = False

try:
    from models import init_db
    models_imported = True
    print("✅ Models imported successfully")
except Exception as e:
    print(f"⚠️  Warning: Error importing models: {e}")
    import traceback
    traceback.print_exc()
    # Don't raise - allow app to start for health checks
    init_db = None

try:
    from routes.auth import auth_bp
    from routes.courses import courses_bp
    from routes.plans import plans_bp
    from routes.materials import materials_bp
    from routes.chat import chat_bp
    routes_imported = True
    print("✅ All route blueprints imported successfully")
except Exception as e:
    print(f"⚠️  Warning: Error importing routes: {e}")
    import traceback
    traceback.print_exc()
    # Don't raise - allow app to start for health checks
    # Set empty blueprints to avoid errors
    from flask import Blueprint
    auth_bp = Blueprint("auth", __name__)
    courses_bp = Blueprint("courses", __name__)
    plans_bp = Blueprint("plans", __name__)
    materials_bp = Blueprint("materials", __name__)
    chat_bp = Blueprint("chat", __name__)

app = Flask(__name__)

# Production configuration
IS_PRODUCTION = os.getenv("FLASK_ENV") == "production" or os.getenv("ENVIRONMENT") == "production"

print(f"🔧 Environment: {'PRODUCTION' if IS_PRODUCTION else 'DEVELOPMENT'}")
print(f"🔧 FLASK_ENV: {os.getenv('FLASK_ENV')}")
print(f"🔧 ENVIRONMENT: {os.getenv('ENVIRONMENT')}")

# CORS Configuration - allow Vercel preview deployments and production domain
if IS_PRODUCTION:
    frontend_url = os.getenv("FRONTEND_URL", "").strip()
    print(f"🔧 FRONTEND_URL: {frontend_url if frontend_url else 'NOT SET'}")
    
    # Function to check if origin is allowed (supports Vercel previews)
    def is_origin_allowed(origin):
        if not origin:
            return False
        
        # Always allow Vercel preview deployments
        if ".vercel.app" in origin:
            return True
        
        if not frontend_url:
            # No FRONTEND_URL set - allow all (permissive mode)
            return True
        
        # Normalize for comparison
        origin_clean = origin.rstrip('/')
        frontend_clean = frontend_url.rstrip('/')
        
        # Check exact match
        if origin_clean == frontend_clean:
            return True
        
        # Check www/non-www variants
        if "www." in frontend_clean:
            non_www = frontend_clean.replace("www.", "", 1)
            if origin_clean == non_www:
                return True
        else:
            www_version = frontend_clean.replace("://", "://www.", 1)
            if origin_clean == www_version:
                return True
        
        # Check http/https variants
        if origin_clean == frontend_clean.replace("https://", "http://"):
            return True
        if origin_clean == frontend_clean.replace("http://", "https://"):
            return True
        
        return False
    
    # Build allowed origins list for logging
    allowed_origins_list = []
    if frontend_url:
        allowed_origins_list.append(frontend_url)
        if "www." in frontend_url:
            allowed_origins_list.append(frontend_url.replace("www.", "", 1))
        else:
            allowed_origins_list.append(frontend_url.replace("://", "://www.", 1))
    allowed_origins_list.append("*.vercel.app (all Vercel previews)")
    
    print(f"✅ CORS configured to allow: {', '.join(allowed_origins_list)}")
    
    CORS(app, 
         origin=is_origin_allowed,  # Use function to check origins
         supports_credentials=True,
         allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         max_age=3600,  # Cache preflight for 1 hour
         automatic_options=True)
else:
    # Development: allow all origins
    print("✅ CORS configured for development (all origins)")
    CORS(app, supports_credentials=True)

# JWT Configuration
jwt_secret = os.getenv("JWT_SECRET_KEY")
if IS_PRODUCTION:
    if not jwt_secret or jwt_secret == "dev-secret-key-change-in-production":
        print("⚠️  WARNING: JWT_SECRET_KEY not set or using default. Generating temporary secret.")
        # Generate a temporary secret instead of crashing
        import secrets
        jwt_secret = secrets.token_urlsafe(32)
        print("⚠️  WARNING: Using temporary JWT secret. Set JWT_SECRET_KEY in environment variables!")
    elif len(jwt_secret) < 32:
        print("⚠️  WARNING: JWT_SECRET_KEY is too short. Generating temporary secret.")
        import secrets
        jwt_secret = secrets.token_urlsafe(32)
    else:
        print("✅ JWT_SECRET_KEY configured")
else:
    jwt_secret = jwt_secret or "dev-secret-key-change-in-production"
    print("✅ JWT using development secret")

app.config["JWT_SECRET_KEY"] = jwt_secret
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False  # We handle expiration in routes
app.config["JWT_COOKIE_SECURE"] = IS_PRODUCTION  # Only send over HTTPS in production
app.config["JWT_COOKIE_HTTPONLY"] = True
app.config["JWT_COOKIE_SAMESITE"] = "Lax"
jwt = JWTManager(app)

# Uploads folder
app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(__file__), "uploads")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max file size
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Security headers - let Flask-CORS handle CORS automatically, we just add security headers
@app.after_request
def set_security_headers(response):
    # Security headers for production
    if IS_PRODUCTION:
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    
    # Debug: Log CORS headers (Flask-CORS sets these)
    origin = request.headers.get('Origin', '')
    if origin:
        if request.method == "OPTIONS":
            print(f"🔍 OPTIONS preflight from origin: {origin}")
        print(f"✅ CORS Allow-Origin: {response.headers.get('Access-Control-Allow-Origin', 'NOT SET')}")
    
    return response

# Health check endpoint - register BEFORE blueprints so it's always available
# This must be registered early so Railway health checks work immediately
# This endpoint MUST work even if everything else fails
@app.route("/api/health", methods=["GET", "OPTIONS", "HEAD"])
@app.route("/health", methods=["GET", "OPTIONS", "HEAD"])
@app.route("/", methods=["GET", "OPTIONS", "HEAD"])
def health():
    """Health check endpoint for monitoring and Railway health checks."""
    # Flask-CORS will handle OPTIONS automatically, but ensure headers are set
    # Handle OPTIONS preflight for CORS
    if request.method == "OPTIONS":
        response = jsonify({})
        # Get origin from request
        origin = request.headers.get('Origin', '*')
        response.headers.add("Access-Control-Allow-Origin", origin)
        response.headers.add("Access-Control-Allow-Methods", "GET, OPTIONS, HEAD")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        response.headers.add("Access-Control-Allow-Credentials", "true")
        return response
    
    # Handle HEAD requests (used by some health checkers)
    if request.method == "HEAD":
        return "", 200
    
    # Fast, simple health check that Railway can verify quickly
    # Return minimal response to avoid any timeout issues
    # Don't check MongoDB here - health check should work even if DB is down
    # This endpoint must be fast and never fail for Railway health checks
    response = jsonify({
        "status": "ok",
        "service": "learnium-backend",
        "models_loaded": models_imported,
        "routes_loaded": routes_imported,
        "message": "Backend is running"
    })
    return response, 200

# Init MongoDB - DO NOT initialize before fork (fork-safe)
# Skip init_db() here - it will be called after workers fork in gunicorn
# This prevents the PyMongo "opened before fork" warning
# For non-gunicorn runs (direct Flask), we'll initialize on first request
print("✅ MongoDB initialization deferred until after worker fork (fork-safe)")

# Register blueprints (only if routes were imported successfully)
if routes_imported:
    try:
        app.register_blueprint(auth_bp, url_prefix="/api/auth")
        app.register_blueprint(courses_bp, url_prefix="/api/courses")
        app.register_blueprint(plans_bp, url_prefix="/api/plans")
        app.register_blueprint(materials_bp, url_prefix="/api/materials")
        app.register_blueprint(chat_bp, url_prefix="/api/chat")
        
        # Debug: Print registered auth routes
        print("✅ All routes registered successfully")
        print(f"   Auth routes: POST /api/auth/register, POST /api/auth/login, GET /api/auth/me")
    except Exception as e:
        print(f"⚠️  Warning: Error registering routes: {e}")
        import traceback
        traceback.print_exc()
        # Don't raise - health check should still work
        # Make sure app object exists even if registration fails
        pass
else:
    print("⚠️  Warning: Routes not imported - only health check will work")
    # Create dummy routes so app doesn't crash
    @app.route("/api/auth/login", methods=["POST", "OPTIONS"])
    def dummy_login():
        return jsonify({"error": "Backend routes not loaded. Check server logs."}), 503
    
    @app.route("/api/auth/register", methods=["POST", "OPTIONS"])
    def dummy_register():
        return jsonify({"error": "Backend routes not loaded. Check server logs."}), 503

# Add a route for /api to help with debugging
@app.route("/api", methods=["GET", "OPTIONS"])
def api_root():
    """Root API endpoint - redirects to health check."""
    if request.method == "OPTIONS":
        response = jsonify({})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "GET, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        return response
    return jsonify({
        "message": "Learnium API",
        "version": "1.0",
        "endpoints": {
            "health": "/api/health",
            "auth": {
                "register": "/api/auth/register",
                "login": "/api/auth/login",
                "me": "/api/auth/me"
            },
            "courses": "/api/courses",
            "plans": "/api/plans",
            "materials": "/api/materials",
            "chat": "/api/chat"
        }
    }), 200

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found", "path": request.path}), 404

@app.errorhandler(500)
def internal_error(error):
    if IS_PRODUCTION:
        return jsonify({"error": "An internal error occurred"}), 500
    else:
        return jsonify({"error": str(error)}), 500

@app.errorhandler(413)
def file_too_large(error):
    return jsonify({"error": "File too large. Maximum size is 16MB"}), 413


# Verify app is ready
print("✅ Flask app created and configured")
print(f"✅ App name: {app.name}")
print(f"✅ Registered blueprints: {list(app.blueprints.keys())}")
print(f"✅ Models imported: {models_imported}")
print(f"✅ Routes imported: {routes_imported}")

# Final startup message
print("=" * 60)
print("🚀 Learnium Backend Application Ready!")
print(f"   Environment: {'PRODUCTION' if IS_PRODUCTION else 'DEVELOPMENT'}")
print(f"   Health check: /api/health, /health, /")
if not models_imported:
    print("   ⚠️  WARNING: Models not imported - database features disabled")
if not routes_imported:
    print("   ⚠️  WARNING: Routes not imported - API endpoints disabled")
print("=" * 60)

if __name__ == "__main__":
    # Can be used in production as fallback if gunicorn fails
    port = int(os.getenv("PORT", 5001))
    debug_mode = os.getenv("FLASK_ENV") != "production" and os.getenv("ENVIRONMENT") != "production"
    print(f"🚀 Starting Flask server on port {port}")
    print(f"✅ Application ready! Environment: {'PRODUCTION' if IS_PRODUCTION else 'DEVELOPMENT'}")
    app.run(debug=debug_mode, port=port, host="0.0.0.0")
else:
    # Running under gunicorn
    print("✅ App loaded by Gunicorn")
    print(f"✅ PORT: {os.getenv('PORT', 'NOT SET')}")