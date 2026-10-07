import React from 'react';
import {
  AbsoluteFill, Audio, Easing, Img, Sequence, interpolate, spring,
  staticFile, useCurrentFrame, useVideoConfig,
} from 'remotion';
import tl from '../public/timeline.json';

// Рилс 1080x1920: кадры с Ken Burns + плашки + субтитры по словам + оверлеи-эффекты.
// Все тайминги приходят из public/timeline.json (его пишет prep.py).

type Shot = {img: string; start: number; dur: number; z0: number; z1: number; fx: number; fy: number; overlay?: string; shake?: boolean};
type Seg = {start: number; dur: number; title: string; color: string; fx?: string; subs: boolean; shots: Shot[]};
type Word = {s: number; e: number; w: string; chunk: number};

const FPS = 30;
const fr = (s: number) => Math.round(s * FPS);
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const COLORS: Record<string, string> = {red: '#FF2D3D', blue: '#0A7CFF', green: '#16C060', yellow: '#FFD600'};
const segs = tl.segments as Seg[];
const words = tl.words as Word[];
const TOTAL = fr(tl.total);

const outline = (px: number, c = '#000') => {
  const s: string[] = [];
  for (let a = 0; a < 360; a += 30) {
    const r = (a * Math.PI) / 180;
    s.push(`${(Math.cos(r) * px).toFixed(1)}px ${(Math.sin(r) * px).toFixed(1)}px 0 ${c}`);
  }
  return s.join(',') + `, 0 ${px + 4}px ${px * 2}px rgba(0,0,0,.55)`;
};

// --- Оверлеи, привязанные к картинке (едут вместе с Ken Burns) ---
const TrapCircle: React.FC<{t: number}> = ({t}) => {
  const C = 2 * Math.PI * 140;
  const draw = interpolate(t, [4, 16], [C, 0], {...clamp, easing: Easing.out(Easing.cubic)});
  const pulse = 1 + 0.04 * Math.sin(Math.max(0, t - 16) / 3);
  const tag = spring({frame: t - 14, fps: FPS, config: {damping: 10, stiffness: 180}});
  return (
    <AbsoluteFill>
      <svg width={1080} height={1920} style={{position: 'absolute'}}>
        <g transform={`translate(450 1066) scale(${pulse}) rotate(-90)`}>
          <ellipse rx={160} ry={118} fill="none" stroke="#FF2D3D" strokeWidth={14}
            strokeDasharray={C} strokeDashoffset={draw} strokeLinecap="round"
            style={{filter: 'drop-shadow(0 0 14px rgba(255,45,61,.9))'}} />
        </g>
      </svg>
      <div style={{position: 'absolute', left: 560, top: 905, transform: `scale(${tag}) rotate(8deg)`,
        background: '#FF2D3D', color: '#fff', fontSize: 50, padding: '8px 22px', borderRadius: 14,
        boxShadow: '0 8px 0 rgba(0,0,0,.35)'}}>ЛОВУШКА</div>
    </AbsoluteFill>
  );
};

const ReceiptBox: React.FC<{t: number}> = ({t}) => {
  const P = 2 * (470 + 180);
  const draw = interpolate(t, [6, 22], [P, 0], {...clamp, easing: Easing.out(Easing.cubic)});
  return (
    <svg width={1080} height={1920} style={{position: 'absolute'}}>
      <rect x={100} y={975} width={470} height={180} rx={18} fill="rgba(255,214,0,.12)" stroke="#FFD600"
        strokeWidth={12} strokeDasharray={P} strokeDashoffset={draw}
        style={{filter: 'drop-shadow(0 0 12px rgba(255,214,0,.9))'}} />
    </svg>
  );
};

// --- Кадр ---
const ShotView: React.FC<{shot: Shot; pre: number; dur: number; isHook: boolean; isLoop?: boolean}> = ({shot, pre, dur, isHook, isLoop}) => {
  const f = useCurrentFrame();
  const t = f - pre;
  const p = Math.min(Math.max(t / dur, 0), 1);
  const z = shot.z0 + (shot.z1 - shot.z0) * Easing.inOut(Easing.quad)(p);
  const enter = pre ? interpolate(f, [0, pre], [0, 1], clamp) : 1;
  const hookPunch = isHook ? interpolate(f, [0, 9], [1.45, 1], {...clamp, easing: Easing.out(Easing.back(1.6))}) : 1;
  const entryScale = pre ? interpolate(enter, [0, 1], [1.3, 1]) : hookPunch;
  const blur = pre ? interpolate(enter, [0, 1], [18, 0]) : 0;
  const opacity = pre ? interpolate(f, [0, 3], [0, 1], clamp) : 1;
  const shakeAmt = (isHook ? interpolate(f, [0, 14], [20, 0], clamp) : 0) + (shot.shake ? interpolate(t, [0, 12], [16, 0], clamp) : 0);
  const sx = Math.sin(f * 2.3) * shakeAmt;
  const sy = Math.cos(f * 3.1) * shakeAmt;
  return (
    <AbsoluteFill style={{opacity, filter: `blur(${blur}px) contrast(1.08) saturate(1.18)`}}>
      <AbsoluteFill style={{transform: `translate(${sx}px,${sy}px) scale(${z * entryScale})`,
        transformOrigin: `${shot.fx * 100}% ${shot.fy * 100}%`}}>
        <Img src={staticFile(shot.img)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
        {!isLoop && shot.overlay === 'circle' && <TrapCircle t={t} />}
        {!isLoop && shot.overlay === 'receipt' && <ReceiptBox t={t} />}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// --- Плашка-заголовок: удар с отскоком ---
const Title: React.FC<{seg: Seg; idx: number}> = ({seg, idx}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const d = fr(seg.dur);
  const s = spring({frame: f, fps, config: {damping: 11, stiffness: 210, mass: 0.8}});
  const out = interpolate(f, [d - 5, d], [1, 0], clamp);
  const scale = interpolate(s, [0, 1], [idx === 0 ? 1.5 : 1.9, 1]) * interpolate(out, [0, 1], [0.7, 1]);
  const rot = interpolate(s, [0, 1], [-9, idx % 2 ? 2 : -2]);
  const lines = seg.title.split('\n');
  const bg = COLORS[seg.color] || COLORS.red;
  return (
    <div style={{position: 'absolute', top: 250, width: '100%', display: 'flex', flexDirection: 'column',
      alignItems: 'center', gap: 10, opacity: out, transform: `scale(${scale}) rotate(${rot}deg)`}}>
      {lines.map((l, i) => (
        <div key={i} style={{background: i === 0 ? bg : '#fff', color: i === 0 ? '#fff' : '#111',
          fontSize: Math.min(idx === 0 ? 104 : 88, Math.floor(960 / (l.length * 0.72))), lineHeight: 1.05, padding: '12px 30px', borderRadius: 20,
          letterSpacing: -1, boxShadow: '0 10px 0 rgba(0,0,0,.35)', whiteSpace: 'nowrap'}}>{l}</div>
      ))}
    </div>
  );
};

// --- Субтитры: 3 слова, текущее — жёлтое и «прыгает» ---
const Subs: React.FC = () => {
  const frame = useCurrentFrame();
  const t = frame / FPS;
  let k = -1;
  for (let i = 0; i < words.length; i++) {
    if (words[i].s <= t + 0.02) k = i; else break;
  }
  if (k < 0) return null;
  const cur = words[k];
  const next = words[k + 1];
  if (t > cur.e + 0.35 && (!next || next.s > t)) return null;
  const segOf = segs.findIndex((s) => t >= s.start && t < s.start + s.dur);
  if (segOf >= 0 && !segs[segOf].subs) return null;
  const chunk = words.filter((w) => w.chunk === cur.chunk);
  const chunkStart = fr(chunk[0].s);
  const pop = spring({frame: frame - chunkStart, fps: FPS, config: {damping: 12, stiffness: 260}});
  return (
    <div style={{position: 'absolute', top: 1150, width: '100%', display: 'flex', justifyContent: 'center',
      flexWrap: 'wrap', gap: '0 34px', padding: '0 50px', boxSizing: 'border-box',
      transform: `scale(${interpolate(pop, [0, 1], [0.6, 1])})`}}>
      {chunk.map((w, i) => {
        const active = w === cur;
        const ws = spring({frame: frame - fr(w.s), fps: FPS, config: {damping: 9, stiffness: 300}});
        return (
          <span key={i} style={{fontSize: 86, color: active ? '#FFD600' : '#fff', textShadow: outline(7),
            display: 'inline-block', transform: `scale(${active ? interpolate(ws, [0, 1], [1.22, 1.05]) : 1})`}}>
            {w.w.toUpperCase()}
          </span>
        );
      })}
    </div>
  );
};

// --- Эффекты сегментов ---
const PriceCounter: React.FC<{dur: number}> = ({dur}) => {
  const f = useCurrentFrame();
  const inS = spring({frame: f - 6, fps: FPS, config: {damping: 12}});
  const v = interpolate(f, [24, 60], [100, 108], {...clamp, easing: Easing.out(Easing.cubic)});
  const hot = f > 40;
  const out = interpolate(f, [dur - 6, dur], [1, 0], clamp);
  return (
    <div style={{position: 'absolute', top: 640, width: '100%', display: 'flex', justifyContent: 'center',
      opacity: out, transform: `translateY(${interpolate(inS, [0, 1], [80, 0])}px) scale(${inS})`}}>
      <div style={{background: 'rgba(0,0,0,.78)', borderRadius: 28, padding: '22px 44px', display: 'flex',
        alignItems: 'center', gap: 26, border: `6px solid ${hot ? '#FF2D3D' : '#fff'}`}}>
        <span style={{color: '#bbb', fontSize: 58, textDecoration: 'line-through'}}>100 $</span>
        <span style={{color: '#fff', fontSize: 58}}>→</span>
        <span style={{color: hot ? '#FF2D3D' : '#fff', fontSize: 92,
          transform: `scale(${hot ? 1 + 0.06 * Math.sin(f / 2) : 1})`, display: 'inline-block'}}>{v.toFixed(0)} $</span>
      </div>
    </div>
  );
};

const Stamp: React.FC<{dur: number}> = ({dur}) => {
  const f = useCurrentFrame();
  const s = spring({frame: f - 12, fps: FPS, config: {damping: 9, stiffness: 160}});
  const out = interpolate(f, [dur - 6, dur], [1, 0], clamp);
  return (
    <div style={{position: 'absolute', top: 640, width: '100%', display: 'flex', justifyContent: 'center', opacity: out * Math.min(1, s * 2)}}>
      <div style={{width: 420, height: 420, borderRadius: '50%', border: '16px solid #16C060', background: 'rgba(22,192,96,.22)',
        display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
        transform: `scale(${interpolate(s, [0, 1], [3, 1])}) rotate(-12deg)`, boxShadow: '0 0 40px rgba(22,192,96,.7)'}}>
        <svg width={130} height={110} viewBox="0 0 130 110"><path d="M10 58 L48 94 L120 12" fill="none" stroke="#fff" strokeWidth={22} strokeLinecap="round" strokeLinejoin="round" /></svg>
        <div style={{color: '#fff', fontSize: 60, textAlign: 'center', lineHeight: 1.05, textShadow: outline(5)}}>МЕСТНАЯ<br />ВАЛЮТА</div>
      </div>
    </div>
  );
};

const SaveHint: React.FC = () => {
  const f = useCurrentFrame();
  const s = spring({frame: f - 8, fps: FPS, config: {damping: 8}});
  const bob = Math.sin(f / 4) * 14;
  return (
    <div style={{position: 'absolute', right: 150, top: 1420, transform: `translateY(${bob}px) scale(${s})`,
      display: 'flex', alignItems: 'center', gap: 18}}>
      <div style={{color: '#fff', fontSize: 68, textShadow: outline(6)}}>СОХРАНИ</div>
      <svg width={140} height={165} viewBox="0 0 110 130" style={{filter: 'drop-shadow(0 6px 10px rgba(0,0,0,.6))'}}>
        <path d="M15 8 H95 V122 L55 92 L15 122 Z" fill="#FFD600" stroke="#000" strokeWidth={8} strokeLinejoin="round" />
      </svg>
      <svg width={90} height={60} viewBox="0 0 90 60"><path d="M5 30 H70 M50 8 L78 30 L50 52" fill="none" stroke="#fff" strokeWidth={12} strokeLinecap="round" strokeLinejoin="round" /></svg>
    </div>
  );
};

const Flash: React.FC<{at: number}> = ({at}) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [at - 1, at + 1, at + 5], [0, 0.6, 0], clamp);
  return o > 0 ? <AbsoluteFill style={{background: '#fff', opacity: o}} /> : null;
};

export const Reel: React.FC = () => {
  const frame = useCurrentFrame();
  const first = segs[0].shots[0];
  return (
    <AbsoluteFill style={{background: '#000', fontFamily: 'M'}}>
      <style>{`@font-face{font-family:M;src:url(${staticFile('Montserrat-ExtraBold.ttf')}) format('truetype');}`}</style>

      {segs.map((seg, i) => seg.shots.map((sh, j) => {
        const isHook = i === 0 && j === 0;
        const pre = isHook ? 0 : 5;
        const from = fr(sh.start);
        return (
          <Sequence key={`${i}-${j}`} from={from - pre} durationInFrames={fr(sh.dur) + pre + 1}>
            <ShotView shot={sh} pre={pre} dur={fr(sh.dur)} isHook={isHook} />
          </Sequence>
        );
      }))}

      {/* петля: в конце «въезжаем» обратно в первый кадр */}
      <Sequence from={TOTAL - 6} durationInFrames={6}>
        <ShotView shot={{...first, z0: 1.0, z1: 1.0}} pre={6} dur={6} isHook={false} isLoop />
      </Sequence>

      <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 55%, transparent 55%, rgba(0,0,0,.5) 100%)'}} />
      <AbsoluteFill style={{background: 'linear-gradient(to bottom, rgba(0,0,0,.35), transparent 28%, transparent 70%, rgba(0,0,0,.35))'}} />

      {segs.map((seg, i) => i > 0 && <Flash key={`f${i}`} at={fr(seg.start)} />)}

      {segs.map((seg, i) => (
        <Sequence key={`t${i}`} from={fr(seg.start)} durationInFrames={fr(seg.dur)}>
          <Title seg={seg} idx={i} />
          {seg.fx === 'counter' && <PriceCounter dur={fr(seg.dur)} />}
          {seg.fx === 'stamp' && <Stamp dur={fr(seg.dur)} />}
          {seg.fx === 'save' && <SaveHint />}
        </Sequence>
      ))}

      <Subs />

      {/* полоса прогресса */}
      <div style={{position: 'absolute', top: 0, left: 0, height: 12, width: `${(frame / TOTAL) * 100}%`,
        background: '#FFD600', boxShadow: '0 0 12px rgba(255,214,0,.8)'}} />

      <Audio src={staticFile('vo.wav')} />
      {(tl.sfx as {file: string; t: number; vol: number}[]).map((x, i) => (
        <Sequence key={`s${i}`} from={Math.max(0, fr(x.t))}>
          <Audio src={staticFile(x.file)} volume={x.vol} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
