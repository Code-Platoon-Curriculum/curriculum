# Full Stack Flow Diagram

This is a [mermaid](https://mermaid.js.org/) sequence diagram showing how data flows from the client to the server, through the Django backend to the database, and back to the client (browser).

```mermaid
sequenceDiagram
    box Frontend Client Application
        participant B as Browser DOM
        participant V as React Virtual DOM
        participant UI as React UI Components
        participant S as React State Logic
    end
    box Django REST Framework Backend
        participant CO as CORS
        participant UR as URLs
        participant A as Authentication
        participant P as Permissions
        participant V2 as Views
        participant SE as Serializers
        participant M as Models
        participant D as Database
    end

    B->>UI: DOM Events
    UI->>S: Update State
    S->>UI: State Changes
    UI->>V: Virtual DOM Updates
    V->>B: DOM Reconciliation
    
    Note over B,D: Data Flow
    UI->>CO: API Request
    CO->>UR: Process Request
    UR->>A: Route
    A->>P: Authenticate
    P->>V2: Authorize
    V2->>SE: Get Data
    SE->>M: Validate
    M->>D: Query
    D->>M: Return Results
    M->>SE: Map Data
    SE->>S: JSON Response
    S->>UI: Update UI
    UI->>V: Virtual DOM Updates
    V->>B: DOM Reconciliation
```