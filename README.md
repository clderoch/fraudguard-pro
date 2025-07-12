# FraudGuard Pro - GitHub Repository Structure

## Repository Organization

```
fraudguard-pro/
├── README.md
├── LICENSE
├── .gitignore
├── docs/
│   ├── business-plan.md
│   ├── api-documentation.md
│   ├── user-guide.md
│   └── deployment-guide.md
├── frontend/
│   ├── index.html
│   ├── css/
│   │   ├── styles.css
│   │   └── components.css
│   ├── js/
│   │   ├── app.js
│   │   ├── charts.js
│   │   ├── ai-chat.js
│   │   └── upload.js
│   ├── assets/
│   │   ├── images/
│   │   └── icons/
│   └── components/
│       ├── dashboard.html
│       ├── upload-modal.html
│       └── transaction-detail.html
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── models/
│   │   ├── fraud_detection.py
│   │   ├── risk_scoring.py
│   │   └── ml_pipeline.py
│   ├── api/
│   │   ├── routes.py
│   │   ├── auth.py
│   │   └── transactions.py
│   ├── data/
│   │   ├── sample_transactions.csv
│   │   └── training_data.csv
│   └── utils/
│       ├── data_processing.py
│       ├── security.py
│       └── validators.py
├── ml-models/
│   ├── notebooks/
│   │   ├── data_exploration.ipynb
│   │   ├── model_training.ipynb
│   │   └── evaluation.ipynb
│   ├── trained_models/
│   │   ├── fraud_classifier.pkl
│   │   └── risk_scorer.pkl
│   └── scripts/
│       ├── train_model.py
│       ├── evaluate_model.py
│       └── deploy_model.py
├── tests/
│   ├── test_api.py
│   ├── test_models.py
│   └── test_frontend.py
├── docker/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── nginx.conf
├── scripts/
│   ├── setup.sh
│   ├── deploy.sh
│   └── backup.sh
└── .github/
    └── workflows/
        ├── ci.yml
        └── deploy.yml
```

## File Contents

### README.md
```markdown
# 🛡️ FraudGuard Pro

AI-powered fraud detection platform for small and medium-sized businesses.

## Features

- **Real-time Transaction Analysis**: AI-powered risk scoring
- **Interactive Dashboard**: Comprehensive analytics and insights
- **Smart Alerts**: Proactive fraud prevention notifications
- **AI Assistant**: Intelligent chatbot for fraud analysis
- **Easy Integration**: Simple file upload and API access

## Quick Start

### Frontend Only (Demo)
```bash
git clone https://github.com/yourusername/fraudguard-pro.git
cd fraudguard-pro/frontend
open index.html
```

### Full Stack Development
```bash
git clone https://github.com/yourusername/fraudguard-pro.git
cd fraudguard-pro
./scripts/setup.sh
```

## Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript, Chart.js
- **Backend**: Python, Flask/FastAPI
- **ML**: scikit-learn, pandas, numpy
- **Database**: PostgreSQL, Redis
- **Deployment**: Docker, AWS/GCP

## Documentation

- [Business Plan](docs/business-plan.md)
- [API Documentation](docs/api-documentation.md)
- [User Guide](docs/user-guide.md)
- [Deployment Guide](docs/deployment-guide.md)

## License

MIT License - see [LICENSE](LICENSE) file for details.
```

### .gitignore
```
# Dependencies
node_modules/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/
pip-log.txt
pip-delete-this-directory.txt

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Logs
*.log
logs/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Database
*.db
*.sqlite
*.sqlite3

# ML Models (if large)
*.pkl
*.model
*.h5

# Build outputs
dist/
build/
*.tar.gz

# Secrets
config/secrets.json
*.pem
*.key
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:80"
    volumes:
      - ./frontend:/usr/share/nginx/html
    depends_on:
      - backend

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/fraudguard
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    volumes:
      - ./backend:/app

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=fraudguard
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backend/sql:/docker-entrypoint-initdb.d
    ports:
      - "5432:5432"

  redis:
    image: redis:6-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

### backend/requirements.txt
```
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
redis==5.0.1
pandas==2.1.3
numpy==1.25.2
scikit-learn==1.3.2
joblib==1.3.2
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0
pytest==7.4.3
pytest-asyncio==0.21.1
```

### backend/app.py
```python
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import pandas as pd
import numpy as np
from models.fraud_detection import FraudDetector
from api.routes import router
import uvicorn

app = FastAPI(title="FraudGuard Pro API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api/v1")

# Serve static files
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

# Initialize fraud detector
fraud_detector = FraudDetector()

@app.get("/")
async def root():
    return {"message": "FraudGuard Pro API is running"}

@app.post("/api/v1/analyze-transactions")
async def analyze_transactions(file: UploadFile = File(...)):
    try:
        # Read uploaded file
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        
        # Analyze transactions
        results = fraud_detector.analyze_batch(df)
        
        return {
            "status": "success",
            "total_transactions": len(df),
            "high_risk_count": len(results[results['risk_score'] > 70]),
            "results": results.to_dict('records')
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### ml-models/fraud_detection.py
```python
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, roc_auc_score
import joblib

class FraudDetector:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_columns = [
            'amount', 'hour', 'day_of_week', 'merchant_category',
            'payment_method', 'device_score', 'location_risk'
        ]
    
    def preprocess_data(self, df):
        """Preprocess transaction data for model input"""
        # Feature engineering
        df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
        df['day_of_week'] = pd.to_datetime(df['timestamp']).dt.dayofweek
        
        # Risk scoring features
        df['amount_zscore'] = np.abs((df['amount'] - df['amount'].mean()) / df['amount'].std())
        df['velocity_risk'] = self._calculate_velocity_risk(df)
        
        return df[self.feature_columns]
    
    def train(self, training_data):
        """Train the fraud detection model"""
        X = self.preprocess_data(training_data)
        y = training_data['is_fraud']
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train ensemble model
        self.model = GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=6,
            random_state=42
        )
        
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred_proba = self.model.predict_proba(X_test_scaled)[:, 1]
        auc_score = roc_auc_score(y_test, y_pred_proba)
        
        print(f"Model AUC Score: {auc_score:.4f}")
        
        return self.model
    
    def predict_risk_score(self, transaction_data):
        """Predict risk score for a single transaction"""
        if self.model is None:
            raise ValueError("Model not trained. Call train() first.")
        
        X = self.preprocess_data(transaction_data)
        X_scaled = self.scaler.transform(X)
        
        # Get probability of fraud (0-1) and convert to risk score (0-100)
        fraud_probability = self.model.predict_proba(X_scaled)[:, 1]
        risk_score = (fraud_probability * 100).astype(int)
        
        return risk_score[0] if len(risk_score) == 1 else risk_score
    
    def analyze_batch(self, df):
        """Analyze a batch of transactions"""
        risk_scores = self.predict_risk_score(df)
        
        df['risk_score'] = risk_scores
        df['risk_category'] = pd.cut(
            risk_scores, 
            bins=[0, 30, 70, 100], 
            labels=['Low', 'Medium', 'High']
        )
        
        return df
    
    def save_model(self, filepath):
        """Save trained model and scaler"""
        joblib.dump({
            'model': self.model,
            'scaler': self.scaler,
            'feature_columns': self.feature_columns
        }, filepath)
    
    def load_model(self, filepath):
        """Load trained model and scaler"""
        saved_objects = joblib.load(filepath)
        self.model = saved_objects['model']
        self.scaler = saved_objects['scaler']
        self.feature_columns = saved_objects['feature_columns']
    
    def _calculate_velocity_risk(self, df):
        """Calculate velocity-based risk score"""
        # Simplified velocity calculation
        return np.random.rand(len(df)) * 0.3  # Placeholder
```

### GitHub Workflow (.github/workflows/ci.yml)
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        cd backend
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        cd backend
        pytest tests/ -v
    
    - name: Run security checks
      run: |
        pip install bandit safety
        bandit -r backend/
        safety check -r backend/requirements.txt

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to production
      run: |
        echo "Deploy to production server"
        # Add your deployment scripts here
```

## How to Set Up Your GitHub Repository

1. **Create Repository:**
   ```bash
   # On GitHub, create a new repository named "fraudguard-pro"
   git clone https://github.com/yourusername/fraudguard-pro.git
   cd fraudguard-pro
   ```

2. **Create Directory Structure:**
   ```bash
   mkdir -p frontend/{css,js,assets,components}
   mkdir -p backend/{models,api,data,utils,tests}
   mkdir -p ml-models/{notebooks,trained_models,scripts}
   mkdir -p docs docker scripts .github/workflows
   ```

3. **Add Files:**
   - Copy the HTML content into `frontend/index.html`
   - Split CSS into `frontend/css/styles.css`
   - Split JavaScript into appropriate files in `frontend/js/`
   - Add all the configuration files shown above

4. **Initialize Git:**
   ```bash
   git add .
   git commit -m "Initial commit: MVP fraud detection platform"
   git push origin main
   ```

## Working Across Sessions

Since Claude doesn't retain session data, here are strategies to maintain continuity:

1. **Document Everything**: Keep detailed README files and comments
2. **Version Control**: Use git branches for different features
3. **Reference Previous Work**: You can always share your existing code with Claude in new conversations
4. **Modular Design**: Keep components separate so they're easy to understand and modify

Would you like me to create any specific files from this structure, or help you set up a particular component?
