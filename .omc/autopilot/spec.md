# EBS Infrastructure Redesign - Specification

**Generated**: 2026-02-02
**Phase**: Expansion Complete

---

## 1. Requirements Analysis (Analyst)

### 1.1 Core Transformation

| Aspect | Current (RFID Project) | Target (Infrastructure) |
|--------|------------------------|------------------------|
| Core Goal | Card Recognition → Display | Data Flow Center for Poker Production |
| Scope | RFID + Overlay | Data Production/Storage/Distribution/Analytics |
| API Direction | WSOP+ → EBS (Consume) | EBS → Other Systems (Provide) |
| SLA | 4-hour uptime | 99.9% availability |
| Scalability | Single table | N concurrent tables |
| Data Ownership | Self-consumption | Lifecycle management, access control |

### 1.2 Infrastructure Requirements

1. **Event Streaming** - Real-time event publishing
2. **Data Lake Integration** - ETL to analytics platform
3. **Multi-tenant Support** - Independent operation per event/venue
4. **Monitoring/Alerting** - Infrastructure monitoring
5. **Audit Trail** - All data change logs
6. **API Gateway** - External access management

### 1.3 Missing Definitions

- **SLA**: 99.9% availability (monthly downtime < 43.8 min)
- **RPO**: Max 1 hand data loss
- **RTO**: < 5 min service recovery
- **Concurrent Tables**: 10
- **API Response**: p95 < 500ms

---

## 2. Technical Specification (Architect)

### 2.1 Target 5-Layer Architecture

```
PRESENTATION LAYER → API LAYER → PROCESSING LAYER → DATA LAYER → HARDWARE LAYER
```

### 2.2 Stage-wise Infrastructure

| Stage | Infrastructure | Features |
|-------|---------------|----------|
| 0 | Monitoring basics | E2E latency |
| 1 | API Gateway, Event logging | Trustless Mode |
| 2 | Message Queue, Multi-table | WSOP+ sync |
| 3 | Event Sourcing, Data Lake | Automation |

---

## 3. Implementation Plan

### Documents to Create/Update
1. `INFRA-EBS-Platform-Architecture.md` - 신규
2. `PRD-0003-EBS-RFID-System.md` - 인프라 관점 추가
3. `CONCEPT-EBS-Vision.md` - 플랫폼 관점 강화

**Status**: Ready for Execution
