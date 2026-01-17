# 🌌 Space Weather Prediction System - Flow Diagrams

## 1. Overall System Architecture

```mermaid
graph TB
    subgraph "Data Sources"
        A1[NOAA SWPC API]
        A2[NASA DONKI API]
        A3[GOES Satellite]
    end
    
    subgraph "Data Collection Layer"
        B[SpaceWeatherDataCollector]
    end
    
    subgraph "Data Processing"
        C[Feature Engineering]
        D[Data Validation]
        E[Synthetic Data Generator]
    end
    
    subgraph "Machine Learning Models"
        F1[Solar Flare Predictor<br/>XGBoost]
        F2[Geomagnetic Storm Forecaster<br/>LSTM]
        F3[Satellite Risk Assessor<br/>LightGBM]
    end
    
    subgraph "Output Layer"
        G1[Predictions & Forecasts]
        G2[Risk Assessment]
        G3[Alert System]
        G4[Visualizations]
    end
    
    subgraph "Storage"
        H1[(Model Files)]
        H2[(CSV Exports)]
        H3[(Training Data)]
    end
    
    A1 --> B
    A2 --> B
    A3 --> B
    B --> C
    C --> D
    E --> D
    D --> F1
    D --> F2
    D --> F3
    F1 --> G1
    F2 --> G1
    F3 --> G2
    G1 --> G3
    G2 --> G3
    G1 --> G4
    G2 --> G4
    F1 -.Save.-> H1
    F2 -.Save.-> H1
    F3 -.Save.-> H1
    G1 -.Export.-> H2
    G2 -.Export.-> H2
    E -.Generate.-> H3
```

## 2. Data Collection Flow

```mermaid
flowchart LR
    A[Start Data Collection] --> B{API Available?}
    B -->|Yes| C[Fetch Solar Wind Data]
    B -->|No| D[Use Cached Data]
    C --> E[Fetch Geomagnetic Data]
    E --> F[Fetch X-ray Flux]
    F --> G[Fetch Proton Flux]
    G --> H[Fetch Magnetometer Data]
    H --> I[Combine All Data]
    D --> I
    I --> J{Data Valid?}
    J -->|Yes| K[Return DataFrame]
    J -->|No| L[Log Error]
    L --> M[Return Empty/Partial Data]
    K --> N[End]
    M --> N
```

## 3. Machine Learning Pipeline

```mermaid
flowchart TD
    A[Raw Data Input] --> B[Feature Engineering]
    B --> C[Data Preprocessing]
    C --> D[Train/Test Split]
    
    D --> E1[Solar Flare Model]
    D --> E2[Storm Forecast Model]
    D --> E3[Risk Assessment Model]
    
    E1 --> F1[XGBoost Training]
    E2 --> F2[LSTM Training]
    E3 --> F3[LightGBM Training]
    
    F1 --> G1[Model Evaluation]
    F2 --> G2[Model Evaluation]
    F3 --> G3[Model Evaluation]
    
    G1 --> H{Performance OK?}
    G2 --> H
    G3 --> H
    
    H -->|Yes| I[Save Models]
    H -->|No| J[Tune Hyperparameters]
    J --> F1
    J --> F2
    J --> F3
    
    I --> K[Deploy for Predictions]
```

## 4. Prediction & Alert Flow

```mermaid
flowchart TD
    A[New Data Arrives] --> B[Load Trained Models]
    B --> C[Preprocess Data]
    
    C --> D1[Flare Prediction]
    C --> D2[Storm Forecast]
    C --> D3[Risk Assessment]
    
    D1 --> E{Flare Prob > 70%?}
    D2 --> F{Kp Index > 5?}
    D3 --> G{Risk > 7?}
    
    E -->|Yes| H1[🔴 HIGH Alert]
    E -->|No| I1[Check Moderate]
    F -->|Yes| H2[🔴 Storm Alert]
    F -->|No| I2[Monitor]
    G -->|Yes| H3[🔴 Satellite Alert]
    G -->|No| I3[Normal Ops]
    
    I1 --> J{Prob > 40%?}
    J -->|Yes| K1[🟡 MODERATE Alert]
    J -->|No| L1[🟢 LOW]
    
    H1 --> M[Generate Alert]
    H2 --> M
    H3 --> M
    K1 --> M
    
    M --> N[Send Notifications]
    N --> O[Update Dashboard]
    O --> P[Log Event]
    
    L1 --> O
    I2 --> O
    I3 --> O
```

## 5. Real-Time Monitoring System

```mermaid
sequenceDiagram
    participant User
    participant System
    participant DataCollector
    participant Models
    participant AlertSystem
    participant Dashboard
    
    User->>System: Start Monitoring
    
    loop Every 15 minutes
        System->>DataCollector: Fetch Latest Data
        DataCollector->>DataCollector: Query NOAA/NASA APIs
        DataCollector-->>System: Return Space Weather Data
        
        System->>Models: Make Predictions
        Models->>Models: Flare Prediction
        Models->>Models: Storm Forecast
        Models->>Models: Risk Assessment
        Models-->>System: Return Predictions
        
        System->>AlertSystem: Check Alert Conditions
        
        alt High Risk Detected
            AlertSystem->>User: 🔴 Send Alert
            AlertSystem->>Dashboard: Update Status
        else Moderate Risk
            AlertSystem->>User: 🟡 Send Warning
            AlertSystem->>Dashboard: Update Status
        else Normal Conditions
            AlertSystem->>Dashboard: Update Status
        end
        
        Dashboard-->>User: Display Real-time Data
    end
```

## 6. Model Training Workflow

```mermaid
stateDiagram-v2
    [*] --> DataGeneration
    DataGeneration --> FeatureEngineering
    FeatureEngineering --> DataValidation
    
    DataValidation --> TrainFlareModel
    DataValidation --> TrainStormModel
    DataValidation --> TrainRiskModel
    
    TrainFlareModel --> EvaluateFlare
    TrainStormModel --> EvaluateStorm
    TrainRiskModel --> EvaluateRisk
    
    EvaluateFlare --> CheckPerformance
    EvaluateStorm --> CheckPerformance
    EvaluateRisk --> CheckPerformance
    
    CheckPerformance --> SaveModels: All Pass
    CheckPerformance --> TuneHyperparameters: Failed
    
    TuneHyperparameters --> TrainFlareModel
    TuneHyperparameters --> TrainStormModel
    TuneHyperparameters --> TrainRiskModel
    
    SaveModels --> [*]
```

## 7. Data Processing Pipeline

```mermaid
graph LR
    A[Raw Data] --> B[Remove Duplicates]
    B --> C[Handle Missing Values]
    C --> D[Normalize Features]
    D --> E[Create Time Features]
    E --> F[Calculate Derivatives]
    F --> G[Add Rolling Statistics]
    G --> H[Classify Events]
    H --> I[Create Sequences]
    I --> J[Scale Data]
    J --> K[Ready for Training]
    
    style A fill:#ff6b6b
    style K fill:#51cf66
```

## 8. Alert System Decision Tree

```mermaid
graph TD
    A[Analyze Current Conditions] --> B{Solar Wind Speed}
    B -->|> 700 km/s| C[🟡 High Speed Stream]
    B -->|< 700 km/s| D{IMF Bz}
    
    D -->|< -10 nT| E[🔴 Geoeffective]
    D -->|> -10 nT| F{Kp Index}
    
    F -->|>= 7| G[🔴 Strong Storm]
    F -->|>= 5| H[🟡 Minor Storm]
    F -->|< 5| I{Flare Probability}
    
    I -->|> 70%| J[🔴 High Flare Risk]
    I -->|> 40%| K[🟡 Moderate Flare Risk]
    I -->|< 40%| L{Satellite Risk}
    
    L -->|> 7| M[🔴 High Satellite Risk]
    L -->|> 5| N[🟡 Elevated Risk]
    L -->|< 5| O[🟢 Normal Conditions]
    
    C --> P[Generate Alert]
    E --> P
    G --> P
    H --> P
    J --> P
    K --> P
    M --> P
    N --> P
    O --> Q[No Alert]
```

## 9. Feature Engineering Process

```mermaid
flowchart TB
    A[Input: Raw Space Weather Data] --> B[Time-based Features]
    A --> C[Statistical Features]
    A --> D[Domain Features]
    
    B --> B1[Hour of Day]
    B --> B2[Day of Year]
    B --> B3[Solar Cycle Phase]
    
    C --> C1[Rolling Mean]
    C --> C2[Rolling Std]
    C --> C3[Rate of Change]
    
    D --> D1[Storm Classification]
    D --> D2[Flare Classification]
    D --> D3[Risk Scoring]
    
    B1 --> E[Feature Matrix]
    B2 --> E
    B3 --> E
    C1 --> E
    C2 --> E
    C3 --> E
    D1 --> E
    D2 --> E
    D3 --> E
    
    E --> F[Standardization]
    F --> G[Output: Engineered Features]
```

## 10. Deployment Architecture

```mermaid
graph TB
    subgraph "User Interface"
        A1[Web Dashboard]
        A2[Mobile App]
        A3[API Clients]
    end
    
    subgraph "Application Layer"
        B1[FastAPI Server]
        B2[Streamlit Dashboard]
        B3[Background Scheduler]
    end
    
    subgraph "Business Logic"
        C1[Prediction Service]
        C2[Alert Service]
        C3[Data Service]
    end
    
    subgraph "ML Models"
        D1[Flare Model]
        D2[Storm Model]
        D3[Risk Model]
    end
    
    subgraph "Data Layer"
        E1[(PostgreSQL)]
        E2[(Redis Cache)]
        E3[Model Storage]
    end
    
    subgraph "External Services"
        F1[NOAA API]
        F2[NASA API]
        F3[Email Service]
        F4[SMS Service]
    end
    
    A1 --> B1
    A1 --> B2
    A2 --> B1
    A3 --> B1
    
    B1 --> C1
    B1 --> C2
    B2 --> C3
    B3 --> C1
    B3 --> C2
    
    C1 --> D1
    C1 --> D2
    C1 --> D3
    C2 --> F3
    C2 --> F4
    C3 --> F1
    C3 --> F2
    
    D1 --> E3
    D2 --> E3
    D3 --> E3
    
    C1 --> E1
    C2 --> E1
    C3 --> E2
```

## 11. Model Prediction Flow (Detailed)

```mermaid
sequenceDiagram
    participant Input as Input Data
    participant Prep as Preprocessor
    participant Flare as Flare Model
    participant Storm as Storm Model
    participant Risk as Risk Model
    participant Output as Output Handler
    
    Input->>Prep: Raw space weather data
    Prep->>Prep: Feature engineering
    Prep->>Prep: Normalization
    Prep->>Prep: Create sequences
    
    par Parallel Predictions
        Prep->>Flare: Processed features
        Flare->>Flare: XGBoost inference
        Flare-->>Output: Flare probability
    and
        Prep->>Storm: Time sequences
        Storm->>Storm: LSTM inference
        Storm-->>Output: Kp forecast
    and
        Prep->>Risk: Combined features
        Risk->>Risk: LightGBM inference
        Risk-->>Output: Risk score
    end
    
    Output->>Output: Combine predictions
    Output->>Output: Apply thresholds
    Output->>Output: Generate alerts
    Output-->>Input: Final predictions + alerts
```

## 12. System State Machine

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Collecting: Start Monitoring
    Collecting --> Processing: Data Received
    Processing --> Predicting: Data Valid
    Processing --> Error: Data Invalid
    Predicting --> Alerting: High Risk
    Predicting --> Monitoring: Normal
    Alerting --> Monitoring: Alert Sent
    Monitoring --> Collecting: Next Cycle
    Error --> Collecting: Retry
    Monitoring --> Idle: Stop Monitoring
    Idle --> [*]
```

---

## How to Use These Diagrams

### In Documentation
Copy the mermaid code blocks into any markdown file. GitHub, GitLab, and many documentation tools render them automatically.

### In Presentations
Use tools like:
- Mermaid Live Editor: https://mermaid.live/
- Draw.io: Import mermaid syntax
- VS Code: Mermaid preview extensions

### In README
Add to your README.md:
```markdown
## System Architecture
```mermaid
[paste diagram code here]
```
```

These diagrams provide a complete visual understanding of your Space Weather Prediction System! 🌌
