# Comprehensive Diff Report: CTFd vs CTFd-HIKARI

## Executive Summary

CTFd-HIKARI is a specialized cybersecurity training platform built on top of CTFd, designed specifically for Blue Team competitions focused on log analysis and threat detection. It transforms the standard CTF experience into a dynamic, real-time incident response simulation environment.

## 1. Core Architectural Changes

### **Platform Purpose**
- **CTFd**: General-purpose Capture The Flag platform
- **CTFd-HIKARI**: Specialized Blue Team cybersecurity training platform

### **Competition Model**
- **CTFd**: Static challenges with predetermined flags
- **CTFd-HIKARI**: Dynamic log injection based on team progression

### **Team Isolation**
- **CTFd**: Shared challenge environment
- **CTFd-HIKARI**: Isolated Zerotier networks per team with dedicated Kibana spaces

## 2. New Features and Functionality

### **HIKARI Plugin System**
- **hikari-plugin**: Main management interface with competition controls
- **hikari_challenge**: Custom challenge type for log analysis
- **Dynamic Log Injection**: Real-time streaming via Kafka to ELK stack
- **Progressive Challenge Unlocking**: Prerequisite-based challenge chains

### **External Integrations**
- **Kibana**: Automated dashboard provisioning per team
- **Elasticsearch**: Centralized log storage and analysis
- **Zerotier**: Network isolation and team connectivity
- **Kafka**: Real-time log streaming infrastructure

### **Enhanced Admin Features**
- Competition lifecycle management (start/stop/reset)
- Zerotier network assignment and management
- Team notification system
- Bulk user credential generation
- Custom import/export for HIKARI competitions

## 3. User Interface and Experience

### **Modern Theme Architecture**
- **CTFd**: Bootstrap 4 + jQuery
- **CTFd-HIKARI**: Bootstrap 5 + Alpine.js + Vite

### **Visual Improvements**
- Portuguese localization with cultural adaptation
- Dark/light mode toggle with system preference detection
- Modern login page with split-screen design
- Enhanced navigation with light theme
- Professional green gradient branding

### **New UI Components**
- User statistics dashboard
- Competition status indicators
- Challenge dependency visualization
- Team collaboration tools
- Real-time notification system

## 4. Technical Implementation Changes

### **Database Extensions**
```sql
-- New tables in HIKARI
CREATE TABLE zerotier (id, name, network_id);
CREATE TABLE zerotier_config (team_id, zerotier_id);
CREATE TABLE json_log_files (id, name, content);
CREATE TABLE hikari_challenge_model (
    id,
    logs_activated BOOLEAN,
    is_first_challenge BOOLEAN,
    logs_filename TEXT,
    chall_logs JSON
);
```

### **New API Endpoints**
- `GET /admin/hikari` - Competition dashboard
- `GET /admin/hikari/init-competition` - Start competition
- `GET /admin/hikari/reset-competition` - Reset competition
- `POST /admin/set-zerotier-config` - Network management
- `POST /admin/hikari-notify` - Team notifications

### **Enhanced Security**
- Network isolation per team via Zerotier
- Kibana space-based data separation
- Automated credential generation
- Role-based access control for monitoring tools

## 5. Infrastructure and Deployment

### **Container Architecture**
- **CTFd**: Basic Flask application deployment
- **CTFd-HIKARI**: Microservices architecture with ELK stack

### **Dependencies**
```python
# Additional HIKARI dependencies
confluent-kafka==1.9.2
dataset==1.5.2
requests==2.28.1
```

### **Environment Configuration**
```bash
# HIKARI-specific environment variables
KAFKA_BOOTSTRAP_SERVERS=
KAFKA_SASL_USERNAME=
KAFKA_SASL_PASSWORD=
ELASTICSEARCH_URL=
KIBANA_URL=
```

## 6. Educational and Training Features

### **Blue Team Focus**
- Log analysis challenges using real security tools
- Incident response simulation scenarios
- Team-based collaborative investigation
- Progressive skill development through challenge chains

### **Real-time Learning**
- Dynamic log injection based on team progress
- Simulated attack scenarios with realistic timelines
- Collaborative analysis environment
- Immediate feedback on threat detection

## 7. Missing Features (CTFd → CTFd-HIKARI)

### **Recent CTFd Updates**
- Challenge attribution system
- Enhanced hint titles
- Additional language packs (bg, cs, el, fi, ro, sl, sv)
- Recent security improvements
- Email exception handling enhancements

### **Standard CTF Features**
- Some traditional CTF challenge types
- Basic jeopardy-style competition support
- Simplified deployment options

## 8. Version and Maintenance

### **Version State**
- **CTFd-HIKARI**: Based on earlier CTFd fork (~2023)
- **CTFd**: Current version with ongoing updates

### **Maintenance Considerations**
- HIKARI requires additional infrastructure management
- Complex deployment with multiple services
- Specialized knowledge required for ELK stack management
- Network configuration complexity with Zerotier

## 9. Use Case Comparison

### **CTFd Best For:**
- General cybersecurity competitions
- Educational institutions
- Quick deployment scenarios
- Traditional jeopardy-style CTFs

### **CTFd-HIKARI Best For:**
- Professional cybersecurity training
- Blue Team skill development
- Incident response training
- Corporate security awareness programs
- Advanced threat detection education

## 10. Technical Debt and Considerations

### **Advantages of HIKARI**
- Specialized for cybersecurity training
- Modern UI/UX with excellent user experience
- Real-time learning environment
- Professional-grade tool integration

### **Challenges**
- Complex infrastructure requirements
- Higher maintenance overhead
- Specialized deployment knowledge required
- Missing recent CTFd security updates

## Conclusion

CTFd-HIKARI represents a significant evolution of the CTFd platform, transforming it from a general-purpose CTF platform into a specialized cybersecurity training environment. While it adds substantial value for Blue Team education and incident response training, it comes with increased complexity and infrastructure requirements.

The platform successfully bridges the gap between academic cybersecurity education and real-world threat detection scenarios, providing an immersive learning experience that closely mimics professional security operations center (SOC) environments.