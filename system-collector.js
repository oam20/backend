/**
 * Client-Side System Details Collector for Web Forms
 * Automatically collects system information when form is submitted
 * Works in modern browsers (Chrome, Edge, Firefox)
 */

class SystemDetailsCollector {
  constructor() {
    this.details = {};
  }

  /**
   * Collect all available system information
   */
  async collect() {
    try {
      this.details = {
        username: this.getUsername(),
        hostname: this.getHostname(),
        system_manufacturer: this.getSystemManufacturer(),
        system_model: this.getSystemModel(),
        ip_address: await this.getIPAddress(),
        serial_number: this.getSerialNumber(),
        os_info: this.getOSInfo(),
        storage: await this.getStorageInfo(),
        ram: this.getRAMInfo(),
        browser: this.getBrowserInfo(),
        screen: this.getScreenInfo(),
        collected_at: new Date().toISOString()
      };
      return this.details;
    } catch (error) {
      console.error('Error collecting system details:', error);
      return this.details;
    }
  }

  /**
   * Get username (limited - browser security restrictions)
   */
  getUsername() {
    // Try to get from various sources
    try {
      // This won't work due to browser security, but we try
      return navigator.userAgentData?.platform || 'Unknown';
    } catch {
      return 'Unknown';
    }
  }

  /**
   * Get hostname (limited - browser security restrictions)
   */
  getHostname() {
    try {
      return window.location.hostname || 'Unknown';
    } catch {
      return 'Unknown';
    }
  }

  /**
   * Get system manufacturer (limited - browser security)
   */
  getSystemManufacturer() {
    try {
      // Try to detect from user agent
      const ua = navigator.userAgent;
      if (ua.includes('Win64') || ua.includes('Windows')) {
        // Can't get actual manufacturer from browser
        return 'Detected: Windows';
      }
      return 'Unknown';
    } catch {
      return 'Unknown';
    }
  }

  /**
   * Get system model (limited - browser security)
   */
  getSystemModel() {
    try {
      const ua = navigator.userAgent;
      // Try to extract some info from user agent
      if (ua.includes('x64')) return 'x64 Architecture';
      if (ua.includes('ARM64')) return 'ARM64 Architecture';
      return 'Unknown';
    } catch {
      return 'Unknown';
    }
  }

  /**
   * Get IP address using external service
   */
  async getIPAddress() {
    try {
      // Try multiple IP detection services with timeout
      const services = [
        'https://api.ipify.org?format=json',
        'https://ipapi.co/json/',
        'https://api.ip.sb/ip'
      ];

      for (const service of services) {
        try {
          const controller = new AbortController();
          const timeoutId = setTimeout(() => controller.abort(), 5000);
          
          const response = await fetch(service, { 
            signal: controller.signal,
            method: 'GET'
          });
          clearTimeout(timeoutId);
          
          const data = await response.json();
          if (data.ip) return data.ip;
          if (data.query) return data.query;
        } catch (e) {
          continue;
        }
      }
      return 'Unknown';
    } catch {
      return 'Unknown';
    }
  }

  /**
   * Get serial number (not possible from browser - security restriction)
   */
  getSerialNumber() {
    // Browser security prevents access to hardware serial numbers
    return 'Not available via browser';
  }

  /**
   * Get OS information
   */
  getOSInfo() {
    try {
      const platform = navigator.platform || 'Unknown';
      const userAgent = navigator.userAgent || '';
      
      let system = 'Unknown';
      let release = 'Unknown';
      
      if (userAgent.includes('Windows NT 10.0')) {
        system = 'Windows';
        release = '10';
      } else if (userAgent.includes('Windows NT 6.3')) {
        system = 'Windows';
        release = '8.1';
      } else if (userAgent.includes('Windows NT 6.2')) {
        system = 'Windows';
        release = '8';
      } else if (userAgent.includes('Windows NT 6.1')) {
        system = 'Windows';
        release = '7';
      } else if (userAgent.includes('Mac OS X')) {
        system = 'macOS';
        const match = userAgent.match(/Mac OS X (\d+[._]\d+)/);
        release = match ? match[1].replace('_', '.') : 'Unknown';
      } else if (userAgent.includes('Linux')) {
        system = 'Linux';
        release = 'Unknown';
      }

      return {
        system: system,
        release: release,
        version: userAgent,
        platform: platform,
        processor: navigator.hardwareConcurrency ? `${navigator.hardwareConcurrency} cores` : 'Unknown',
        userAgent: userAgent
      };
    } catch {
      return {
        system: 'Unknown',
        release: 'Unknown',
        version: 'Unknown',
        platform: 'Unknown',
        processor: 'Unknown'
      };
    }
  }

  /**
   * Get storage information (limited - browser quota API)
   */
  async getStorageInfo() {
    try {
      if ('storage' in navigator && 'estimate' in navigator.storage) {
        const estimate = await navigator.storage.estimate();
        const usage = estimate.usage || 0;
        const quota = estimate.quota || 0;
        
        return [{
          drive: 'Browser Storage',
          total_gb: round(quota / (1024**3), 2),
          used_gb: round(usage / (1024**3), 2),
          free_gb: round((quota - usage) / (1024**3), 2),
          used_percent: quota > 0 ? round((usage / quota) * 100, 2) : 0
        }];
      }
      return [];
    } catch {
      return [];
    }
  }

  /**
   * Get RAM information (limited - browser API)
   */
  getRAMInfo() {
    try {
      if ('deviceMemory' in navigator) {
        const totalGB = navigator.deviceMemory || 0;
        return {
          total_gb: totalGB,
          available_gb: null,  // Use null instead of 'Not available' for database compatibility
          used_gb: null,
          free_gb: null,
          used_percent: null,
          note: 'Browser API limitation - only total RAM available'
        };
      }
      return {
        error: 'RAM information not available via browser API'
      };
    } catch {
      return {
        error: 'Could not retrieve RAM information'
      };
    }
  }

  /**
   * Get browser information
   */
  getBrowserInfo() {
    try {
      return {
        name: this.getBrowserName(),
        version: this.getBrowserVersion(),
        language: navigator.language || 'Unknown',
        cookieEnabled: navigator.cookieEnabled,
        onLine: navigator.onLine
      };
    } catch {
      return {};
    }
  }

  /**
   * Get browser name
   */
  getBrowserName() {
    const ua = navigator.userAgent;
    if (ua.includes('Chrome') && !ua.includes('Edg')) return 'Chrome';
    if (ua.includes('Edg')) return 'Edge';
    if (ua.includes('Firefox')) return 'Firefox';
    if (ua.includes('Safari') && !ua.includes('Chrome')) return 'Safari';
    return 'Unknown';
  }

  /**
   * Get browser version
   */
  getBrowserVersion() {
    const ua = navigator.userAgent;
    const match = ua.match(/(Chrome|Edg|Firefox|Safari)\/(\d+)/);
    return match ? match[2] : 'Unknown';
  }

  /**
   * Get screen information
   */
  getScreenInfo() {
    try {
      return {
        width: screen.width || 0,
        height: screen.height || 0,
        availWidth: screen.availWidth || 0,
        availHeight: screen.availHeight || 0,
        colorDepth: screen.colorDepth || 0,
        pixelDepth: screen.pixelDepth || 0
      };
    } catch {
      return {};
    }
  }
}

// Helper function
function round(value, decimals) {
  return Number(Math.round(value + 'e' + decimals) + 'e-' + decimals);
}

// Export for use in forms
if (typeof module !== 'undefined' && module.exports) {
  module.exports = SystemDetailsCollector;
}

