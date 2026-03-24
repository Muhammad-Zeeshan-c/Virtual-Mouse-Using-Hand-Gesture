import React, { useState, useEffect } from 'react';
import { 
  Settings, 
  MousePointer2, 
  Hand, 
  Activity, 
  Cpu, 
  ShieldCheck,
  Mouse,
  Layers,
  Zap
} from 'lucide-react';

const App = () => {
  const [status, setStatus] = useState({
    fps: 0,
    gesture: "NONE",
    hand_detected: false
  });
  
  const [settings, setSettings] = useState({
    sensitivity: 5,
    smoothing: 5,
    enableMove: true,
    enableClick: true,
    enableRightClick: true,
    enableScroll: true,
    enableDrag: true
  });

  const [connected, setConnected] = useState(false);

  // Connect to Python Backend via WebSocket
  useEffect(() => {
    let ws;
    const connect = () => {
      ws = new WebSocket('ws://localhost:8000/ws');
      
      ws.onopen = () => {
        setConnected(true);
        console.log('Connected to backend');
      };

      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        setStatus(data.status);
        // We only update settings if they were changed from backend (optional)
        // For now, we assume local state is source of truth for UI
      };

      ws.onclose = () => {
        setConnected(false);
        setTimeout(connect, 2000); // Retry connection
      };
    };

    connect();
    return () => ws?.close();
  }, []);

  const updateSettings = async (newSettings) => {
    const updated = { ...settings, ...newSettings };
    setSettings(updated);
    
    try {
      await fetch('http://localhost:8000/settings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updated)
      });
    } catch (err) {
      console.error("Failed to update settings", err);
    }
  };

  const Toggle = ({ name, label, value }) => (
    <div className="flex items-center justify-between p-4 mb-2 transition-all rounded-xl glass hover:bg-white/5">
      <div className="flex items-center gap-3">
        <label className="text-sm font-medium text-gray-300">{label}</label>
      </div>
      <button 
        onClick={() => updateSettings({ [name]: !value })}
        className={`w-12 h-6 rounded-full transition-all duration-300 relative ${value ? 'bg-cyan-500' : 'bg-gray-700'}`}
      >
        <div className={`absolute top-1 left-1 w-4 h-4 rounded-full bg-white transition-all transform ${value ? 'translate-x-6' : ''}`} />
      </button>
    </div>
  );

  return (
    <div className="min-h-screen p-6 md:p-12 max-w-6xl mx-auto">
      {/* Header */}
      <header className="flex flex-col md:flex-row items-center justify-between mb-12 gap-6">
        <div>
          <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-cyan-400 to-purple-500 bg-clip-text text-transparent mb-2">
            AI Virtual Mouse
          </h1>
          <p className="text-gray-400 flex items-center gap-2">
            Control your workspace with zero touch.
            <span className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium ${connected ? 'bg-green-500/10 text-green-400 border border-green-500/20' : 'bg-red-500/10 text-red-400 border border-red-500/20'}`}>
              <span className={`w-1.5 h-1.5 rounded-full ${connected ? 'bg-green-400 animate-pulse' : 'bg-red-400'}`} />
              {connected ? 'System Online' : 'Connecting to Server...'}
            </span>
          </p>
        </div>
        <div className="flex items-center gap-4 bg-white/5 p-4 rounded-2xl border border-white/10">
          <Activity className="text-cyan-400" size={24} />
          <div className="text-right">
            <div className="text-2xl font-bold font-mono">{status.fps} FPS</div>
            <div className="text-[10px] uppercase text-gray-500 tracking-wider">Engine Performance</div>
          </div>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Real-time Status */}
        <div className="lg:col-span-1 space-y-6">
          <div className="p-8 rounded-3xl glass relative overflow-hidden group">
            <div className="absolute top-0 right-0 p-4 opacity-20 group-hover:opacity-40 transition-opacity">
              <Hand size={80} />
            </div>
            <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
              <Cpu size={20} className="text-purple-400" /> Live Feedback
            </h2>
            
            <div className="space-y-8 relative">
              <div>
                <label className="text-xs uppercase text-gray-500 tracking-widest mb-2 block">Active Gesture</label>
                <div className={`text-3xl font-bold font-mono py-2 px-4 rounded-lg inline-block ${status.gesture !== 'NONE' ? 'bg-cyan-500/20 text-cyan-400 neon-text' : 'bg-white/5 text-gray-600'}`}>
                  {status.gesture}
                </div>
              </div>
              
              <div>
                <label className="text-xs uppercase text-gray-500 tracking-widest mb-2 block">Detection Status</label>
                <div className="flex items-center gap-2 text-xl">
                  {status.hand_detected ? (
                    <><ShieldCheck className="text-green-500" /> <span className="text-green-400">Hand Tracked</span></>
                  ) : (
                    <><Zap className="text-yellow-500 animate-pulse" /> <span className="text-yellow-400">Searching...</span></>
                  )}
                </div>
              </div>
            </div>
          </div>

          <div className="p-8 rounded-3xl glass">
            <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <Layers size={18} className="text-cyan-400" /> System Metrics
            </h3>
            <div className="space-y-4">
              <div className="w-full bg-white/5 h-2 rounded-full overflow-hidden">
                <div className="bg-cyan-400 h-full w-[85%] animate-pulse" />
              </div>
              <div className="flex justify-between text-xs text-gray-500 font-mono text-center">
                 <span>Latency: ~12ms</span>
                 <span>Buffer: 0.1s</span>
              </div>
            </div>
          </div>
        </div>

        {/* Settings Panel */}
        <div className="lg:col-span-2 p-8 rounded-3xl glass border border-white/5">
          <div className="flex items-center justify-between mb-8">
            <h2 className="text-2xl font-semibold mb-2 flex items-center gap-2">
              <Settings size={22} className="text-cyan-400" /> Configuration
            </h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
            <div className="space-y-6">
              <h3 className="text-sm font-medium text-gray-400 uppercase tracking-widest">Precision</h3>
              <div>
                <div className="flex justify-between mb-2">
                  <label className="text-sm">Cursor Sensitivity</label>
                  <span className="text-cyan-400 font-mono">{settings.sensitivity}x</span>
                </div>
                <input 
                  type="range" min="1" max="10" 
                  value={settings.sensitivity}
                  onChange={(e) => updateSettings({ sensitivity: parseInt(e.target.value) })}
                  className="w-full accent-cyan-400"
                />
              </div>

              <div>
                <div className="flex justify-between mb-2">
                  <label className="text-sm">Jitter Smoothing</label>
                  <span className="text-purple-400 font-mono">{settings.smoothing}x</span>
                </div>
                <input 
                  type="range" min="1" max="15" 
                  value={settings.smoothing}
                  onChange={(e) => updateSettings({ smoothing: parseInt(e.target.value) })}
                  className="w-full accent-purple-400"
                />
              </div>
            </div>

            <div className="space-y-1">
              <h3 className="text-sm font-medium text-gray-400 uppercase tracking-widest mb-4">Input Toggles</h3>
              <Toggle name="enableMove" label="Cursor Movement" value={settings.enableMove} />
              <Toggle name="enableClick" label="Left Click (Index Pinch)" value={settings.enableClick} />
              <Toggle name="enableRightClick" label="Right Click (Two Finger)" value={settings.enableRightClick} />
              <Toggle name="enableScroll" label="Scroll Support" value={settings.enableScroll} />
              <Toggle name="enableDrag" label="Drag & Drop" value={settings.enableDrag} />
            </div>
          </div>

          <div className="p-6 rounded-2xl bg-gradient-to-br from-cyan-500/10 to-purple-500/10 border border-cyan-500/20">
             <div className="flex items-start gap-4">
                <div className="p-3 bg-cyan-400/20 rounded-xl">
                  <MousePointer2 className="text-cyan-400" size={24} />
                </div>
                <div>
                  <h4 className="font-semibold text-white mb-1">Mirror Mode Enabled</h4>
                  <p className="text-sm text-gray-400">The cursor tracks your movements in mirrored mode for a more natural interaction feel.</p>
                </div>
             </div>
          </div>
        </div>
      </div>
      
      <footer className="mt-12 text-center text-gray-600 text-sm">
        AI Virtual Mouse System &bull; Built with MediaPipe & React
      </footer>
    </div>
  );
};

export default App;
