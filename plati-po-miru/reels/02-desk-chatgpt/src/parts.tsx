import React from 'react';
import {Easing, interpolate, spring, staticFile} from 'remotion';
import cfg from '../config.json';

export const FPS = cfg.fps;
export const C = cfg.colors;
export const T = cfg.texts;
export const A = cfg.assets;
export const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
export const ease = Easing.bezier(0.22, 1, 0.36, 1);
export const lerp = (f: number, a: number, b: number, from: number, to: number, e = ease) =>
  interpolate(f, [a, b], [from, to], {...clamp, easing: e});
export const sp = (f: number, delay: number, damping = 14, stiffness = 170) =>
  spring({frame: f - delay, fps: FPS, config: {damping, stiffness, mass: 0.9}});

// детерминированный «рандом» для рваных краёв
export const rnd = (i: number) => {
  const x = Math.sin(i * 127.1 + 311.7) * 43758.5453;
  return x - Math.floor(x);
};

// clip-path для бумажной полоски с рваными короткими краями
export const tornPolygon = (seed: number, steps = 14, amp = 3.2) => {
  const pts: string[] = [];
  for (let i = 0; i <= steps; i++) pts.push(`${(rnd(seed + i) * amp).toFixed(2)}% ${(i / steps) * 100}%`);
  for (let i = steps; i >= 0; i--) pts.push(`${(100 - rnd(seed + 50 + i) * amp).toFixed(2)}% ${(i / steps) * 100}%`);
  return `polygon(${pts.join(',')})`;
};

export const Fonts: React.FC = () => (
  <style>{`
    @font-face{font-family:M;src:url(${staticFile(A.fontMain)}) format('truetype');}
    @font-face{font-family:H;src:url(${staticFile(A.fontHand)}) format('truetype');}
    @font-face{font-family:TM;src:url(${staticFile(A.fontMono)}) format('truetype');}
  `}</style>
);

// фактура бумаги (SVG-шум), накладывается multiply
export const GrainDefs: React.FC = () => (
  <svg width={0} height={0} style={{position: 'absolute'}}>
    <filter id="grain">
      <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves={3} seed={7} />
      <feColorMatrix type="matrix" values="0 0 0 0 0.45  0 0 0 0 0.42  0 0 0 0 0.38  0 0 0 0.35 0" />
    </filter>
  </svg>
);
export const Grain: React.FC<{o?: number}> = ({o = 0.5}) => (
  <svg style={{position: 'absolute', inset: 0, width: '100%', height: '100%', mixBlendMode: 'multiply', opacity: o, pointerEvents: 'none'}}>
    <rect width="100%" height="100%" filter="url(#grain)" />
  </svg>
);

// Главный объект ролика — бумажная полоска с текстом (одна форма/фактура во всех трёх появлениях)
export const Strip: React.FC<{w: number; h: number; children: React.ReactNode; seed?: number}> = ({w, h, children, seed = 3}) => (
  <div style={{position: 'relative', width: w, height: h, filter: 'drop-shadow(0 22px 26px rgba(20,28,33,.28)) drop-shadow(0 4px 6px rgba(20,28,33,.18))'}}>
    <div style={{position: 'absolute', inset: 0, background: C.paper, clipPath: tornPolygon(seed), overflow: 'hidden',
      display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
      <Grain o={0.55} />
      <div style={{position: 'relative'}}>{children}</div>
    </div>
    {/* скотч */}
    <div style={{position: 'absolute', left: -18, top: -16, width: 120, height: 44, background: 'rgba(255,255,255,.62)', transform: 'rotate(-14deg)', boxShadow: '0 2px 4px rgba(0,0,0,.08)'}} />
    <div style={{position: 'absolute', right: -14, bottom: -14, width: 110, height: 42, background: 'rgba(255,255,255,.62)', transform: 'rotate(-10deg)', boxShadow: '0 2px 4px rgba(0,0,0,.08)'}} />
  </div>
);

// бумажный чип для кинетической типографики
export const Chip: React.FC<{children: React.ReactNode; bg?: string; color?: string; size?: number; rot?: number; seed?: number}> =
  ({children, bg = C.paper, color = C.ink, size = 104, rot = 0, seed = 9}) => (
  <div style={{display: 'inline-block', transform: `rotate(${rot}deg)`, filter: 'drop-shadow(0 12px 14px rgba(20,28,33,.22))'}}>
    <div style={{position: 'relative', background: bg, clipPath: tornPolygon(seed, 8, 2.2), padding: `${size * 0.12}px ${size * 0.34}px`, overflow: 'hidden'}}>
      <Grain o={bg === C.paper ? 0.5 : 0.25} />
      <div style={{position: 'relative', fontFamily: 'M', fontSize: size, lineHeight: 1, color, letterSpacing: -1.5, whiteSpace: 'nowrap'}}>{children}</div>
    </div>
  </div>
);

// рукописная бирка (реплика)
export const Tag: React.FC<{text: string; rot?: number; size?: number}> = ({text, rot = 2, size = 66}) => (
  <div style={{display: 'inline-block', transform: `rotate(${rot}deg)`, filter: 'drop-shadow(0 10px 12px rgba(20,28,33,.22))'}}>
    <div style={{position: 'relative', background: '#fff', clipPath: tornPolygon(21, 6, 2), padding: '10px 34px 14px', overflow: 'hidden'}}>
      <Grain o={0.35} />
      <div style={{position: 'relative', fontFamily: 'H', fontSize: size, color: C.ink, whiteSpace: 'nowrap'}}>{text}</div>
    </div>
  </div>
);

export const StickyNote: React.FC = () => (
  <div style={{width: 340, height: 340, position: 'relative', filter: 'drop-shadow(0 18px 18px rgba(20,28,33,.25))'}}>
    <div style={{position: 'absolute', inset: 0, background: C.note, overflow: 'hidden'}}>
      <Grain o={0.45} />
      <div style={{position: 'absolute', left: 34, top: 30, fontFamily: 'H', fontSize: 66, lineHeight: 1.0, color: '#3b3420'}}>
        {T.note.map((l, i) => <div key={i}>{l}</div>)}
      </div>
      <svg width={340} height={340} style={{position: 'absolute', inset: 0}}>
        <path d="M262 250 l14 30 l30 4 l-22 20 l6 30 l-28 -15 l-28 15 l6 -30 l-22 -20 l30 -4 z" fill="none" stroke={C.accent} strokeWidth={5} strokeLinejoin="round" />
      </svg>
    </div>
  </div>
);

export const ScriptPage: React.FC = () => (
  <div style={{width: 470, height: 560, position: 'relative', filter: 'drop-shadow(0 18px 22px rgba(20,28,33,.22))'}}>
    <div style={{position: 'absolute', inset: 0, background: '#fff', overflow: 'hidden', padding: '40px 38px', boxSizing: 'border-box'}}>
      <Grain o={0.3} />
      {T.script.map((l, i) => (
        <div key={i} style={{position: 'relative', fontFamily: 'TM', fontSize: 30, lineHeight: '52px', color: i === 0 || i === 6 ? C.ink : '#4a4f55', fontWeight: 700, height: 52}}>{l}</div>
      ))}
      <svg width={470} height={560} style={{position: 'absolute', inset: 0}}>
        <path d="M36 92 C 140 84, 260 98, 380 88" fill="none" stroke={C.accent} strokeWidth={5} strokeLinecap="round" />
        <path d="M400 210 c 20 -6 40 6 30 26" fill="none" stroke={C.accent} strokeWidth={4} strokeLinecap="round" />
      </svg>
    </div>
  </div>
);

export const EditorWindow: React.FC<{t: number}> = ({t}) => {
  const head = 140 + ((t * 9) % 560);
  const clips = [[0, 30, 190, C.accent], [0, 240, 150, '#6b7280'], [0, 410, 230, C.accent], [1, 60, 260, '#f59e0b'], [1, 350, 300, '#f59e0b'], [2, 20, 420, '#10b981'], [2, 470, 200, '#10b981']];
  return (
    <div style={{width: 820, height: 400, borderRadius: 22, background: C.editor, overflow: 'hidden', position: 'relative', boxShadow: '0 28px 40px rgba(20,28,33,.35)'}}>
      <div style={{height: 52, background: '#2a2d35', display: 'flex', alignItems: 'center', gap: 12, paddingLeft: 22}}>
        {['#ff5f57', '#febc2e', '#28c840'].map((c) => <div key={c} style={{width: 18, height: 18, borderRadius: 9, background: c}} />)}
        <div style={{marginLeft: 20, fontFamily: 'M', fontSize: 22, color: '#9aa0aa'}}>reel_v3.edit</div>
      </div>
      {[0, 1, 2].map((r) => <div key={r} style={{position: 'absolute', left: 30, right: 30, top: 100 + r * 92, height: 64, background: '#262931', borderRadius: 10}} />)}
      {clips.map(([r, x, w, c], i) => (
        <div key={i} style={{position: 'absolute', left: 30 + (x as number), top: 104 + (r as number) * 92, width: w as number, height: 56, borderRadius: 8, background: c as string, opacity: 0.9}} />
      ))}
      <div style={{position: 'absolute', left: head, top: 70, width: 4, height: 320, background: '#ff3b30'}} />
      <div style={{position: 'absolute', left: head - 10, top: 62, width: 24, height: 16, borderRadius: 4, background: '#ff3b30'}} />
    </div>
  );
};

export const Cursor: React.FC<{press: number}> = ({press}) => (
  <svg width={110} height={130} viewBox="0 0 22 26" style={{transform: `scale(${1 - 0.15 * press})`, transformOrigin: '10% 5%', filter: 'drop-shadow(0 6px 8px rgba(0,0,0,.35))'}}>
    <path d="M2 1 L2 20 L7 15.5 L10.5 23.5 L13.8 22 L10.4 14.3 L17 14.3 Z" fill="#fff" stroke={C.ink} strokeWidth={1.4} strokeLinejoin="round" />
  </svg>
);

export const PaperClip: React.FC = () => (
  <svg width={70} height={160} viewBox="0 0 70 160">
    <path d="M20 40 L20 130 a15 15 0 0 0 30 0 L50 25 a12 12 0 0 0 -24 0 L26 120" fill="none" stroke="#8a929c" strokeWidth={6} strokeLinecap="round" />
  </svg>
);
