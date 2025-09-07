# Master Product Development Scenario Library
## 100 Foundational Scenarios for AI Work Classification

**Purpose**: This is the definitive library of product development scenarios that serves as the foundation for all AI work classification. Every work item should be matched against these scenarios first, with new scenarios only added when absolutely necessary.

**Classification Key**: `Size/Complexity/Type` where:
- **Size**: XS (<1d), S (1-3d), M (1-2w), L (2-4w), XL (1-2m), XXL (2+m)
- **Complexity**: Low, Medium, High, Critical
- **Type**: Feature, Enhancement, Bug, Infrastructure, Migration, Research, Epic

---

## 🔐 **AUTHENTICATION & SECURITY (10 scenarios)**

### AS-001: Basic User Registration
**Classification**: M/Low/Feature  
**Description**: Simple user signup with email/password, email verification, basic profile  
**Context**: Standard web application, no complex requirements  
**Examples**: "User signup form", "Email verification system", "Basic user profiles"

### AS-002: OAuth Integration (Single Provider)
**Classification**: L/Medium/Feature  
**Description**: Integrate one OAuth provider (Google, GitHub, etc.) with user profile sync  
**Context**: Web/mobile app, established OAuth libraries available  
**Examples**: "Google OAuth login", "GitHub authentication", "Facebook login integration"

### AS-003: Multi-Provider OAuth System
**Classification**: XL/High/Feature  
**Description**: Support multiple OAuth providers with unified user management  
**Context**: Enterprise application, complex user flows, provider-specific handling  
**Examples**: "Google + Microsoft + GitHub OAuth", "Social login aggregation", "Enterprise SSO"

### AS-004: Role-Based Access Control (RBAC)
**Classification**: L/Medium/Feature  
**Description**: Implement user roles, permissions, and access control throughout application  
**Context**: Multi-user application, various permission levels needed  
**Examples**: "Admin/User/Guest roles", "Permission-based UI", "Resource access control"

### AS-005: Two-Factor Authentication (2FA)
**Classification**: M/Medium/Feature  
**Description**: Add 2FA with SMS, authenticator app, or hardware token support  
**Context**: Security-conscious application, compliance requirements  
**Examples**: "SMS verification codes", "Google Authenticator integration", "Hardware token support"

### AS-006: Single Sign-On (SSO) Integration
**Classification**: XL/High/Feature  
**Description**: Enterprise SSO integration with SAML, OIDC, or Active Directory  
**Context**: Enterprise environment, complex identity provider integration  
**Examples**: "SAML SSO with Okta", "Active Directory integration", "Azure AD connection"

### AS-007: Password Security Enhancement
**Classification**: M/Medium/Enhancement  
**Description**: Improve password policies, reset flows, and security measures  
**Context**: Existing authentication system, security audit requirements  
**Examples**: "Strong password requirements", "Secure password reset", "Account lockout policies"

### AS-008: Session Management System
**Classification**: M/Medium/Feature  
**Description**: Implement secure session handling, timeouts, and multi-device management  
**Context**: Web application with user sessions, security requirements  
**Examples**: "Session timeout handling", "Multi-device login", "Session security"

### AS-009: Security Audit Implementation
**Classification**: L/High/Infrastructure  
**Description**: Implement comprehensive security logging, monitoring, and audit trails  
**Context**: Compliance requirements, security-critical application  
**Examples**: "Security event logging", "Access audit trails", "Compliance monitoring"

### AS-010: Authentication Bug Fixes
**Classification**: S/Low/Bug  
**Description**: Fix issues with login flows, session handling, or authentication edge cases  
**Context**: Existing authentication system with specific issues  
**Examples**: "Login form validation fix", "Session timeout bug", "OAuth callback error"

---

## 💳 **PAYMENT & BILLING (8 scenarios)**

### PB-001: Basic Payment Integration
**Classification**: L/Medium/Feature  
**Description**: Integrate single payment provider (Stripe, PayPal) for one-time payments  
**Context**: E-commerce or SaaS application, standard payment flows  
**Examples**: "Stripe checkout integration", "PayPal payment button", "Credit card processing"

### PB-002: Subscription Billing System
**Classification**: XL/High/Feature  
**Description**: Implement recurring billing, subscription management, plan changes  
**Context**: SaaS application, multiple subscription tiers, billing complexity  
**Examples**: "Monthly subscription billing", "Plan upgrade/downgrade", "Proration handling"

### PB-003: Multi-Currency Payment Support
**Classification**: L/High/Enhancement  
**Description**: Add support for multiple currencies with conversion and localization  
**Context**: International application, currency conversion requirements  
**Examples**: "USD/EUR/GBP support", "Currency conversion", "Localized pricing"

### PB-004: Payment Security & PCI Compliance
**Classification**: XL/Critical/Infrastructure  
**Description**: Implement PCI DSS compliance, tokenization, and payment security measures  
**Context**: Payment processing application, regulatory compliance required  
**Examples**: "PCI DSS compliance", "Payment tokenization", "Security audit requirements"

### PB-005: Refund & Dispute Management
**Classification**: M/Medium/Feature  
**Description**: Handle payment refunds, chargebacks, and dispute resolution workflows  
**Context**: Payment system with customer service requirements  
**Examples**: "Automated refund processing", "Chargeback handling", "Dispute workflow"

### PB-006: Invoice Generation System
**Classification**: M/Low/Feature  
**Description**: Generate, send, and track invoices with payment status  
**Context**: B2B application, invoice-based billing model  
**Examples**: "PDF invoice generation", "Email invoice delivery", "Payment tracking"

### PB-007: Payment Analytics & Reporting
**Classification**: M/Medium/Feature  
**Description**: Payment metrics, revenue tracking, and financial reporting  
**Context**: Business intelligence needs, financial reporting requirements  
**Examples**: "Revenue dashboards", "Payment success rates", "Financial reports"

### PB-008: Payment Bug Fixes
**Classification**: S/Medium/Bug  
**Description**: Fix payment processing errors, failed transactions, or billing issues  
**Context**: Existing payment system with transaction problems  
**Examples**: "Failed payment retry", "Billing calculation fix", "Payment form error"

---

## 🎨 **USER INTERFACE & DESIGN (12 scenarios)**

### UI-001: Component Library Creation
**Classification**: L/Low/Infrastructure  
**Description**: Build reusable UI component library with design system  
**Context**: New project or design system standardization  
**Examples**: "React component library", "Design system components", "Storybook setup"

### UI-002: Responsive Design Implementation
**Classification**: M/Low/Enhancement  
**Description**: Make existing application responsive across devices and screen sizes  
**Context**: Desktop-first application needing mobile support  
**Examples**: "Mobile responsive dashboard", "Tablet layout optimization", "Cross-device compatibility"

### UI-003: Dark Mode Implementation
**Classification**: M/Low/Feature  
**Description**: Add dark/light theme toggle with persistent user preferences  
**Context**: Modern application, user experience enhancement  
**Examples**: "Dark theme toggle", "Theme persistence", "System theme detection"

### UI-004: Accessibility Improvements
**Classification**: M/Medium/Enhancement  
**Description**: Implement WCAG compliance, keyboard navigation, screen reader support  
**Context**: Public-facing application, compliance or inclusivity requirements  
**Examples**: "WCAG 2.1 compliance", "Keyboard navigation", "Screen reader optimization"

### UI-005: Form Design & Validation
**Classification**: M/Low/Feature  
**Description**: Create complex forms with validation, error handling, and user experience  
**Context**: Data collection application, user input requirements  
**Examples**: "Multi-step forms", "Real-time validation", "Form error handling"

### UI-006: Data Visualization Dashboard
**Classification**: L/Medium/Feature  
**Description**: Build interactive dashboards with charts, graphs, and data visualization  
**Context**: Analytics application, business intelligence needs  
**Examples**: "Sales dashboard", "Analytics charts", "Interactive data visualization"

### UI-007: Mobile App UI Development
**Classification**: L/Medium/Feature  
**Description**: Design and implement mobile-specific UI patterns and interactions  
**Context**: Mobile application, touch interfaces, platform-specific design  
**Examples**: "Mobile navigation patterns", "Touch gestures", "Platform-specific UI"

### UI-008: Animation & Micro-interactions
**Classification**: S/Low/Enhancement  
**Description**: Add animations, transitions, and micro-interactions for better UX  
**Context**: Existing application, user experience enhancement  
**Examples**: "Loading animations", "Hover effects", "Page transitions"

### UI-009: Internationalization (i18n)
**Classification**: M/Medium/Feature  
**Description**: Add multi-language support with translation management  
**Context**: Global application, multiple language requirements  
**Examples**: "Multi-language support", "Translation management", "RTL language support"

### UI-010: Performance Optimization (Frontend)
**Classification**: M/High/Enhancement  
**Description**: Optimize frontend performance, loading times, and user experience  
**Context**: Performance issues, user experience problems  
**Examples**: "Bundle optimization", "Lazy loading", "Performance monitoring"

### UI-011: Cross-Browser Compatibility
**Classification**: S/Medium/Enhancement  
**Description**: Ensure application works consistently across different browsers  
**Context**: Web application with browser compatibility issues  
**Examples**: "Safari compatibility fix", "IE11 support", "Browser testing"

### UI-012: UI Bug Fixes
**Classification**: XS/Low/Bug  
**Description**: Fix visual bugs, alignment issues, styling problems  
**Context**: Existing application with visual defects  
**Examples**: "Button alignment fix", "CSS styling issue", "Layout problem"

---

## 🔌 **API DEVELOPMENT (15 scenarios)**

### API-001: REST API Basic CRUD
**Classification**: M/Low/Feature  
**Description**: Create standard REST API endpoints for basic data operations  
**Context**: Standard web application, database-backed API  
**Examples**: "User CRUD API", "Product management API", "Basic resource endpoints"

### API-002: GraphQL API Implementation
**Classification**: L/Medium/Feature  
**Description**: Design and implement GraphQL schema with resolvers and queries  
**Context**: Complex data requirements, flexible query needs  
**Examples**: "GraphQL schema design", "Resolver implementation", "Query optimization"

### API-003: API Authentication & Authorization
**Classification**: M/Medium/Feature  
**Description**: Implement API security with tokens, rate limiting, and access control  
**Context**: Public or partner API, security requirements  
**Examples**: "JWT token authentication", "API key management", "Rate limiting"

### API-004: Third-Party API Integration
**Classification**: M/Medium/Feature  
**Description**: Integrate with external APIs, handle responses, error cases  
**Context**: Application requiring external data or services  
**Examples**: "Stripe API integration", "Google Maps API", "Social media APIs"

### API-005: Webhook System Implementation
**Classification**: M/Medium/Feature  
**Description**: Create webhook endpoints for event-driven communication  
**Context**: Event-driven architecture, real-time notifications  
**Examples**: "Payment webhook handling", "User event webhooks", "System notifications"

### API-006: API Documentation & OpenAPI
**Classification**: S/Low/Infrastructure  
**Description**: Create comprehensive API documentation with interactive examples  
**Context**: API used by developers, documentation requirements  
**Examples**: "OpenAPI specification", "Interactive API docs", "Developer portal"

### API-007: API Versioning Strategy
**Classification**: M/Medium/Infrastructure  
**Description**: Implement API versioning for backward compatibility and evolution  
**Context**: Mature API with breaking changes needed  
**Examples**: "Version header handling", "Backward compatibility", "Deprecation strategy"

### API-008: Real-time API (WebSockets)
**Classification**: L/High/Feature  
**Description**: Implement real-time communication with WebSockets or Server-Sent Events  
**Context**: Real-time application requirements, live updates needed  
**Examples**: "Chat system WebSockets", "Live notifications", "Real-time collaboration"

### API-009: API Performance Optimization
**Classification**: M/High/Enhancement  
**Description**: Optimize API performance, caching, database queries  
**Context**: Performance issues, scalability requirements  
**Examples**: "Query optimization", "Caching implementation", "Response time improvement"

### API-010: API Testing & Quality Assurance
**Classification**: M/Low/Infrastructure  
**Description**: Implement comprehensive API testing with automated test suites  
**Context**: API quality assurance, CI/CD integration  
**Examples**: "Integration test suite", "API contract testing", "Performance testing"

### API-011: API Rate Limiting & Throttling
**Classification**: S/Medium/Infrastructure  
**Description**: Implement API rate limiting, quotas, and abuse prevention  
**Context**: Public API, resource protection requirements  
**Examples**: "Request rate limiting", "User quotas", "Abuse prevention"

### API-012: API Error Handling & Logging
**Classification**: S/Low/Infrastructure  
**Description**: Standardize API error responses, logging, and monitoring  
**Context**: Production API, debugging and monitoring needs  
**Examples**: "Structured error responses", "API logging", "Error monitoring"

### API-013: API Gateway Implementation
**Classification**: XL/High/Infrastructure  
**Description**: Implement API gateway for routing, security, and management  
**Context**: Microservices architecture, centralized API management  
**Examples**: "Kong API Gateway", "AWS API Gateway", "Custom routing layer"

### API-014: Microservices API Design
**Classification**: XXL/High/Epic  
**Description**: Design and implement APIs for microservices architecture  
**Context**: Large-scale application, service decomposition  
**Examples**: "Service API boundaries", "Inter-service communication", "Service mesh"

### API-015: API Bug Fixes
**Classification**: S/Low/Bug  
**Description**: Fix API endpoint bugs, response issues, or integration problems  
**Context**: Existing API with functional defects  
**Examples**: "Endpoint response fix", "Parameter validation bug", "Integration error"

---

## 🗄️ **DATABASE & DATA MANAGEMENT (12 scenarios)**

### DB-001: Basic Database Schema Design
**Classification**: M/Low/Infrastructure  
**Description**: Design database schema for new application with tables and relationships  
**Context**: New application, standard relational database needs  
**Examples**: "User/product schema", "E-commerce database design", "Content management schema"

### DB-002: Database Migration (Schema Changes)
**Classification**: M/Medium/Migration  
**Description**: Add/modify database columns, tables, or constraints with data preservation  
**Context**: Existing application, schema evolution needs  
**Examples**: "Add user preferences table", "Modify product schema", "Index optimization"

### DB-003: Zero-Downtime Database Migration
**Classification**: XL/Critical/Migration  
**Description**: Major database changes without service interruption  
**Context**: Production system, high availability requirements  
**Examples**: "MySQL to PostgreSQL migration", "Schema restructuring", "Platform migration"

### DB-004: Database Performance Optimization
**Classification**: L/High/Enhancement  
**Description**: Optimize database queries, indexes, and performance bottlenecks  
**Context**: Performance issues, scalability requirements  
**Examples**: "Query optimization", "Index tuning", "Database scaling"

### DB-005: Data Import/Export System
**Classification**: M/Medium/Feature  
**Description**: Build system for bulk data import/export with validation  
**Context**: Data migration needs, bulk operations required  
**Examples**: "CSV import system", "Data export tools", "Bulk data processing"

### DB-006: Database Backup & Recovery
**Classification**: M/Medium/Infrastructure  
**Description**: Implement automated backup, recovery, and disaster recovery procedures  
**Context**: Production system, data protection requirements  
**Examples**: "Automated backups", "Point-in-time recovery", "Disaster recovery"

### DB-007: Database Monitoring & Analytics
**Classification**: M/Low/Infrastructure  
**Description**: Implement database monitoring, metrics, and performance analytics  
**Context**: Production database, operational visibility needs  
**Examples**: "Database metrics", "Query performance monitoring", "Capacity planning"

### DB-008: Data Archival System
**Classification**: L/Medium/Feature  
**Description**: Implement data archival for old records with retrieval capabilities  
**Context**: Large dataset, compliance or performance requirements  
**Examples**: "Old data archival", "Historical data access", "Compliance data retention"

### DB-009: Database Security & Encryption
**Classification**: L/High/Infrastructure  
**Description**: Implement database encryption, access controls, and security measures  
**Context**: Sensitive data, compliance requirements (GDPR, HIPAA)  
**Examples**: "Data encryption at rest", "Database access controls", "Audit logging"

### DB-010: Multi-Database Integration
**Classification**: XL/High/Infrastructure  
**Description**: Integrate multiple databases or data sources with synchronization  
**Context**: Complex data architecture, multiple data sources  
**Examples**: "Multi-database queries", "Data synchronization", "Federated data access"

### DB-011: Database Sharding/Partitioning
**Classification**: XXL/Critical/Infrastructure  
**Description**: Implement database sharding or partitioning for massive scale  
**Context**: High-scale application, performance at scale requirements  
**Examples**: "Horizontal sharding", "Table partitioning", "Distributed database"

### DB-012: Database Bug Fixes
**Classification**: S/Medium/Bug  
**Description**: Fix database-related bugs, query issues, or data consistency problems  
**Context**: Existing database system with functional issues  
**Examples**: "Query performance bug", "Data consistency fix", "Migration rollback"

---

## 📱 **MOBILE DEVELOPMENT (10 scenarios)**

### MOB-001: Native Mobile App Development
**Classification**: XXL/Medium/Epic  
**Description**: Build complete native mobile application for iOS and/or Android  
**Context**: New mobile product, platform-specific requirements  
**Examples**: "iOS app development", "Android app creation", "Mobile-first product"

### MOB-002: Cross-Platform Mobile App
**Classification**: XXL/High/Epic  
**Description**: Build cross-platform mobile app with React Native, Flutter, or similar  
**Context**: Multi-platform mobile product, code sharing requirements  
**Examples**: "React Native app", "Flutter development", "Xamarin application"

### MOB-003: Mobile API Integration
**Classification**: M/Medium/Feature  
**Description**: Integrate mobile app with backend APIs, handle offline scenarios  
**Context**: Mobile app with backend services, connectivity considerations  
**Examples**: "REST API integration", "Offline data sync", "Background sync"

### MOB-004: Push Notification System
**Classification**: M/Medium/Feature  
**Description**: Implement push notifications with targeting and delivery tracking  
**Context**: Mobile app, user engagement requirements  
**Examples**: "Firebase push notifications", "Targeted messaging", "Notification analytics"

### MOB-005: Mobile Authentication
**Classification**: M/Medium/Feature  
**Description**: Implement mobile-specific authentication with biometrics, device security  
**Context**: Mobile app, security and user experience requirements  
**Examples**: "Biometric authentication", "Device PIN", "Mobile OAuth"

### MOB-006: Camera/Media Integration
**Classification**: L/Medium/Feature  
**Description**: Integrate camera, photo/video capture, and media processing  
**Context**: Mobile app with media requirements  
**Examples**: "Photo capture", "Video recording", "Image processing"

### MOB-007: Location Services Integration
**Classification**: M/Medium/Feature  
**Description**: Implement GPS, maps, geolocation, and location-based features  
**Context**: Mobile app with location requirements  
**Examples**: "GPS tracking", "Map integration", "Location-based services"

### MOB-008: Mobile Performance Optimization
**Classification**: M/High/Enhancement  
**Description**: Optimize mobile app performance, memory usage, battery life  
**Context**: Performance issues, user experience problems  
**Examples**: "App performance tuning", "Memory optimization", "Battery usage"

### MOB-009: App Store Deployment
**Classification**: S/Medium/Infrastructure  
**Description**: Prepare and deploy mobile app to App Store/Play Store  
**Context**: Mobile app ready for distribution  
**Examples**: "iOS App Store submission", "Google Play deployment", "App review process"

### MOB-010: Mobile Bug Fixes
**Classification**: S/Low/Bug  
**Description**: Fix mobile-specific bugs, crashes, or platform issues  
**Context**: Existing mobile app with functional problems  
**Examples**: "App crash fix", "Platform compatibility", "UI rendering issue"

---

## 🏗️ **INFRASTRUCTURE & DEVOPS (15 scenarios)**

### INF-001: CI/CD Pipeline Setup
**Classification**: L/Medium/Infrastructure  
**Description**: Implement continuous integration and deployment pipeline  
**Context**: Development team, automated deployment needs  
**Examples**: "GitHub Actions CI/CD", "Jenkins pipeline", "GitLab CI setup"

### INF-002: Docker Containerization
**Classification**: M/Low/Infrastructure  
**Description**: Containerize application with Docker, create deployment images  
**Context**: Application deployment, containerization strategy  
**Examples**: "Dockerfile creation", "Multi-stage builds", "Container optimization"

### INF-003: Kubernetes Deployment
**Classification**: L/High/Infrastructure  
**Description**: Deploy application to Kubernetes with scaling and management  
**Context**: Container orchestration, scalable deployment  
**Examples**: "K8s deployment manifests", "Service configuration", "Ingress setup"

### INF-004: Cloud Infrastructure Setup
**Classification**: L/Medium/Infrastructure  
**Description**: Set up cloud infrastructure (AWS, Azure, GCP) for application hosting  
**Context**: Cloud deployment, infrastructure as code  
**Examples**: "AWS infrastructure", "Terraform setup", "Cloud resource provisioning"

### INF-005: Monitoring & Alerting System
**Classification**: M/Medium/Infrastructure  
**Description**: Implement application monitoring, metrics, and alerting  
**Context**: Production application, operational visibility  
**Examples**: "Application monitoring", "Alert setup", "Metrics collection"

### INF-006: Logging & Observability
**Classification**: M/Low/Infrastructure  
**Description**: Implement structured logging, log aggregation, and observability  
**Context**: Production application, debugging and monitoring needs  
**Examples**: "Centralized logging", "Log analysis", "Distributed tracing"

### INF-007: Load Balancing & Scaling
**Classification**: L/High/Infrastructure  
**Description**: Implement load balancing, auto-scaling, and high availability  
**Context**: High-traffic application, scalability requirements  
**Examples**: "Load balancer setup", "Auto-scaling configuration", "High availability"

### INF-008: Database Administration & Scaling
**Classification**: L/High/Infrastructure  
**Description**: Database scaling, replication, clustering, and administration  
**Context**: Database performance issues, scalability needs  
**Examples**: "Database clustering", "Read replicas", "Database scaling"

### INF-009: Security Infrastructure
**Classification**: L/Critical/Infrastructure  
**Description**: Implement security infrastructure, firewalls, VPNs, access controls  
**Context**: Security requirements, compliance needs  
**Examples**: "Network security", "VPN setup", "Security policies"

### INF-010: Backup & Disaster Recovery
**Classification**: M/High/Infrastructure  
**Description**: Implement comprehensive backup and disaster recovery procedures  
**Context**: Business continuity requirements, data protection  
**Examples**: "Automated backups", "Disaster recovery plan", "Data restoration"

### INF-011: Environment Management
**Classification**: S/Low/Infrastructure  
**Description**: Set up and manage development, staging, and production environments  
**Context**: Development workflow, environment consistency  
**Examples**: "Environment setup", "Configuration management", "Environment parity"

### INF-012: Performance Monitoring
**Classification**: M/Medium/Infrastructure  
**Description**: Implement performance monitoring, profiling, and optimization tools  
**Context**: Performance requirements, optimization needs  
**Examples**: "APM tools", "Performance profiling", "Bottleneck identification"

### INF-013: Infrastructure as Code
**Classification**: L/Medium/Infrastructure  
**Description**: Implement infrastructure automation with Terraform, CloudFormation, etc.  
**Context**: Infrastructure management, repeatability requirements  
**Examples**: "Terraform modules", "Infrastructure automation", "Cloud provisioning"

### INF-014: Network & DNS Configuration
**Classification**: S/Medium/Infrastructure  
**Description**: Configure networking, DNS, CDN, and connectivity  
**Context**: Application deployment, network requirements  
**Examples**: "DNS configuration", "CDN setup", "Network routing"

### INF-015: Infrastructure Bug Fixes
**Classification**: S/Medium/Bug  
**Description**: Fix infrastructure issues, deployment problems, configuration errors  
**Context**: Existing infrastructure with operational problems  
**Examples**: "Deployment script fix", "Configuration error", "Service connectivity"

---

## 🧪 **TESTING & QUALITY ASSURANCE (10 scenarios)**

### TEST-001: Unit Testing Implementation
**Classification**: M/Low/Infrastructure  
**Description**: Create comprehensive unit test suite with good coverage  
**Context**: Code quality requirements, testing strategy  
**Examples**: "Jest unit tests", "Python pytest suite", "Component testing"

### TEST-002: Integration Testing
**Classification**: M/Medium/Infrastructure  
**Description**: Implement integration tests for API endpoints and system interactions  
**Context**: System integration validation, API testing  
**Examples**: "API integration tests", "Database integration testing", "Service testing"

### TEST-003: End-to-End Testing
**Classification**: L/Medium/Infrastructure  
**Description**: Implement E2E testing with browser automation and user flow validation  
**Context**: User experience validation, regression testing  
**Examples**: "Cypress E2E tests", "Selenium automation", "User journey testing"

### TEST-004: Performance Testing
**Classification**: M/High/Infrastructure  
**Description**: Implement load testing, stress testing, and performance validation  
**Context**: Performance requirements, scalability validation  
**Examples**: "Load testing", "Stress testing", "Performance benchmarking"

### TEST-005: Security Testing
**Classification**: L/High/Infrastructure  
**Description**: Implement security testing, vulnerability scanning, penetration testing  
**Context**: Security requirements, compliance validation  
**Examples**: "Vulnerability scanning", "Penetration testing", "Security audit"

### TEST-006: Test Automation Framework
**Classification**: L/Medium/Infrastructure  
**Description**: Build test automation framework and CI/CD integration  
**Context**: Testing efficiency, automated quality gates  
**Examples**: "Test framework setup", "CI/CD test integration", "Test reporting"

### TEST-007: Mobile Testing Strategy
**Classification**: M/Medium/Infrastructure  
**Description**: Implement mobile-specific testing across devices and platforms  
**Context**: Mobile application, device compatibility requirements  
**Examples**: "Device testing", "Platform compatibility", "Mobile automation"

### TEST-008: API Contract Testing
**Classification**: S/Medium/Infrastructure  
**Description**: Implement contract testing for API providers and consumers  
**Context**: API integration, contract validation  
**Examples**: "PACT testing", "API contract validation", "Schema testing"

### TEST-009: Test Data Management
**Classification**: S/Low/Infrastructure  
**Description**: Create test data management, fixtures, and data generation  
**Context**: Testing requirements, data consistency  
**Examples**: "Test data fixtures", "Data generation", "Test environment setup"

### TEST-010: Testing Bug Fixes
**Classification**: XS/Low/Bug  
**Description**: Fix test failures, flaky tests, or testing infrastructure issues  
**Context**: Existing test suite with problems  
**Examples**: "Flaky test fix", "Test environment issue", "Test data problem"

---

## 🔄 **INTEGRATION & COMMUNICATION (8 scenarios)**

### INT-001: Message Queue Implementation
**Classification**: M/Medium/Infrastructure  
**Description**: Implement message queues for asynchronous processing and communication  
**Context**: Distributed system, asynchronous processing needs  
**Examples**: "Redis queue", "RabbitMQ setup", "AWS SQS integration"

### INT-002: Event-Driven Architecture
**Classification**: L/High/Infrastructure  
**Description**: Implement event sourcing, event-driven communication between services  
**Context**: Microservices architecture, loose coupling requirements  
**Examples**: "Event sourcing", "Domain events", "Event bus implementation"

### INT-003: File Upload & Processing
**Classification**: M/Medium/Feature  
**Description**: Implement file upload, storage, processing, and management  
**Context**: Application with file handling requirements  
**Examples**: "Image upload system", "Document processing", "File storage integration"

### INT-004: Email System Integration
**Classification**: S/Low/Feature  
**Description**: Integrate email sending, templates, and delivery tracking  
**Context**: Application with email communication needs  
**Examples**: "Transactional emails", "Email templates", "Delivery tracking"

### INT-005: Search Implementation
**Classification**: L/Medium/Feature  
**Description**: Implement search functionality with indexing and relevance scoring  
**Context**: Content-heavy application, search requirements  
**Examples**: "Elasticsearch integration", "Full-text search", "Search optimization"

### INT-006: Caching Strategy Implementation
**Classification**: M/Medium/Infrastructure  
**Description**: Implement caching layers for performance optimization  
**Context**: Performance requirements, scalability needs  
**Examples**: "Redis caching", "Application-level cache", "CDN integration"

### INT-007: External Service Integration
**Classification**: M/Medium/Feature  
**Description**: Integrate with external services, APIs, or SaaS platforms  
**Context**: Third-party service dependency, integration requirements  
**Examples**: "CRM integration", "Analytics service", "Marketing automation"

### INT-008: Integration Bug Fixes
**Classification**: S/Medium/Bug  
**Description**: Fix integration issues, API connection problems, or data sync errors  
**Context**: Existing integrations with functional problems  
**Examples**: "API connection fix", "Data sync error", "Integration timeout"

---

## 📊 **ANALYTICS & REPORTING (8 scenarios)**

### ANAL-001: Basic Analytics Implementation
**Classification**: M/Low/Feature  
**Description**: Implement basic user analytics, page views, and usage tracking  
**Context**: Application with analytics needs, user behavior tracking  
**Examples**: "Google Analytics integration", "User tracking", "Page view analytics"

### ANAL-002: Custom Analytics Dashboard
**Classification**: L/Medium/Feature  
**Description**: Build custom analytics dashboard with business-specific metrics  
**Context**: Business intelligence needs, custom reporting requirements  
**Examples**: "Sales dashboard", "User engagement metrics", "Business KPI dashboard"

### ANAL-003: Real-time Analytics
**Classification**: L/High/Feature  
**Description**: Implement real-time analytics with live data streaming and visualization  
**Context**: Real-time business monitoring, immediate insights needed  
**Examples**: "Live dashboard updates", "Real-time metrics", "Streaming analytics"

### ANAL-004: Data Warehouse Implementation
**Classification**: XL/High/Infrastructure  
**Description**: Build data warehouse with ETL processes and analytical data models  
**Context**: Large-scale analytics, business intelligence platform  
**Examples**: "Data warehouse setup", "ETL pipelines", "Analytical data models"

### ANAL-005: Reporting System
**Classification**: M/Low/Feature  
**Description**: Create automated reporting system with scheduled reports and exports  
**Context**: Business reporting needs, automated insights  
**Examples**: "Automated reports", "PDF generation", "Email report delivery"

### ANAL-006: A/B Testing Framework
**Classification**: L/Medium/Feature  
**Description**: Implement A/B testing framework for feature experimentation  
**Context**: Product optimization, experimental feature testing  
**Examples**: "Feature flag system", "Experiment tracking", "Statistical analysis"

### ANAL-007: User Behavior Analytics
**Classification**: M/Medium/Feature  
**Description**: Implement detailed user behavior tracking and analysis  
**Context**: User experience optimization, product insights  
**Examples**: "User journey tracking", "Behavior analysis", "Conversion funnels"

### ANAL-008: Analytics Bug Fixes
**Classification**: S/Low/Bug  
**Description**: Fix analytics tracking issues, reporting errors, or data accuracy problems  
**Context**: Existing analytics system with data quality issues  
**Examples**: "Tracking script fix", "Report generation error", "Data accuracy issue"

---

## 🤖 **MACHINE LEARNING & AI (8 scenarios)**

### ML-001: ML Model Development & Training
**Classification**: XL/High/Research  
**Description**: Develop, train, and validate machine learning models for specific use cases  
**Context**: AI/ML application, data science requirements  
**Examples**: "Fraud detection model", "Recommendation engine", "Predictive analytics"

### ML-002: ML Model Deployment & Serving
**Classification**: L/High/Infrastructure  
**Description**: Deploy ML models to production with serving infrastructure  
**Context**: Trained model ready for production deployment  
**Examples**: "Model serving API", "ML pipeline deployment", "Model monitoring"

### ML-003: Data Pipeline for ML
**Classification**: L/Medium/Infrastructure  
**Description**: Build data pipelines for ML training, feature engineering, and data processing  
**Context**: ML project with data processing requirements  
**Examples**: "Feature engineering pipeline", "Training data preparation", "Data validation"

### ML-004: ML Model Monitoring & Observability
**Classification**: M/High/Infrastructure  
**Description**: Implement ML model monitoring, drift detection, and performance tracking  
**Context**: Production ML models, model performance requirements  
**Examples**: "Model drift detection", "Performance monitoring", "Model retraining triggers"

### ML-005: AI/ML Feature Integration
**Classification**: L/High/Feature  
**Description**: Integrate AI/ML capabilities into existing application features  
**Context**: Application with AI enhancement opportunities  
**Examples**: "Smart recommendations", "Automated categorization", "Intelligent search"

### ML-006: Natural Language Processing
**Classification**: XL/High/Feature  
**Description**: Implement NLP features like text analysis, sentiment analysis, or chatbots  
**Context**: Text processing requirements, conversational interfaces  
**Examples**: "Chatbot implementation", "Sentiment analysis", "Text classification"

### ML-007: Computer Vision Implementation
**Classification**: XL/High/Feature  
**Description**: Implement image/video processing, object detection, or visual recognition  
**Context**: Visual content processing requirements  
**Examples**: "Image recognition", "Object detection", "Video analysis"

### ML-008: ML Research & Experimentation
**Classification**: M/Medium/Research  
**Description**: Research ML approaches, experiment with algorithms, proof of concepts  
**Context**: Exploratory ML work, algorithm evaluation  
**Examples**: "Algorithm comparison", "ML feasibility study", "Model experimentation"

---

## 🌐 **WEB DEVELOPMENT (12 scenarios)**

### WEB-001: Landing Page Development
**Classification**: S/Low/Feature  
**Description**: Create marketing landing pages with conversion optimization  
**Context**: Marketing website, lead generation  
**Examples**: "Product landing page", "Campaign page", "Sign-up page"

### WEB-002: Admin Dashboard Development
**Classification**: L/Medium/Feature  
**Description**: Build comprehensive admin dashboard for system management  
**Context**: Administrative interface needs, system management  
**Examples**: "User management dashboard", "System admin panel", "Content management"

### WEB-003: E-commerce Website
**Classification**: XXL/High/Epic  
**Description**: Build complete e-commerce website with shopping cart, checkout, payments  
**Context**: Online retail business, full e-commerce functionality  
**Examples**: "Online store", "Shopping cart system", "E-commerce platform"

### WEB-004: Content Management System
**Classification**: XL/Medium/Feature  
**Description**: Build CMS for content creation, editing, and publishing  
**Context**: Content-driven website, editorial workflow  
**Examples**: "Blog CMS", "News management", "Content publishing system"

### WEB-005: User Portal Development
**Classification**: L/Medium/Feature  
**Description**: Create user-facing portal with account management and self-service  
**Context**: User account management, self-service requirements  
**Examples**: "Customer portal", "User account dashboard", "Self-service platform"

### WEB-006: Progressive Web App (PWA)
**Classification**: L/Medium/Feature  
**Description**: Convert web application to PWA with offline capabilities  
**Context**: Mobile-web experience, offline functionality needs  
**Examples**: "PWA conversion", "Offline functionality", "App-like experience"

### WEB-007: SEO & Performance Optimization
**Classification**: M/Medium/Enhancement  
**Description**: Optimize website for search engines and performance  
**Context**: Marketing website, search visibility requirements  
**Examples**: "SEO optimization", "Page speed improvement", "Core Web Vitals"

### WEB-008: Multi-tenant SaaS Platform
**Classification**: XXL/Critical/Epic  
**Description**: Build multi-tenant SaaS platform with tenant isolation and management  
**Context**: SaaS business model, multiple customer isolation  
**Examples**: "Multi-tenant architecture", "Tenant management", "SaaS platform"

### WEB-009: Social Features Implementation
**Classification**: L/Medium/Feature  
**Description**: Add social features like sharing, comments, user interactions  
**Context**: Social application, community features  
**Examples**: "Social sharing", "Comment system", "User interactions"

### WEB-010: Web Accessibility Implementation
**Classification**: M/Medium/Enhancement  
**Description**: Implement web accessibility standards and compliance  
**Context**: Public website, accessibility requirements  
**Examples**: "WCAG compliance", "Screen reader support", "Keyboard navigation"

### WEB-011: Website Migration
**Classification**: L/High/Migration  
**Description**: Migrate website to new platform, framework, or hosting  
**Context**: Technology upgrade, platform change  
**Examples**: "Framework migration", "Hosting migration", "Platform upgrade"

### WEB-012: Web Bug Fixes
**Classification**: XS/Low/Bug  
**Description**: Fix website bugs, broken links, or functionality issues  
**Context**: Existing website with functional problems  
**Examples**: "Broken link fix", "Form submission error", "Layout issue"

---

## ⚡ **PERFORMANCE & OPTIMIZATION (6 scenarios)**

### PERF-001: Application Performance Optimization
**Classification**: M/High/Enhancement  
**Description**: Optimize application performance, response times, and resource usage  
**Context**: Performance issues, user experience problems  
**Examples**: "Code optimization", "Database query tuning", "Memory optimization"

### PERF-002: Scalability Implementation
**Classification**: L/High/Infrastructure  
**Description**: Implement horizontal/vertical scaling for increased capacity  
**Context**: Growth requirements, capacity planning  
**Examples**: "Horizontal scaling", "Load distribution", "Capacity planning"

### PERF-003: Caching Strategy Optimization
**Classification**: M/Medium/Enhancement  
**Description**: Optimize caching strategies for better performance  
**Context**: Performance bottlenecks, caching opportunities  
**Examples**: "Cache optimization", "CDN implementation", "Application caching"

### PERF-004: Database Performance Tuning
**Classification**: L/High/Enhancement  
**Description**: Optimize database performance, queries, and indexing strategies  
**Context**: Database performance issues, query optimization  
**Examples**: "Query optimization", "Index tuning", "Database scaling"

### PERF-005: Frontend Performance Optimization
**Classification**: M/Medium/Enhancement  
**Description**: Optimize frontend performance, bundle size, and loading times  
**Context**: Frontend performance issues, user experience  
**Examples**: "Bundle optimization", "Lazy loading", "Asset optimization"

### PERF-006: Performance Bug Fixes
**Classification**: S/Medium/Bug  
**Description**: Fix performance-related bugs, memory leaks, or efficiency issues  
**Context**: Existing application with performance problems  
**Examples**: "Memory leak fix", "Performance regression", "Efficiency improvement"

---

## 🔧 **MAINTENANCE & SUPPORT (5 scenarios)**

### MAINT-001: Dependency Updates
**Classification**: S/Low/Maintenance  
**Description**: Update dependencies, libraries, and framework versions  
**Context**: Security updates, dependency maintenance  
**Examples**: "Package updates", "Security patches", "Framework upgrades"

### MAINT-002: Code Refactoring
**Classification**: M/Low/Enhancement  
**Description**: Refactor code for better maintainability, readability, and structure  
**Context**: Technical debt reduction, code quality improvement  
**Examples**: "Code cleanup", "Architecture improvement", "Technical debt reduction"

### MAINT-003: Documentation Updates
**Classification**: XS/Low/Enhancement  
**Description**: Update documentation, README files, and technical guides  
**Context**: Documentation maintenance, knowledge sharing  
**Examples**: "API documentation update", "README improvement", "Technical guides"

### MAINT-004: Configuration Management
**Classification**: S/Low/Infrastructure  
**Description**: Manage application configuration, environment variables, and settings  
**Context**: Configuration maintenance, environment management  
**Examples**: "Config file updates", "Environment setup", "Settings management"

### MAINT-005: Maintenance Bug Fixes
**Classification**: XS/Low/Bug  
**Description**: Fix minor bugs, typos, or small functional issues  
**Context**: General maintenance, minor issue resolution  
**Examples**: "Typo fix", "Minor bug fix", "Small improvement"

---

## 🏢 **ENTERPRISE & COMPLIANCE (6 scenarios)**

### ENT-001: Enterprise SSO Integration
**Classification**: XL/High/Feature  
**Description**: Implement enterprise SSO with SAML, OIDC, or Active Directory  
**Context**: Enterprise customer requirements, identity provider integration  
**Examples**: "SAML SSO", "Active Directory integration", "Enterprise identity"

### ENT-002: Compliance Implementation (GDPR/HIPAA)
**Classification**: XL/Critical/Infrastructure  
**Description**: Implement compliance requirements for data protection and privacy  
**Context**: Regulatory compliance, legal requirements  
**Examples**: "GDPR compliance", "HIPAA implementation", "Data privacy controls"

### ENT-003: Audit Logging & Compliance Reporting
**Classification**: L/High/Infrastructure  
**Description**: Implement comprehensive audit logging and compliance reporting  
**Context**: Compliance requirements, audit trail needs  
**Examples**: "Audit trail logging", "Compliance reports", "Activity monitoring"

### ENT-004: Enterprise Integration (ERP/CRM)
**Classification**: XL/High/Integration  
**Description**: Integrate with enterprise systems like SAP, Salesforce, or custom ERP  
**Context**: Enterprise customer, existing system integration  
**Examples**: "Salesforce integration", "SAP connection", "ERP data sync"

### ENT-005: Multi-Region Deployment
**Classification**: XL/Critical/Infrastructure  
**Description**: Deploy application across multiple regions for compliance and performance  
**Context**: Global application, data residency requirements  
**Examples**: "Multi-region setup", "Data residency", "Global deployment"

### ENT-006: Enterprise Security Implementation
**Classification**: XL/Critical/Infrastructure  
**Description**: Implement enterprise-grade security measures and controls  
**Context**: Enterprise security requirements, threat protection  
**Examples**: "Advanced threat protection", "Security controls", "Enterprise firewall"

---

## 🔬 **RESEARCH & PROTOTYPING (6 scenarios)**

### RES-001: Technology Evaluation & POC
**Classification**: M/Medium/Research  
**Description**: Research and evaluate new technologies with proof of concept development  
**Context**: Technology decision making, feasibility assessment  
**Examples**: "Framework evaluation", "Technology spike", "Feasibility study"

### RES-002: Architecture Research & Design
**Classification**: L/Medium/Research  
**Description**: Research and design system architecture for new or existing systems  
**Context**: Architectural decisions, system design needs  
**Examples**: "Architecture design", "System design research", "Technical architecture"

### RES-003: Performance Research & Benchmarking
**Classification**: M/High/Research  
**Description**: Research performance optimization approaches and benchmark solutions  
**Context**: Performance requirements, optimization strategy  
**Examples**: "Performance benchmarking", "Optimization research", "Scalability study"

### RES-004: Security Research & Assessment
**Classification**: L/High/Research  
**Description**: Research security approaches, vulnerability assessment, threat modeling  
**Context**: Security requirements, risk assessment  
**Examples**: "Security assessment", "Threat modeling", "Vulnerability research"

### RES-005: User Experience Research
**Classification**: M/Low/Research  
**Description**: Research user experience, usability testing, and design optimization  
**Context**: User experience improvement, design decisions  
**Examples**: "UX research", "Usability testing", "Design optimization"

### RES-006: Market & Competitive Research
**Classification**: S/Low/Research  
**Description**: Research market trends, competitive analysis, and feature benchmarking  
**Context**: Product strategy, competitive positioning  
**Examples**: "Competitive analysis", "Market research", "Feature comparison"

---

## 🔄 **MIGRATION & UPGRADES (5 scenarios)**

### MIG-001: Framework/Platform Migration
**Classification**: XXL/High/Migration  
**Description**: Migrate application to new framework, platform, or technology stack  
**Context**: Technology upgrade, platform change requirements  
**Examples**: "React to Vue migration", "Python 2 to 3 upgrade", "Framework modernization"

### MIG-002: Cloud Migration
**Classification**: XL/High/Migration  
**Description**: Migrate on-premise application to cloud infrastructure  
**Context**: Cloud adoption, infrastructure modernization  
**Examples**: "AWS migration", "Azure migration", "Cloud-native transformation"

### MIG-003: Database Migration
**Classification**: L/Critical/Migration  
**Description**: Migrate database to new platform with data preservation  
**Context**: Database platform change, data migration needs  
**Examples**: "MySQL to PostgreSQL", "On-premise to cloud DB", "Database upgrade"

### MIG-004: Legacy System Modernization
**Classification**: XXL/Critical/Epic  
**Description**: Modernize legacy systems with new technology and architecture  
**Context**: Legacy system replacement, modernization initiative  
**Examples**: "Legacy app modernization", "Monolith to microservices", "System replacement"

### MIG-005: Data Migration & Transformation
**Classification**: L/High/Migration  
**Description**: Migrate and transform data between systems with validation  
**Context**: System change, data format transformation  
**Examples**: "Data format migration", "System data transfer", "Data transformation"

---

## 📋 **USAGE GUIDELINES**

### **Scenario Matching Process:**

1. **Primary Match**: Find exact scenario that matches work description
2. **Category Match**: Find scenario in same domain with similar characteristics  
3. **Pattern Match**: Find scenario with similar size/complexity/type pattern
4. **Create New**: Only if no reasonable match exists and represents truly new pattern

### **New Scenario Criteria:**
- **Unique Pattern**: Significantly different from existing scenarios
- **Recurring Need**: Will apply to multiple future work items
- **Clear Boundaries**: Distinct from similar scenarios
- **Domain Coverage**: Fills important gap in scenario library

### **Consistency Rules:**
- **Similar Work → Similar Classification**: Identical scenarios must get identical results
- **Context Sensitivity**: Same scenario with different context may have different classification
- **Boundary Clarity**: Clear criteria for when work moves between scenario categories
- **Regular Review**: Scenarios updated based on feedback patterns and usage data

---

## 🎯 **CLASSIFICATION OPTIMIZATION STRATEGY**

### **Phase 1: Foundation (Scenarios 1-30)**
Focus on most common product development patterns:
- Core web development scenarios (10)
- Basic API and database work (8)
- Essential infrastructure setup (7)
- Common bug fixes and enhancements (5)

### **Phase 2: Expansion (Scenarios 31-70)**
Add specialized and complex scenarios:
- Advanced features and integrations (15)
- Mobile and cross-platform development (10)
- Security and compliance work (10)
- Performance and optimization (10)

### **Phase 3: Excellence (Scenarios 71-100)**
Complete coverage with edge cases:
- Enterprise and large-scale scenarios (10)
- Research and experimental work (8)
- Migration and transformation projects (7)
- Specialized domain work (5)

---

## 📊 **SUCCESS METRICS**

### **Coverage Metrics:**
- **Domain Coverage**: All major product development areas represented
- **Size Distribution**: Balanced representation across XS through XXL
- **Complexity Distribution**: Adequate coverage of Low through Critical
- **Type Distribution**: All work types well represented

### **Quality Metrics:**
- **Scenario Utilization**: >90% of work matched to existing scenarios
- **Classification Consistency**: >95% identical results for scenario matches
- **Confidence Scores**: >85% average confidence for scenario-based classifications
- **User Acceptance**: >90% acceptance rate for scenario-matched classifications

### **Optimization Metrics:**
- **New Scenario Rate**: <5% of work requires new scenario creation
- **Scenario Effectiveness**: High usage and accuracy scores for each scenario
- **Pattern Recognition**: Strong correlation between scenario patterns and classification results
- **System Learning**: Continuous improvement in accuracy and consistency over time

---

**This Master Scenario Library serves as the foundation for achieving 95%+ accuracy and 90%+ consistency in AI work classification by providing comprehensive, standardized patterns that cover all product development scenarios.**
