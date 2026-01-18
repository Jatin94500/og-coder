# Space Weather System - Simple Diagrams

## System Overview

```mermaid
graph LR
    A[Data Collection] --> B[Processing]
    B --> C[ML Models]
    C --> D[Predictions]
    D --> E[Alerts & Visualization]
```

## Data Flow

```mermaid
flowchart TD
    Start[Start] --> Collect[Collect Data from APIs]
    Collect --> Process[Process & Engineer Features]
    Process --> Train[Train ML Models]
    Train --> Predict[Make Predictions]
    Predict --> Alert{High Risk?}
    Alert -->|Yes| Send[Send Alert]
    Alert -->|No| Monitor[Continue Monitoring]
    Send --> Monitor
    Monitor --> Collect
```

## Model Architecture

```mermaid
graph TB
    subgraph Input
        I1[Solar Wind Speed]
        I2[Proton Density]
        I3[Magnetic Field]
        I4[X-ray Flux]
    end
    
    subgraph Models
        M1[XGBoost<br/>Flare Predictor]
        M2[LSTM<br/>Storm Forecaster]
        M3[LightGBM<br/>Risk Assessor]
    end
    
    subgraph Output
        O1[Flare Probability]
        O2[Kp Index Forecast]
        O3[Risk Score]
    end
    
    I1 --> M1
    I2 --> M1
    I3 --> M1
    I4 --> M1
    
    I1 --> M2
    I2 --> M2
    I3 --> M2
    
    I1 --> M3
    I2 --> M3
    I3 --> M3
    I4 --> M3
    
    M1 --> O1
    M2 --> O2
    M3 --> O3
```

## Alert System

```mermaid
flowchart TD
    A[New Data] --> B{Flare Prob > 70%?}
    B -->|Yes| C[HIGH Alert]
    B -->|No| D{Kp > 5?}
    D -->|Yes| E[Storm Alert]
    D -->|No| F{Risk > 7?}
    F -->|Yes| G[Satellite Alert]
    F -->|No| H[Normal]
    
    C --> I[Send Notification]
    E --> I
    G --> I
    H --> J[Update Dashboard]
    I --> J
```

## Sequence Diagram

```mermaid
sequenceDiagram
    participant User
    participant System
    participant API
    participant Models
    
    User->>System: Start Monitoring
    loop Every 15 min
        System->>API: Fetch Data
        API-->>System: Space Weather Data
        System->>Models: Make Predictions
        Models-->>System: Results
        System->>User: Update Dashboard
        
        alt High Risk
            System->>User: Send Alert
        end
    end
```

## State Diagram

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Collecting: Start
    Collecting --> Processing: Data Ready
    Processing --> Predicting: Valid Data
    Predicting --> Alerting: High Risk
    Predicting --> Monitoring: Normal
    Alerting --> Monitoring: Alert Sent
    Monitoring --> Collecting: Next Cycle
    Monitoring --> Idle: Stop
    Idle --> [*]
```

## Component Diagram

```mermaid
graph TB
    subgraph Frontend
        UI[Web Dashboard]
        API_Client[API Client]
    end
    
    subgraph Backend
        Server[FastAPI Server]
        Scheduler[Background Jobs]
    end
    
    subgraph ML
        Flare[Flare Model]
        Storm[Storm Model]
        Risk[Risk Model]
    end
    
    subgraph Data
        DB[(Database)]
        Cache[(Redis)]
    end
    
    UI --> Server
    API_Client --> Server
    Server --> Flare
    Server --> Storm
    Server --> Risk
    Scheduler --> Flare
    Scheduler --> Storm
    Server --> DB
    Server --> Cache
```

---

**Note**: These diagrams will render automatically on GitHub, GitLab, and most markdown viewers that support Mermaid.
