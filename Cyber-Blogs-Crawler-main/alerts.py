import json
import os
from datetime import datetime, timedelta
from collections import defaultdict

class AlertRule:
    """Define alert trigger rules with thresholds"""
    
    def __init__(self):
        self.alerts = []
        self.alerts_file = 'alerts.json'
        self.load_alerts()
        
        # Define alert rules: {incident_type: threshold_count}
        self.rules = {
            'malware': 10,           # Alert if > 10 malware posts in 1 hour
            'phishing': 5,           # Alert if > 5 phishing posts in 1 hour
            'ransomware': 8,         # Alert if > 8 ransomware posts in 1 hour
            'data_breach': 7,        # Alert if > 7 data breach posts in 1 hour
            'exploit': 6,            # Alert if > 6 exploit posts in 1 hour
            'zero-day': 3,           # Alert if > 3 zero-day posts in 1 hour
            'apt': 4,                # Alert if > 4 APT posts in 1 hour
            'vulnerability': 15,     # Alert if > 15 vulnerability posts in 1 hour
        }
        
        # Incident type mapping from keywords
        self.incident_map = {
            'malware': ['malware', 'worm', 'trojan', 'botnet'],
            'phishing': ['phishing', 'spear phishing', 'whaling'],
            'ransomware': ['ransomware', 'lockbit', 'wannacry', 'conti'],
            'data_breach': ['data breach', 'breach', 'leaked'],
            'exploit': ['exploit', 'RCE', 'remote code execution'],
            'zero-day': ['zero-day', '0-day', 'zero day'],
            'apt': ['APT', 'advanced persistent threat'],
            'vulnerability': ['vulnerability', 'CVE', 'patch']
        }

    def load_alerts(self):
        """Load existing alerts from JSON file"""
        if os.path.exists(self.alerts_file):
            try:
                with open(self.alerts_file, 'r') as f:
                    self.alerts = json.load(f)
            except:
                self.alerts = []
        else:
            self.alerts = []

    def save_alerts(self):
        """Save alerts to JSON file"""
        with open(self.alerts_file, 'w') as f:
            json.dump(self.alerts, f, indent=2)

    def categorize_incident(self, title):
        """Categorize incident based on title keywords"""
        title_lower = title.lower()
        for incident_type, keywords in self.incident_map.items():
            for keyword in keywords:
                if keyword in title_lower:
                    return incident_type
        return 'general'

    def check_thresholds(self, posts_data):
        """Check if incident counts exceed thresholds and generate alerts"""
        
        # Count incidents by type in the last hour
        current_time = datetime.now()
        one_hour_ago = current_time - timedelta(hours=1)
        
        incident_counts = defaultdict(int)
        
        for post in posts_data:
            incident_type = self.categorize_incident(post.get('title', ''))
            incident_counts[incident_type] += 1
        
        # Check against rules
        new_alerts = []
        for incident_type, count in incident_counts.items():
            threshold = self.rules.get(incident_type, 20)  # Default threshold
            
            if count > threshold:
                alert = {
                    'id': len(self.alerts) + len(new_alerts) + 1,
                    'timestamp': current_time.isoformat(),
                    'severity': self.calculate_severity(incident_type, count),
                    'type': incident_type,
                    'message': f'🚨 ALERT: {count} {incident_type.upper()} incidents detected (Threshold: {threshold})',
                    'count': count,
                    'threshold': threshold,
                    'status': 'active',
                    'read': False
                }
                new_alerts.append(alert)
                print(f"⚠️  ALERT TRIGGERED: {alert['message']}")
        
        # Add new alerts to the list
        if new_alerts:
            self.alerts.extend(new_alerts)
            self.save_alerts()
        
        return new_alerts

    def calculate_severity(self, incident_type, count):
        """Calculate alert severity level"""
        if incident_type in ['ransomware', 'data_breach', 'zero-day', 'apt']:
            if count > 5:
                return 'CRITICAL'
            elif count > 3:
                return 'HIGH'
            else:
                return 'MEDIUM'
        elif incident_type in ['malware', 'exploit']:
            if count > 15:
                return 'CRITICAL'
            elif count > 10:
                return 'HIGH'
            else:
                return 'MEDIUM'
        else:
            if count > 20:
                return 'HIGH'
            else:
                return 'MEDIUM'

    def get_recent_alerts(self, limit=10):
        """Get recent alerts (last N alerts)"""
        return sorted(self.alerts, key=lambda x: x['timestamp'], reverse=True)[:limit]

    def get_active_alerts(self):
        """Get all active alerts"""
        return [a for a in self.alerts if a['status'] == 'active']

    def mark_alert_as_read(self, alert_id):
        """Mark an alert as read"""
        for alert in self.alerts:
            if alert['id'] == alert_id:
                alert['read'] = True
                self.save_alerts()
                return True
        return False

    def dismiss_alert(self, alert_id):
        """Dismiss/close an alert"""
        for alert in self.alerts:
            if alert['id'] == alert_id:
                alert['status'] = 'dismissed'
                self.save_alerts()
                return True
        return False

    def get_alert_statistics(self):
        """Get alert statistics"""
        active_count = len(self.get_active_alerts())
        total_count = len(self.alerts)
        
        # Count by severity
        severity_count = defaultdict(int)
        for alert in self.alerts:
            severity_count[alert['severity']] += 1
        
        return {
            'active_count': active_count,
            'total_count': total_count,
            'by_severity': dict(severity_count)
        }

# Create global alert manager instance
alert_manager = AlertRule()
