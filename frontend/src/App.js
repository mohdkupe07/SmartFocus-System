import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';

const socket = io('http://localhost:5000');

const PALETTE = {
  YALE_BLUE: "#1B4079",
  AIR_FORCE_BLUE: "#4D7C8A",
  CAMBRIDGE_BLUE: "#7F9C96",
  LIGHT_CAMBRIDGE: "#8FAD88",
  MINDARO: "#CBDF90",
  BG_DARK: "#0F172A"
};

function App() {
  const [data, setData] = useState({ status: 'Stopped', timeLeft: 0, frame: '' });
  const [minutes, setMinutes] = useState(25);
  const [active, setActive] = useState(false);

  useEffect(() => {
    socket.on('status', (res) => setData(res));
    return () => socket.off('status');
  }, []);

  const formatTime = (s) => `${Math.floor(s/60).toString().padStart(2, '0')}:${(s%60).toString().padStart(2, '0')}`;

  return (
    <div style={{ display: 'flex', height: '100vh', backgroundColor: PALETTE.BG_DARK, color: 'white', fontFamily: 'Inter, sans-serif' }}>
      
      {/* Sidebar - Control Panel */}
      <div style={{ width: '350px', backgroundColor: PALETTE.YALE_BLUE, padding: '40px', display: 'flex', flexDirection: 'column', boxShadow: '10px 0 30px rgba(0,0,0,0.3)' }}>
        <h1 style={{ color: PALETTE.MINDARO, fontSize: '28px', fontWeight: '800' }}>Smart Study Monitor</h1>
        <p style={{ color: PALETTE.CAMBRIDGE_BLUE, fontSize: '13px' }}>AI-Powered Focus Tracking</p>
        
        <div style={{ marginTop: '50px' }}>
          <label style={{ fontSize: '11px', fontWeight: 'bold', color: PALETTE.LIGHT_CAMBRIDGE }}>DURATION (MIN)</label>
          <input 
            type="number" 
            value={minutes} 
            onChange={(e) => setMinutes(e.target.value)}
            disabled={active}
            style={{ width: '100%', padding: '15px', marginTop: '10px', borderRadius: '12px', border: 'none', background: 'rgba(255,255,255,0.1)', color: 'white', fontSize: '18px' }}
          />
        </div>

        <div style={{ marginTop: '50px', padding: '30px', backgroundColor: 'rgba(0,0,0,0.2)', borderRadius: '20px', textAlign: 'center' }}>
          <p style={{ fontSize: '11px', color: PALETTE.CAMBRIDGE_BLUE }}>SESSION TIME</p>
          <h2 style={{ fontSize: '60px', margin: '10px 0', color: active ? PALETTE.MINDARO : PALETTE.AIR_FORCE_BLUE }}>
            {active ? formatTime(data.timeLeft) : `${minutes}:00`}
          </h2>
        </div>

        <div style={{ marginTop: 'auto', display: 'flex', flexDirection: 'column', gap: '15px' }}>
          <button 
            onClick={() => { setActive(true); fetch('http://localhost:5000/start', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({duration: minutes}) }); }}
            style={{ padding: '18px', borderRadius: '12px', border: 'none', background: PALETTE.MINDARO, color: PALETTE.YALE_BLUE, fontWeight: '800', cursor: 'pointer' }}>
            START STUDY
          </button>
          <button 
            onClick={() => { setActive(false); fetch('http://localhost:5000/stop', {method:'POST'}); }}
            style={{ padding: '18px', borderRadius: '12px', border: `1px solid ${PALETTE.CAMBRIDGE_BLUE}`, background: 'transparent', color: PALETTE.CAMBRIDGE_BLUE, fontWeight: '800', cursor: 'pointer' }}>
            STOP STUDY
          </button>
        </div>
      </div>

      {/* Main View - Camera Panel */}
      <div style={{ flex: 1, padding: '40px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <div style={{ width: '100%', maxWidth: '1100px', aspectRatio: '16/9', background: '#000', borderRadius: '24px', overflow: 'hidden', border: `2px solid ${PALETTE.AIR_FORCE_BLUE}`, boxShadow: '0 20px 50px rgba(0,0,0,0.5)' }}>
          {data.frame ? (
            <img src={`data:image/jpeg;base64,${data.frame}`} style={{ width: '100%', height: '100%', objectFit: 'contain' }} alt="Live Monitor" />
          ) : (
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%', color: PALETTE.AIR_FORCE_BLUE }}>
              Camera Standby - Click Start to Monitor
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;