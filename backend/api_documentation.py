"""
API Documentation Generator
Generates OpenAPI/Swagger documentation for all endpoints
"""

from typing import Dict, List, Any, Optional
import json
import inspect
from flask import Flask

class APIDocGenerator:
    """Generate OpenAPI 3.0 documentation"""
    
    def __init__(self, app: Flask):
        self.app = app
        self.spec = {
            "openapi": "3.0.0",
            "info": {
                "title": "EduBot Smart Assistant API",
                "version": "2.0.0",
                "description": "Comprehensive AI-powered educational chatbot with advanced features",
                "contact": {
                    "name": "EduBot Team",
                    "email": "support@edubot.com"
                },
                "license": {
                    "name": "MIT",
                    "url": "https://opensource.org/licenses/MIT"
                }
            },
            "servers": [
                {
                    "url": "http://localhost:5000",
                    "description": "Development server"
                },
                {
                    "url": "https://api.edubot.com",
                    "description": "Production server"
                }
            ],
            "tags": [
                {"name": "Authentication", "description": "User authentication and authorization"},
                {"name": "Chat", "description": "Chat and conversation endpoints"},
                {"name": "Security", "description": "Security features and validation"},
                {"name": "Admin", "description": "Administrative functions"},
                {"name": "Lecture", "description": "Lecture note management"},
                {"name": "I18n", "description": "Internationalization"},
                {"name": "Analytics", "description": "Analytics and monitoring"}
            ],
            "paths": {},
            "components": {
                "securitySchemes": {
                    "bearerAuth": {
                        "type": "http",
                        "scheme": "bearer",
                        "bearerFormat": "JWT",
                        "description": "JWT authentication token"
                    },
                    "sessionAuth": {
                        "type": "apiKey",
                        "in": "cookie",
                        "name": "session",
                        "description": "Session cookie authentication"
                    }
                },
                "schemas": self._get_schemas()
            }
        }
    
    def _get_schemas(self) -> Dict[str, Any]:
        """Get common data schemas"""
        return {
            "User": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "integer"},
                    "username": {"type": "string"},
                    "email": {"type": "string", "format": "email"},
                    "role": {"type": "string", "enum": ["user", "admin"]},
                    "is_active": {"type": "boolean"},
                    "created_at": {"type": "string", "format": "date-time"}
                }
            },
            "LoginRequest": {
                "type": "object",
                "required": ["username", "password"],
                "properties": {
                    "username": {"type": "string"},
                    "password": {"type": "string", "format": "password"}
                }
            },
            "LoginResponse": {
                "type": "object",
                "properties": {
                    "success": {"type": "boolean"},
                    "access_token": {"type": "string"},
                    "refresh_token": {"type": "string"},
                    "user": {"$ref": "#/components/schemas/User"}
                }
            },
            "Error": {
                "type": "object",
                "properties": {
                    "error": {"type": "string"},
                    "message": {"type": "string"},
                    "status_code": {"type": "integer"}
                }
            },
            "ChatMessage": {
                "type": "object",
                "properties": {
                    "message": {"type": "string"},
                    "timestamp": {"type": "string", "format": "date-time"},
                    "user_id": {"type": "integer"}
                }
            },
            "ChatResponse": {
                "type": "object",
                "properties": {
                    "response": {"type": "string"},
                    "html": {"type": "string"},
                    "timestamp": {"type": "string", "format": "date-time"}
                }
            }
        }
    
    def generate_auth_endpoints(self):
        """Generate authentication endpoint documentation"""
        self.spec["paths"]["/auth/login"] = {
            "post": {
                "tags": ["Authentication"],
                "summary": "User login",
                "description": "Authenticate user and receive JWT tokens",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/LoginRequest"}
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Successful login",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/LoginResponse"}
                            }
                        }
                    },
                    "401": {
                        "description": "Invalid credentials",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Error"}
                            }
                        }
                    }
                }
            }
        }
        
        self.spec["paths"]["/auth/register"] = {
            "post": {
                "tags": ["Authentication"],
                "summary": "User registration",
                "description": "Register a new user account",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "required": ["username", "email", "password"],
                                "properties": {
                                    "username": {"type": "string", "minLength": 3},
                                    "email": {"type": "string", "format": "email"},
                                    "password": {"type": "string", "minLength": 8}
                                }
                            }
                        }
                    }
                },
                "responses": {
                    "201": {"description": "User created successfully"},
                    "400": {"description": "Validation error"}
                }
            }
        }
        
        self.spec["paths"]["/auth/me"] = {
            "get": {
                "tags": ["Authentication"],
                "summary": "Get current user",
                "description": "Get authenticated user information",
                "security": [{"bearerAuth": []}],
                "responses": {
                    "200": {
                        "description": "User information",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "user": {"$ref": "#/components/schemas/User"}
                                    }
                                }
                            }
                        }
                    },
                    "401": {"description": "Unauthorized"}
                }
            }
        }
    
    def generate_chat_endpoints(self):
        """Generate chat endpoint documentation"""
        self.spec["paths"]["/api/chat"] = {
            "post": {
                "tags": ["Chat"],
                "summary": "Send chat message",
                "description": "Send a message to the chatbot and receive response",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/ChatMessage"}
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Chat response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ChatResponse"}
                            }
                        }
                    }
                }
            }
        }
    
    def generate_full_spec(self) -> Dict[str, Any]:
        """Generate complete OpenAPI specification"""
        self.generate_auth_endpoints()
        self.generate_chat_endpoints()
        return self.spec
    
    def save_to_file(self, filename: str = 'api_documentation.json'):
        """Save OpenAPI spec to JSON file"""
        spec = self.generate_full_spec()
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(spec, f, indent=2)
        print(f"[OK] API documentation saved to {filename}")
    
    def get_swagger_ui_html(self) -> str:
        """Generate Swagger UI HTML page"""
        return '''
<!DOCTYPE html>
<html>
<head>
    <title>EduBot API Documentation</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">
    <style>
        body { margin: 0; padding: 0; }
    </style>
</head>
<body>
    <div id="swagger-ui"></div>
    <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
    <script>
        window.onload = function() {
            SwaggerUIBundle({
                url: '/api/docs/spec',
                dom_id: '#swagger-ui',
                deepLinking: true,
                presets: [
                    SwaggerUIBundle.presets.apis,
                    SwaggerUIBundle.SwaggerUIStandalonePreset
                ]
            });
        };
    </script>
</body>
</html>
        '''


def init_api_docs(app: Flask):
    """Initialize API documentation routes"""
    from flask import jsonify, Response
    
    doc_generator = APIDocGenerator(app)
    
    @app.route('/api/docs')
    def api_docs():
        """Swagger UI documentation page"""
        return Response(doc_generator.get_swagger_ui_html(), mimetype='text/html')
    
    @app.route('/api/docs/spec')
    def api_docs_spec():
        """OpenAPI specification JSON"""
        return jsonify(doc_generator.generate_full_spec())
    
    print("[OK] API Documentation available at /api/docs")
    
    # Save to file for external tools
    try:
        doc_generator.save_to_file('static/api_documentation.json')
    except Exception as e:
        print(f"[WARNING] Could not save API docs to file: {e}")
    
    return doc_generator
