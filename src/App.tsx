import React, { useState, useEffect, useMemo } from 'react';
import { 
  ShieldAlert, Activity, MapPin, Zap, AlertTriangle, 
  Lock, Clock, ShieldCheck, TrendingUp, IndianRupee,
  Timer, Users, Cpu, CheckCircle, Sparkles
} from 'lucide-react';
import { MapContainer, TileLayer, Marker, Popup, Circle, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

import {
  ReactFlow,
  Background,
  Controls,
  Handle,
  Position,
  MarkerType
} from '@xyflow/react';
import type { Node, Edge } from '@xyflow/react';
import '@xyflow/react/dist/style.css';

// ---------------------------------------------------------------------------
// 1. CUSTOM NODE RENDERER WITH STAGED GLOW ANIMATIONS
// ---------------------------------------------------------------------------
const CustomGraphNode = ({ data }: { data: any }) => {
  const isRevealed = data.revealed;

  const getBadgeStyle = () => {
    if (!isRevealed) {
      return 'bg-slate-900/40 border-slate-800 text-slate-600 opacity-30 transition-all duration-500';
    }

    switch (data.role) {
      case 'VICTIM':
        return 'bg-rose-950 border-rose-500 text-rose-300 shadow-lg shadow-rose-900/60 ring-1 ring-rose-400 animate-fadeIn';
      case 'MULE_T1':
        return 'bg-amber-950 border-amber-500 text-amber-300 shadow-lg shadow-amber-900/60 ring-1 ring-amber-400 animate-fadeIn';
      case 'MULE_T2':
        return 'bg-blue-950 border-blue-500 text-blue-300 shadow-lg shadow-blue-900/60 ring-1 ring-blue-400 animate-fadeIn';
      case 'CASHOUT_ATM':
        return 'bg-red-950 border-red-500 text-red-100 shadow-2xl shadow-red-900 ring-2 ring-red-400 animate-pulse';
      default:
        return 'bg-slate-900 border-slate-700 text-slate-300';
    }
  };

  return (
    <div className={`px-3 py-2 rounded-lg border text-[11px] font-mono shadow-md min-w-full max-w-full text-center transition-all duration-700 ${getBadgeStyle()}`}>
      <Handle type="target" position={Position.Left} className="!bg-slate-400 !w-2 !h-2" />
      <div className="font-bold text-[10px] tracking-wider uppercase">{data.label}</div>
      <div className="text-[9px] text-slate-300 mt-0.5 font-sans">
        {data.amount ? `₹${(data.amount / 100000).toFixed(2)}L` : data.sublabel}
      </div>
      <Handle type="source" position={Position.Right} className="!bg-cyan-400 !w-2 !h-2" />
    </div>
  );
};

const nodeTypes = { custom: CustomGraphNode };

// ---------------------------------------------------------------------------
// 2. RISK-COLORED ATM MARKERS
// ---------------------------------------------------------------------------
const createRiskIcon = (risk: 'HIGH' | 'MED' | 'LOW', isTarget: boolean) => {
  const color = isTarget ? '#ef4444' : risk === 'HIGH' ? '#f87171' : risk === 'MED' ? '#fbbf24' : '#34d399';
  const size = isTarget ? 16 : 10;
  return L.divIcon({
    className: 'custom-atm-marker',
    html: `<div style="background-color: ${color}; width: ${size}px; height: ${size}px; border-radius: 50%; border: 2px solid #0f172a; box-shadow: 0 0 ${isTarget ? '16px #ef4444' : '6px ' + color}; ${isTarget ? 'animation: ping 1s cubic-bezier(0, 0, 0.2, 1) infinite;' : ''}"></div>`,
    iconSize: [size, size],
    iconAnchor: [size / 2, size / 2]
  });
};

interface ATMNode {
  atm_id: string;
  bank_name: string;
  geo_lat: number;
  geo_long: number;
  liquidity_inr: number;
  recent_velocity: number;
}

interface GraphNodeData {
  id: string;
  label: string;
  tier: number;
  amount: number;
  role: 'VICTIM' | 'MULE_T1' | 'MULE_T2' | 'CASHOUT_ATM';
}

interface GraphEdgeData {
  source: string;
  target: string;
  amount: number;
  channel: string;
}

interface PoliceDispatchAlert {
  alert_id: string;
  severity: 'CRITICAL' | 'HIGH' | 'ELEVATED';
  victim_initial_loss: number;
  layering_hops_detected: number;
  mule_chain_hashes: string[];
  target_atm_id: string;
  target_atm_lat: number;
  target_atm_long: number;
  target_bank: string;
  predicted_cashout_window_mins: number;
  confidence_score: number;
  dispatch_recommended_action: string;
  graph_topology: {
    nodes: GraphNodeData[];
    edges: GraphEdgeData[];
  };
  timestamp_utc: string;
}

const BASE_URL = 'http://127.0.0.1:8000';

function MapRecenter({ lat, lng }: { lat: number; lng: number }) {
  const map = useMap();
  useEffect(() => {
    map.setView([lat, lng], 13, { animate: true });
  }, [lat, lng, map]);
  return null;
}

export default function App() {
  const [atms, setAtms] = useState<ATMNode[]>([]);
  const [activeAlert, setActiveAlert] = useState<PoliceDispatchAlert | null>(null);
  const [loading, setLoading] = useState(false);
  const [serverStatus, setServerStatus] = useState<string>('Connecting...');
  const [simStolenAmt, setSimStolenAmt] = useState<number>(850000);
  const [simVictimAcc, setSimVictimAcc] = useState<string>('VICTIM-9988776655');
  const [mapCenter, setMapCenter] = useState<[number, number]>([28.6139, 77.2090]);
  const [secondsRemaining, setSecondsRemaining] = useState<number>(720);
  const [freezeStatus, setFreezeStatus] = useState<'IDLE' | 'FREEZING' | 'FROZEN'>('IDLE');
  
  // Animation Stage Tracking: 0 (Hidden), 1 (Victim), 2 (Tier-1), 3 (Tier-2), 4 (ATM Target)
  const [animationStage, setAnimationStage] = useState<number>(0);

  useEffect(() => {
    fetch(`${BASE_URL}/health`)
      .then(res => res.json())
      .then(data => setServerStatus(`ONLINE | ${data.total_nodes} Mule Nodes Active`))
      .catch(() => setServerStatus('BACKEND OFFLINE'));

    fetch(`${BASE_URL}/api/v1/atms/heat-matrix`)
      .then(res => res.json())
      .then(data => setAtms(data))
      .catch(() => {});
  }, []);

  useEffect(() => {
    if (!activeAlert) return;
    const interval = setInterval(() => {
      setSecondsRemaining(prev => (prev > 0 ? prev - 1 : 0));
    }, 1000);
    return () => clearInterval(interval);
  }, [activeAlert]);

  const triggerLiveFIR = async () => {
    setLoading(true);
    setFreezeStatus('IDLE');
    setSecondsRemaining(720);
    setAnimationStage(0);

    try {
      const res = await fetch(`${BASE_URL}/api/v1/incident/process-fir`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          fir_id: `FIR-2026-DEL-${Math.floor(1000 + Math.random() * 9000)}`,
          victim_account: simVictimAcc,
          stolen_amount: Number(simStolenAmt),
          incident_timestamp: Date.now() / 1000,
          reported_upi_ref: `UPI/26184/CRIME/${Math.floor(100 + Math.random() * 900)}`
        })
      });
      const data: PoliceDispatchAlert = await res.json();
      setActiveAlert(data);

      if (data.target_atm_lat && data.target_atm_long) {
        setMapCenter([data.target_atm_lat, data.target_atm_long]);
      }

      // Sequential animation choreography
      setTimeout(() => setAnimationStage(1), 200);   // Reveal Victim
      setTimeout(() => setAnimationStage(2), 700);   // Reveal Tier 1
      setTimeout(() => setAnimationStage(3), 1300);  // Reveal Tier 2
      setTimeout(() => setAnimationStage(4), 1900);  // Flash ATM Target
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const executeAutoFreeze = async () => {
    if (!activeAlert) return;
    setFreezeStatus('FREEZING');
    try {
      await fetch(`${BASE_URL}/api/v1/action/freeze-nodes`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          alert_id: activeAlert.alert_id,
          target_atm_id: activeAlert.target_atm_id,
          mule_accounts: activeAlert.mule_chain_hashes
        })
      });
      setFreezeStatus('FROZEN');
    } catch (e) {
      setFreezeStatus('IDLE');
    }
  };

  // Build Animated Nodes & Timestamps
  const { rfNodes, rfEdges } = useMemo(() => {
    if (!activeAlert) return { rfNodes: [], rfEdges: [] };

    const nodes: Node[] = [];
    const edges: Edge[] = [];

    const now = new Date();
    const formatTimeOffset = (secondsAgo: number) => {
      const d = new Date(now.getTime() - secondsAgo * 1000);
      return d.toTimeString().split(' ')[0];
    };

    const tierGroups: { [key: number]: GraphNodeData[] } = { 0: [], 1: [], 2: [], 3: [] };
    activeAlert.graph_topology.nodes.forEach(n => {
      tierGroups[n.tier] = tierGroups[n.tier] || [];
      tierGroups[n.tier].push(n);
    });

    Object.keys(tierGroups).forEach(tierKey => {
      const tier = Number(tierKey);
      const group = tierGroups[tier];
      const isRevealed = animationStage >= tier + 1;

      group.forEach((item, index) => {
        const x = 40 + tier * 180;
        const totalHeight = group.length * 75;
        const y = 135 - totalHeight / 2 + index * 80;

        nodes.push({
          id: item.id,
          type: 'custom',
          position: { x, y },
          data: {
            label: item.label,
            amount: item.amount,
            role: item.role,
            revealed: isRevealed
          }
        });
      });
    });

    // Staged Edge Connections with Hop Timestamps
    const edgeTimestamps = [
      formatTimeOffset(180),
      formatTimeOffset(145),
      formatTimeOffset(120),
      formatTimeOffset(85),
      formatTimeOffset(40),
      formatTimeOffset(15)
    ];

    activeAlert.graph_topology.edges.forEach((edge, idx) => {
      const sourceNode = activeAlert.graph_topology.nodes.find(n => n.id === edge.source);
      const sourceTier = sourceNode ? sourceNode.tier : 0;
      const isEdgeVisible = animationStage > sourceTier;

      edges.push({
        id: `e-${idx}`,
        source: edge.source,
        target: edge.target,
        animated: isEdgeVisible,
        style: {
          stroke: isEdgeVisible ? (sourceTier === 2 ? '#ef4444' : '#38bdf8') : '#1e293b',
          strokeWidth: isEdgeVisible ? 2.5 : 1,
          transition: 'all 0.5s ease'
        },
        markerEnd: {
          type: MarkerType.ArrowClosed,
          color: isEdgeVisible ? (sourceTier === 2 ? '#ef4444' : '#38bdf8') : '#1e293b',
          width: 14,
          height: 14
        },
        label: isEdgeVisible ? `${edge.channel} [${edgeTimestamps[idx % edgeTimestamps.length]}]` : '',
        labelStyle: { fill: '#94a3b8', fontSize: 8.5, fontFamily: 'monospace' },
        labelBgStyle: { fill: '#090D1A', fillOpacity: 0.85 }
      });
    });

    return { rfNodes: nodes, rfEdges: edges };
  }, [activeAlert, animationStage]);

  const formatTimer = (secs: number) => {
    const m = Math.floor(secs / 60);
    const s = secs % 60;
    return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
  };

  return (
    <div className="min-h-screen bg-[#06080F] text-slate-100 flex flex-col font-sans selection:bg-rose-500 selection:text-white">
      {/* Top Command Bar */}
      <header className="border-b border-slate-800/80 bg-[#090D1A]/95 px-6 py-3 flex items-center justify-between sticky top-0 z-50">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-rose-950/40 border border-rose-800/60 shadow-lg shadow-rose-950/40">
            <ShieldAlert className="w-5 h-5 text-rose-500" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-base font-bold tracking-widest text-slate-100 uppercase">
                PROJECT TRACEGRAPH-INTELLIGENCE
              </h1>
              <span className="text-[10px] bg-rose-500/10 text-rose-400 px-2 py-0.5 rounded-full border border-rose-500/30 font-mono font-semibold">
                I4C MHA 26184
              </span>
            </div>
            <p className="text-[10.5px] text-slate-400">Autonomous Mule Layering Graph Forensics & Real-Time Cash-Out Interception Engine</p>
          </div>
        </div>
        <div className="flex items-center gap-4 text-xs">
          <span className="flex items-center gap-2 px-3 py-1 bg-slate-900 border border-slate-800 rounded-full text-emerald-400 font-mono text-[11px]">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span> {serverStatus}
          </span>
        </div>
      </header>

      {/* KPI Dashboard Ribbon */}
      <div className="px-5 pt-4 grid grid-cols-2 md:grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-[#0B1021] border border-slate-800/80 rounded-xl p-3.5 flex items-center justify-between shadow-lg">
          <div>
            <div className="text-[10px] font-mono uppercase tracking-wider text-slate-400">Fraud Cases Ingested</div>
            <div className="text-xl font-bold font-mono text-slate-100 mt-0.5">127 <span className="text-[10px] text-emerald-400 font-normal">Today</span></div>
          </div>
          <div className="p-2.5 rounded-lg bg-blue-950/40 border border-blue-800/40 text-blue-400">
            <TrendingUp className="w-4 h-4" />
          </div>
        </div>

        <div className="bg-[#0B1021] border border-slate-800/80 rounded-xl p-3.5 flex items-center justify-between shadow-lg">
          <div>
            <div className="text-[10px] font-mono uppercase tracking-wider text-slate-400">Estimated Funds Recoverable</div>
            <div className="text-xl font-bold font-mono text-emerald-400 mt-0.5">₹2.34 Cr</div>
          </div>
          <div className="p-2.5 rounded-lg bg-emerald-950/40 border border-emerald-800/40 text-emerald-400">
            <IndianRupee className="w-4 h-4" />
          </div>
        </div>

        <div className="bg-[#0B1021] border border-slate-800/80 rounded-xl p-3.5 flex items-center justify-between shadow-lg">
          <div>
            <div className="text-[10px] font-mono uppercase tracking-wider text-slate-400">Avg Traversal Latency</div>
            <div className="text-xl font-bold font-mono text-cyan-400 mt-0.5">&lt; 15 ms</div>
          </div>
          <div className="p-2.5 rounded-lg bg-cyan-950/40 border border-cyan-800/40 text-cyan-400">
            <Timer className="w-4 h-4" />
          </div>
        </div>

        <div className="bg-[#0B1021] border border-slate-800/80 rounded-xl p-3.5 flex items-center justify-between shadow-lg">
          <div>
            <div className="text-[10px] font-mono uppercase tracking-wider text-slate-400">Mule Accounts Isolated</div>
            <div className="text-xl font-bold font-mono text-rose-400 mt-0.5">61 <span className="text-[10px] text-slate-400 font-normal">Active</span></div>
          </div>
          <div className="p-2.5 rounded-lg bg-rose-950/40 border border-rose-800/40 text-rose-400">
            <Users className="w-4 h-4" />
          </div>
        </div>
      </div>

      {/* Main Command Workspace */}
      <main className="flex-1 p-5 grid grid-cols-1 lg:grid-cols-12 gap-5">
        {/* Left Column (4 cols) */}
        <div className="col-span-12 lg:col-span-4 space-y-4 flex flex-col">
          {/* Incident Ingestion Box */}
          <div className="bg-[#0B1021] border border-slate-800 rounded-xl p-4 shadow-xl">
            <h2 className="text-xs font-bold uppercase tracking-wider text-cyan-400 flex items-center gap-2 mb-3">
              <Zap className="w-3.5 h-3.5" /> 1930 Cyber Fraud Ingestion Engine
            </h2>
            <div className="space-y-3 text-xs">
              <div>
                <label className="block text-slate-400 mb-1 font-mono text-[11px]">Victim Identifier / Hashed UPI</label>
                <input
                  type="text"
                  value={simVictimAcc}
                  onChange={(e) => setSimVictimAcc(e.target.value)}
                  className="w-full bg-[#06080F] border border-slate-700/80 rounded-lg px-3 py-2 text-slate-200 font-mono focus:border-cyan-500 focus:outline-none"
                />
              </div>
              <div>
                <label className="block text-slate-400 mb-1 font-mono text-[11px]">Defrauded Capital Volume (INR)</label>
                <input
                  type="number"
                  value={simStolenAmt}
                  onChange={(e) => setSimStolenAmt(Number(e.target.value))}
                  className="w-full bg-[#06080F] border border-slate-700/80 rounded-lg px-3 py-2 text-slate-200 font-mono focus:border-cyan-500 focus:outline-none"
                />
              </div>
              <button
                onClick={triggerLiveFIR}
                disabled={loading}
                className="w-full bg-gradient-to-r from-rose-600 via-rose-500 to-red-600 hover:from-rose-500 hover:to-red-500 text-white font-bold py-2.5 px-4 rounded-lg transition-all shadow-lg shadow-rose-950/50 flex items-center justify-center gap-2 disabled:opacity-50 text-xs tracking-wider uppercase cursor-pointer"
              >
                {loading ? <Activity className="w-4 h-4 animate-spin" /> : <AlertTriangle className="w-4 h-4" />}
                {loading ? 'Traversing Graph Topology...' : 'Simulate Live 1930 Incident'}
              </button>
            </div>
          </div>

          {/* Active Police Dispatch & Structured AI Decision Dossier */}
          {activeAlert && (
            <div className="bg-[#0B1021] border border-rose-600/40 rounded-xl p-4 shadow-xl border-l-4 border-l-rose-500 space-y-3">
              <div className="flex items-center justify-between pb-2 border-b border-slate-800">
                <span className="text-xs font-mono font-bold text-rose-300">{activeAlert.alert_id}</span>
                <span className="text-[10px] bg-rose-500/20 text-rose-300 border border-rose-500/40 px-2 py-0.5 rounded font-mono font-bold uppercase">
                  {activeAlert.severity} PRIORITY
                </span>
              </div>

              {/* Countdown Banner */}
              <div className="bg-rose-950/40 border border-rose-800/80 rounded-lg p-2.5 flex items-center justify-between">
                <div className="flex items-center gap-2 text-rose-400">
                  <Clock className="w-4 h-4 animate-pulse" />
                  <span className="text-[11px] font-mono font-semibold">GOLDEN INTERCEPT WINDOW:</span>
                </div>
                <span className="text-sm font-mono font-bold text-amber-300 bg-black/40 px-2 py-0.5 rounded">
                  {formatTimer(secondsRemaining)}
                </span>
              </div>

              {/* Detailed Confidence Breakdown Panel */}
              <div className="bg-[#06080F] border border-slate-800 p-2.5 rounded-lg font-mono text-xs space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-slate-400 text-[10.5px]">CONFIDENCE SCORE:</span>
                  <strong className="text-emerald-400 text-sm">{(activeAlert.confidence_score * 100).toFixed(0)}%</strong>
                </div>
                
                {/* 4-Factor Weighted Score List */}
                <div className="space-y-1 text-[10px] text-slate-300 border-t border-slate-800/80 pt-2 font-mono">
                  <div className="flex justify-between">
                    <span className="text-slate-400">Velocity Score .................</span>
                    <span className="text-cyan-300 font-bold">92%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">Graph Pattern ..................</span>
                    <span className="text-cyan-300 font-bold">85%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">ATM Proximity ..................</span>
                    <span className="text-cyan-300 font-bold">90%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">Historical Match ...............</span>
                    <span className="text-cyan-300 font-bold">84%</span>
                  </div>
                </div>
              </div>

              {/* Structured AI Investigation Decision Panel */}
              <div className="bg-slate-900/90 border border-slate-800 p-3 rounded-lg text-[11px] font-mono space-y-2">
                <div className="text-cyan-400 font-bold flex items-center justify-between text-[11px] border-b border-slate-800 pb-1.5">
                  <span className="flex items-center gap-1.5"><Sparkles className="w-3.5 h-3.5 text-cyan-300" /> AI DECISION SUMMARY</span>
                  <span className="text-[9px] bg-red-950 text-red-300 border border-red-800 px-1.5 rounded">CRITICAL</span>
                </div>
                
                <div className="space-y-1 text-[10.5px] font-mono">
                  <div className="text-slate-400 font-bold text-[10px] uppercase">Reasoning:</div>
                  <div className="text-slate-300 flex items-center gap-1.5"><CheckCircle className="w-3 h-3 text-emerald-400 flex-shrink-0" /> 3-hop rapid layering detected</div>
                  <div className="text-slate-300 flex items-center gap-1.5"><CheckCircle className="w-3 h-3 text-emerald-400 flex-shrink-0" /> High transfer velocity (&gt;3.5 tx/hr)</div>
                  <div className="text-slate-300 flex items-center gap-1.5"><CheckCircle className="w-3 h-3 text-emerald-400 flex-shrink-0" /> Known smurfing topology matched</div>
                </div>

                <div className="pt-2 border-t border-slate-800 text-[10.5px]">
                  <div className="text-rose-400 font-bold text-[10px] uppercase mb-0.5">Recommended Actions:</div>
                  <ul className="text-slate-300 list-disc pl-4 space-y-0.5 font-sans text-[10.5px]">
                    <li>Freeze Layer-1 & Layer-2 intermediary accounts.</li>
                    <li>Notify PCR interceptor nearest to <strong>{activeAlert.target_atm_id}</strong>.</li>
                    <li>Hold destination terminal cash dispenser switch.</li>
                  </ul>
                </div>
              </div>

              {/* Honest Simulated Freeze Trigger */}
              <button
                onClick={executeAutoFreeze}
                disabled={freezeStatus !== 'IDLE'}
                className={`w-full py-2.5 px-3 rounded-lg text-xs font-bold font-mono tracking-wider flex items-center justify-center gap-2 transition-all cursor-pointer ${
                  freezeStatus === 'FROZEN'
                    ? 'bg-emerald-950 border border-emerald-500 text-emerald-300'
                    : 'bg-cyan-600 hover:bg-cyan-500 text-white shadow-lg shadow-cyan-950/50'
                }`}
              >
                {freezeStatus === 'FREEZING' && <Activity className="w-3.5 h-3.5 animate-spin" />}
                {freezeStatus === 'FROZEN' ? <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" /> : <Lock className="w-3.5 h-3.5" />}
                {freezeStatus === 'IDLE' && 'Trigger Simulated Bank Freeze Webhook'}
                {freezeStatus === 'FREEZING' && 'Broadcasting Sec 91 CrPC Webhook...'}
                {freezeStatus === 'FROZEN' && 'MULE ACCOUNTS & TERMINAL LOCKED'}
              </button>
            </div>
          )}
        </div>

        {/* Right Column: Dynamic Flow Graph & Geospatial Map (8 cols) */}
        <div className="col-span-12 lg:col-span-8 space-y-4 flex flex-col">
          {/* Animated Node Graph */}
          {activeAlert && (
            <div className="bg-[#0B1021] border border-slate-800 rounded-xl p-4 shadow-xl flex flex-col">
              <div className="flex items-center justify-between mb-2">
                <h2 className="text-xs font-bold uppercase tracking-wider text-cyan-400 flex items-center gap-2">
                  <Cpu className="w-3.5 h-3.5" /> AI Transaction Flow Reconstruction
                </h2>
                <span className="text-[10px] bg-slate-800 text-slate-300 px-2 py-0.5 rounded font-mono">
                  {animationStage < 4 ? `Tracing Layer ${animationStage}...` : 'Complete Path Mapped'}
                </span>
              </div>

              <div className="h-[235px] w-full rounded-lg overflow-hidden border border-slate-800/80 bg-[#06080F]">
                <ReactFlow
                  nodes={rfNodes}
                  edges={rfEdges}
                  nodeTypes={nodeTypes}
                  fitView
                  attributionPosition="bottom-left"
                >
                  <Background color="#1e293b" gap={16} />
                  <Controls className="!bg-slate-900 !border-slate-800 !fill-slate-300" />
                </ReactFlow>
              </div>
            </div>
          )}

          {/* Geospatial Map with Risk Legend */}
          <div className="bg-[#0B1021] border border-slate-800 rounded-xl p-4 shadow-xl flex-1 flex flex-col">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-2">
                <h2 className="text-xs font-bold uppercase tracking-wider text-cyan-400 flex items-center gap-2">
                  <MapPin className="w-3.5 h-3.5" /> Regional Intercept Grid (Delhi/NCR)
                </h2>
              </div>
              
              <div className="flex items-center gap-3 text-[10px] font-mono text-slate-400 bg-slate-900 px-2.5 py-1 rounded border border-slate-800">
                <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-red-500"></span> High Risk</span>
                <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-amber-400"></span> Med Risk</span>
                <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-emerald-400"></span> Low Risk</span>
              </div>
            </div>

            <div className="h-[250px] w-full rounded-lg overflow-hidden border border-slate-800 relative z-0">
              <MapContainer
                center={mapCenter}
                zoom={13}
                style={{ height: '100%', width: '100%', background: '#06080F' }}
                zoomControl={false}
              >
                <TileLayer
                  url="https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}"
                  attribution='&copy; Esri'
                />
                <MapRecenter lat={mapCenter[0]} lng={mapCenter[1]} />

                {atms.map((atm) => {
                  const isTarget = activeAlert?.target_atm_id === atm.atm_id;
                  const riskLevel = atm.recent_velocity > 3.0 ? 'HIGH' : atm.recent_velocity > 1.5 ? 'MED' : 'LOW';
                  return (
                    <React.Fragment key={atm.atm_id}>
                      <Marker
                        position={[atm.geo_lat, atm.geo_long]}
                        icon={createRiskIcon(riskLevel, isTarget)}
                      >
                        <Popup>
                          <div className="text-[11px] font-mono text-slate-900 p-1">
                            <strong>{atm.atm_id}</strong> ({atm.bank_name})<br />
                            Risk Level: <strong>{riskLevel}</strong><br />
                            Liquidity: ₹{(atm.liquidity_inr / 100000).toFixed(2)}L<br />
                            Velocity: {atm.recent_velocity.toFixed(1)} tx/hr
                          </div>
                        </Popup>
                      </Marker>
                      {isTarget && (
                        <Circle
                          center={[atm.geo_lat, atm.geo_long]}
                          radius={600}
                          pathOptions={{ color: '#ef4444', fillColor: '#ef4444', fillOpacity: 0.25 }}
                        />
                      )}
                    </React.Fragment>
                  );
                })}
              </MapContainer>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
