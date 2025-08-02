# ERP Webapp API Documentation

## Overview

The ERP Webapp API is a RESTful service that provides comprehensive financial risk management functionality. All endpoints return JSON responses and use standard HTTP status codes.

**Base URL**: `http://localhost:5000/api`

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

### Token Lifecycle
- **Access Token**: Valid for 24 hours
- **Refresh Token**: Valid for 30 days (if implemented)

## Response Format

### Success Response
```json
{
  "success": true,
  "data": {
    // Response data
  },
  "message": "Operation completed successfully"
}
```

### Error Response
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable error message",
    "details": {
      // Additional error details
    }
  }
}
```

## Status Codes

- `200` - OK
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `422` - Unprocessable Entity
- `500` - Internal Server Error

## Endpoints

### Authentication

#### Register User
```http
POST /api/auth/register
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "email": "user@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "full_name": "John Doe",
      "created_at": "2024-01-01T00:00:00Z"
    },
    "tokens": {
      "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
      "token_type": "Bearer",
      "expires_in": 86400
    }
  }
}
```

#### Login User
```http
POST /api/auth/login
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "email": "user@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "full_name": "John Doe"
    },
    "tokens": {
      "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
      "token_type": "Bearer",
      "expires_in": 86400
    }
  }
}
```

#### Get User Profile
```http
GET /api/auth/profile
```

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "email": "user@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "full_name": "John Doe",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  }
}
```

#### Logout User
```http
POST /api/auth/logout
```

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "success": true,
  "message": "Successfully logged out"
}
```

### Financial Data

#### Get Financial Data
```http
GET /api/financial/data
```

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "success": true,
  "data": {
    "financial_data": {
      "id": 1,
      "user_id": 1,
      "monthly_income": 5000.00,
      "monthly_expenses": 3500.00,
      "monthly_surplus": 1500.00,
      "total_assets": 100000.00,
      "total_debt": 25000.00,
      "net_worth": 75000.00,
      "emergency_fund": 15000.00,
      "emergency_fund_months": 4.3,
      "insurance_coverage": 500000.00,
      "debt_to_income_ratio": 0.42,
      "savings_rate": 0.30,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  }
}
```

#### Update Financial Data
```http
POST /api/financial/data
```

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "monthly_income": 5000.00,
  "monthly_expenses": 3500.00,
  "total_assets": 100000.00,
  "total_debt": 25000.00,
  "emergency_fund": 15000.00,
  "insurance_coverage": 500000.00
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "financial_data": {
      // Updated financial data object
    }
  },
  "message": "Financial data updated successfully"
}
```

#### Get Risk Profile
```http
GET /api/financial/risk-profile
```

**Response:**
```json
{
  "success": true,
  "data": {
    "risk_profile": {
      "id": 1,
      "user_id": 1,
      "risk_tolerance": "moderate",
      "investment_experience": "intermediate",
      "time_horizon": 10,
      "age": 35,
      "employment_status": "full-time",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  }
}
```

#### Update Risk Profile
```http
POST /api/financial/risk-profile
```

**Request Body:**
```json
{
  "risk_tolerance": "moderate",
  "investment_experience": "intermediate",
  "time_horizon": 10,
  "age": 35,
  "employment_status": "full-time"
}
```

#### Get Financial Goals
```http
GET /api/financial/goals
```

**Response:**
```json
{
  "success": true,
  "data": {
    "goals": [
      {
        "id": 1,
        "user_id": 1,
        "goal_name": "Emergency Fund",
        "target_amount": 20000.00,
        "current_amount": 15000.00,
        "target_date": "2024-12-31",
        "priority": "high",
        "status": "in_progress",
        "progress_percentage": 75.0,
        "is_on_track": true,
        "created_at": "2024-01-01T00:00:00Z"
      }
    ]
  }
}
```

#### Create Financial Goal
```http
POST /api/financial/goals
```

**Request Body:**
```json
{
  "goal_name": "Vacation Fund",
  "target_amount": 5000.00,
  "current_amount": 1000.00,
  "target_date": "2024-06-30",
  "priority": "medium"
}
```

### Risk Assessment

#### Run Risk Assessment
```http
POST /api/risk/assess
```

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "success": true,
  "data": {
    "risk_assessment": {
      "id": 1,
      "user_id": 1,
      "liquidity_risk_score": 3.5,
      "credit_risk_score": 4.2,
      "market_risk_score": 5.8,
      "inflation_risk_score": 6.1,
      "protection_risk_score": 2.9,
      "total_risk_score": 4.5,
      "risk_level": "moderate",
      "assessment_date": "2024-01-01T00:00:00Z",
      "risk_breakdown": {
        "liquidity": {
          "score": 3.5,
          "weight": 0.25,
          "weighted_score": 0.875,
          "description": "Emergency fund provides adequate coverage"
        },
        "credit": {
          "score": 4.2,
          "weight": 0.20,
          "weighted_score": 0.84,
          "description": "Debt levels are manageable"
        }
      }
    }
  }
}
```

#### Get Risk Assessment
```http
GET /api/risk/assessment
```

**Response:**
```json
{
  "success": true,
  "data": {
    "risk_assessment": {
      // Latest risk assessment object
    }
  }
}
```

#### Get Risk History
```http
GET /api/risk/history
```

**Query Parameters:**
- `limit` (optional): Number of records to return (default: 10)
- `offset` (optional): Number of records to skip (default: 0)

**Response:**
```json
{
  "success": true,
  "data": {
    "risk_history": [
      {
        // Risk assessment objects ordered by date
      }
    ],
    "total_count": 25,
    "has_more": true
  }
}
```

#### Get Asset Allocation Recommendations
```http
GET /api/risk/recommendations/asset-allocation
```

**Response:**
```json
{
  "success": true,
  "data": {
    "recommendations": {
      "recommended_allocation": {
        "stocks": 60.0,
        "bonds": 30.0,
        "cash": 5.0,
        "real_estate": 5.0
      },
      "risk_level": "moderate",
      "total_risk_score": 4.5,
      "rationale": [
        "Balanced allocation recommended for moderate risk profile",
        "Increased equity allocation suitable for long-term growth"
      ]
    }
  }
}
```

#### Run Monte Carlo Simulation
```http
POST /api/risk/simulations
```

**Request Body:**
```json
{
  "initial_value": 100000.00,
  "expected_return": 0.07,
  "volatility": 0.15,
  "time_horizon": 10,
  "monthly_contribution": 1000.00,
  "iterations": 10000
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "simulation": {
      "id": 1,
      "user_id": 1,
      "initial_portfolio_value": 100000.00,
      "expected_return": 0.07,
      "volatility": 0.15,
      "time_horizon": 10,
      "monthly_contribution": 1000.00,
      "iterations": 10000,
      "expected_value": 285000.00,
      "success_probability": 85.5,
      "var_95": 45000.00,
      "var_99": 65000.00,
      "created_at": "2024-01-01T00:00:00Z",
      "results": {
        "percentiles": {
          "5": 180000.00,
          "25": 220000.00,
          "50": 285000.00,
          "75": 350000.00,
          "95": 420000.00
        },
        "statistics": {
          "total_return": 1.85,
          "annualized_return": 0.065,
          "max_drawdown": 15.2,
          "sharpe_ratio": 0.85
        }
      }
    }
  }
}
```

#### Get Monte Carlo Simulations
```http
GET /api/risk/simulations
```

**Response:**
```json
{
  "success": true,
  "data": {
    "simulations": [
      {
        // Simulation objects
      }
    ]
  }
}
```

### Reports

#### Generate Dashboard Report
```http
POST /api/reports/dashboard
```

**Response:**
```json
{
  "success": true,
  "data": {
    "dashboard": {
      "user_info": {
        "name": "John Doe",
        "email": "user@example.com",
        "last_updated": "2024-01-01T00:00:00Z"
      },
      "financial_summary": {
        // Financial data summary
      },
      "risk_overview": {
        // Risk assessment overview
      },
      "portfolio_projection": {
        // Latest simulation results
      },
      "goals_progress": {
        // Goals tracking data
      },
      "key_metrics": {
        // Important financial metrics
      },
      "recommendations": [
        // Personalized recommendations
      ]
    }
  }
}
```

#### Generate PDF Report
```http
POST /api/reports/pdf
```

**Response:**
```json
{
  "success": true,
  "data": {
    "report": {
      "id": 1,
      "user_id": 1,
      "report_type": "comprehensive",
      "file_path": "/tmp/reports/financial_report_1_20240101_120000.pdf",
      "created_at": "2024-01-01T00:00:00Z"
    }
  }
}
```

#### Download Report
```http
GET /api/reports/{report_id}/download
```

**Response:**
- Content-Type: application/pdf
- Content-Disposition: attachment; filename="financial_report.pdf"
- Binary PDF data

#### Get Analytics Data
```http
GET /api/reports/analytics
```

**Response:**
```json
{
  "success": true,
  "data": {
    "analytics": {
      "risk_trends": {
        "dates": ["2024-01-01", "2024-02-01"],
        "scores": [4.5, 4.2],
        "trend": "improving"
      },
      "simulation_analysis": {
        "total_simulations": 5,
        "average_success_probability": 82.3
      },
      "goals_analytics": {
        "total_goals": 3,
        "completed_goals": 1,
        "completion_rate": 33.3
      },
      "charts_data": {
        "risk_trend": {
          "labels": ["Jan", "Feb", "Mar"],
          "data": [4.5, 4.2, 4.0]
        },
        "goals_progress": {
          "labels": ["Emergency Fund", "Vacation", "Retirement"],
          "data": [75, 20, 45]
        }
      }
    }
  }
}
```

## Error Codes

### Authentication Errors
- `AUTH_001` - Invalid credentials
- `AUTH_002` - Token expired
- `AUTH_003` - Token invalid
- `AUTH_004` - User not found
- `AUTH_005` - Email already exists

### Validation Errors
- `VAL_001` - Required field missing
- `VAL_002` - Invalid email format
- `VAL_003` - Password too weak
- `VAL_004` - Invalid number format
- `VAL_005` - Date format invalid

### Business Logic Errors
- `BIZ_001` - Insufficient financial data
- `BIZ_002` - Risk assessment failed
- `BIZ_003` - Simulation parameters invalid
- `BIZ_004` - Goal target unrealistic

### System Errors
- `SYS_001` - Database connection failed
- `SYS_002` - External service unavailable
- `SYS_003` - File generation failed
- `SYS_004` - Calculation error

## Rate Limiting

The API implements rate limiting to prevent abuse:

- **Authentication endpoints**: 5 requests per minute
- **Data endpoints**: 60 requests per minute
- **Report generation**: 10 requests per hour

Rate limit headers are included in responses:
```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 59
X-RateLimit-Reset: 1640995200
```

## Webhooks (Future Feature)

Webhooks will be available for:
- Risk assessment completion
- Goal milestone reached
- Report generation complete

## SDK and Libraries

### JavaScript/TypeScript
```javascript
import { ERPWebappClient } from 'erp-webapp-sdk';

const client = new ERPWebappClient({
  baseURL: 'http://localhost:5000/api',
  apiKey: 'your-api-key'
});

// Example usage
const financialData = await client.financial.getData();
```

### Python
```python
from erp_webapp_sdk import ERPWebappClient

client = ERPWebappClient(
    base_url='http://localhost:5000/api',
    api_key='your-api-key'
)

# Example usage
financial_data = client.financial.get_data()
```

## Testing

### Postman Collection
A Postman collection is available at `/docs/postman_collection.json`

### cURL Examples

#### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password"
  }'
```

#### Get Financial Data
```bash
curl -X GET http://localhost:5000/api/financial/data \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### Run Risk Assessment
```bash
curl -X POST http://localhost:5000/api/risk/assess \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Support

For API support and questions:
- Email: api-support@yourcompany.com
- Documentation: https://docs.yourcompany.com
- Status Page: https://status.yourcompany.com

## Changelog

### v1.0.0 (2024-01-01)
- Initial API release
- Authentication endpoints
- Financial data management
- Risk assessment engine
- Monte Carlo simulations
- Report generation

### v1.1.0 (2024-02-01)
- Added goal tracking
- Enhanced risk calculations
- Improved error handling
- Rate limiting implementation

---

**Last Updated**: January 1, 2024
**API Version**: 1.1.0

