import React from 'react';
import {AbsoluteFill, Audio, Easing, Img, interpolate, staticFile, useCurrentFrame} from 'remotion';
import cfg from '../config.json';
import {A, C, Chip, Cursor, EditorWindow, Fonts, GrainDefs, PaperClip, ScriptPage, StickyNote, Strip, T, Tag, clamp, lerp, rnd, sp} from './parts';

// Тайминг (кадры, 30 fps, всего 600)
const K = {freeze: 90, strip1: 96, reply: 116, cursorIn: 165, grab: 181, drag: [186, 214], push: [198, 228], reveal: 212,
  scroll: [240, 258], prodText: 248, zoom: [266, 292], underline: [282, 300], pull: [375, 410], calm: 380, link: 395,
  stripBack: [425, 447], code: [450, 470], final: 480};
const inOut = Easing.inOut(Easing.cubic);
const mix = (a: number, b: number, p: number) => a + (b - a) * p;

const QText = () => (
  <div style={{fontFamily: 'M', fontSize: 86, letterSpacing: -1, color: C.ink, whiteSpace: 'nowrap'}}>
    {T.question[0]}<span style={{color: C.accent}}>{T.question[1]}</span>
  </div>
);

export const DeskReel: React.FC = () => {
  const f = useCurrentFrame();
  const dt = Math.min(f, K.freeze); // после «стоп-кадра» коллаж замирает

  // ---------- полоска: 3 состояния одного объекта ----------
  const s1 = sp(f, K.strip1, 13, 220);
  const dragX = lerp(f, K.drag[0], K.drag[1], 0, -1650, Easing.in(Easing.cubic));
  const back = lerp(f, K.stripBack[0], K.stripBack[1], 0, 1);
  const isPromo = f >= K.stripBack[0];
  const stripX = isPromo ? mix(-1150, 0, back) : interpolate(s1, [0, 1], [-1500, 0]) + dragX;
  const stripY = isPromo ? 680 : 880;
  const stripRot = isPromo ? mix(-9, -2, back) : interpolate(s1, [0, 1], [-14, -3]) - (dragX < -1 ? 4 * Math.min(1, -dragX / 400) : 0);
  const stripScaleX = isPromo ? mix(0.3, 1, back) : 1;
  const codeReveal = lerp(f, K.code[0], K.code[1], 100, 0);
  const codeFs = Math.min(150, Math.floor(860 / (cfg.promoCode.length * 0.72)));

  // ---------- разрыв бумаги ----------
  const tearX = f < K.drag[0] ? 1400 : 1020 + dragX;
  const edge: [number, number][] = [];
  for (let k = 0; k <= 24; k++) { const y = k * 80; edge.push([tearX + (y - 880) * 0.18 + (rnd(k) - 0.5) * 40, y]); }
  const collageClip = tearX > 1300 ? 'none' : `polygon(0px 0px, ${edge.map(([x, y]) => `${x}px ${y}px`).join(',')}, 0px 1920px)`;
  const collageScale = lerp(f, K.push[0], K.push[1], 1, 1.3, Easing.in(Easing.quad));
  const collageOp = lerp(f, 210, K.push[1], 1, 0);
  const freeze = lerp(f, K.freeze, K.freeze + 7, 0, 1);

  // ---------- сайт: проход камеры → прокрутка → зум → в телефон ----------
  let a: number, bx: number, by: number;
  if (f < K.scroll[0]) { a = lerp(f, K.drag[0], K.push[1], 1.12, 1); bx = 540 * (1 - a); by = 960 * (1 - a); }
  else if (f < K.pull[0]) { a = lerp(f, K.zoom[0], K.zoom[1], 1, 1.25, inOut); bx = 430 * (1 - a); by = 900 * (1 - a); }
  else { const p = lerp(f, K.pull[0], K.pull[1], 0, 1, inOut); a = mix(1.25, 0.326, p); bx = mix(-107.5, 364, p); by = mix(-225, 920, p); }
  const pp = lerp(f, K.pull[0], K.pull[1], 0, 1, inOut);
  const siteClip = `inset(${mix(0, 964, pp)}px ${mix(0, 364, pp)}px ${mix(0, 204, pp)}px ${mix(0, 364, pp)}px round ${mix(0, 44, pp)}px)`;
  const sc = lerp(f, K.scroll[0], K.scroll[1], 0, 1, inOut);
  const underline = lerp(f, K.underline[0], K.underline[1], 520, 0);
  const prodOut = lerp(f, 368, 380, 1, 0);

  // ---------- курсор ----------
  const cIn = lerp(f, K.cursorIn, K.grab, 0, 1);
  const cx = f < K.drag[0] ? mix(1180, 985, cIn) : 985 + dragX;
  const cy = f < K.drag[0] ? mix(1560, 880, cIn) : 880 + dragX * 0.04;
  const press = f >= K.grab ? Math.min(1, (f - K.grab) / 3) : 0;

  // ---------- финальная спокойная композиция ----------
  const calmOp = lerp(f, K.pull[0], K.pull[0] + 20, 0, 1);
  const phoneIn = lerp(f, K.calm, K.pull[1], 0, 1);
  const sway = f > K.final ? Math.sin((f - K.final) / 18) : 0;
  const c1 = sp(f, K.calm + 5, 18, 120), c2 = sp(f, K.calm + 12, 18, 120), c3 = sp(f, K.calm + 18, 18, 120);

  const paperclipX = f < K.freeze ? 905 + f * 1.1 : 1004 + 16 * (1 - Math.exp(-(f - K.freeze) / 9));
  const paperclipR = f < K.freeze ? f * 0.9 : 81 + 14 * (1 - Math.exp(-(f - K.freeze) / 9));

  return (
    <AbsoluteFill style={{background: '#e7e7e4', overflow: 'hidden', isolation: 'isolate'}}>
      <Fonts /><GrainDefs />

      {/* ===== Сайт (под бумагой) ===== */}
      {f >= K.cursorIn && (
        <AbsoluteFill style={{clipPath: siteClip}}>
          <div style={{position: 'absolute', left: 0, top: 0, width: 1080, height: 1920, transformOrigin: '0 0', transform: `matrix(${a},0,0,${a},${bx},${by})`}}>
            <Img src={staticFile(A.site)} style={{position: 'absolute', left: 0, top: -1920 * sc, width: 1080, height: 1920}} />
            <div style={{position: 'absolute', left: 0, top: 1920 * (1 - sc), width: 1080, height: 1920, background: '#eef3fb'}}>
              <Img src={staticFile(A.card)} style={{position: 'absolute', left: 0, top: 26, width: 1080}} />
              <svg width={1080} height={1920} style={{position: 'absolute', inset: 0}}>
                <path d={`M${cfg.cardTitleX[0]} ${cfg.cardTitleY + 46} C ${cfg.cardTitleX[0] + 150} ${cfg.cardTitleY + 40}, ${cfg.cardTitleX[1] - 150} ${cfg.cardTitleY + 58}, ${cfg.cardTitleX[1]} ${cfg.cardTitleY + 44}`}
                  fill="none" stroke={C.accent} strokeWidth={10} strokeLinecap="round" strokeDasharray={520} strokeDashoffset={underline} />
              </svg>
            </div>
          </div>
        </AbsoluteFill>
      )}

      {/* ===== Рабочий коллаж (сцены 1–3) ===== */}
      {f < K.push[1] && (
        <AbsoluteFill style={{clipPath: collageClip, opacity: collageOp, transform: `scale(${collageScale})`,
          filter: `saturate(${1 - 0.45 * freeze}) brightness(${1 - 0.08 * freeze})`}}>
          <AbsoluteFill style={{transform: `scale(${1.04 + dt * 0.0005}) translateY(${-dt * 0.35}px)`}}>
            <Img src={staticFile(A.desk)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
          </AbsoluteFill>
          {(() => { const s = sp(f, -6, 12, 160); return (
            <div style={{position: 'absolute', left: interpolate(s, [0, 1], [-520, 64]), top: 196 + Math.sin(dt / 22) * 5, transform: `rotate(${interpolate(s, [0, 1], [-30, -6])}deg) scale(${interpolate(s, [0, 1], [1.12, 1])})`}}><StickyNote /></div>); })()}
          {(() => { const s = sp(f, 12, 13, 170); return (
            <div style={{position: 'absolute', left: interpolate(s, [0, 1], [1160, 578]), top: 140 + Math.cos(dt / 25) * 6, transform: `rotate(${interpolate(s, [0, 1], [18, 5])}deg) scale(${interpolate(s, [0, 1], [1.1, 1])})`}}><ScriptPage /></div>); })()}
          {(() => { const s = sp(f, 24, 13, 170); return (
            <div style={{position: 'absolute', left: 128, top: interpolate(s, [0, 1], [2150, 1330]) + Math.sin(dt / 30) * 4, transform: `rotate(${interpolate(s, [0, 1], [-9, -2])}deg) scale(${interpolate(s, [0, 1], [1.08, 1])})`}}><EditorWindow t={dt} /></div>); })()}
          <div style={{position: 'absolute', left: paperclipX, top: 1250, transform: `rotate(${paperclipR}deg)`}}><PaperClip /></div>
          {/* кинетическая типографика: главный вопрос */}
          {T.hook.map((w, i) => { const s = sp(f, 16 + i * 8, 11, 230); return (
            <div key={i} style={{position: 'absolute', width: '100%', top: 760 + i * 138, display: 'flex', justifyContent: 'center',
              opacity: Math.min(1, s * 3) * (1 - 0.75 * freeze), transform: `scale(${interpolate(s, [0, 1], [0.4, 1])})`}}>
              <Chip size={104} rot={[-2, 1.5, -1][i]} seed={30 + i} bg={i === 2 ? C.accent : C.paper} color={i === 2 ? '#fff' : C.ink}>{w}</Chip>
            </div>); })}
          <svg width={1080} height={1920} style={{position: 'absolute', inset: 0}}>
            <path d="M250 560 C 230 640, 260 700, 330 742 M 300 722 l 32 22 l -6 -36" fill="none" stroke={C.ink} strokeWidth={6} strokeLinecap="round" strokeLinejoin="round"
              strokeDasharray={320} strokeDashoffset={lerp(f, 44, 62, 320, 0)} />
          </svg>
          {/* реплика в паузе */}
          {f >= K.reply && (
            <div style={{position: 'absolute', width: '100%', top: 1080, display: 'flex', justifyContent: 'center', opacity: lerp(f, K.drag[0], K.drag[0] + 6, 1, 0),
              transform: `scale(${sp(f, K.reply, 12, 200)})`}}><Tag text={T.reply} rot={2} /></div>
          )}
          {/* бумажная кайма разрыва */}
          {tearX < 1300 && (
            <svg width={1080} height={1920} style={{position: 'absolute', inset: 0, overflow: 'visible', filter: 'drop-shadow(6px 0 8px rgba(0,0,0,.35))'}}>
              <polyline points={edge.map(([x, y]) => `${x},${y}`).join(' ')} fill="none" stroke={C.paper} strokeWidth={16} strokeLinejoin="round" />
            </svg>
          )}
        </AbsoluteFill>
      )}

      {/* ===== «Вот один из вариантов» ===== */}
      {f >= K.reveal && f < K.scroll[0] + 6 && (
        <div style={{position: 'absolute', width: '100%', top: 1470, display: 'flex', justifyContent: 'center', opacity: lerp(f, K.scroll[0], K.scroll[0] + 6, 1, 0),
          transform: `scale(${sp(f, K.reveal, 12, 200)})`}}><Tag text={T.reveal} rot={-2} /></div>
      )}

      {/* ===== Текст продукта ===== */}
      {f >= K.prodText && f < 382 && (
        <div style={{position: 'absolute', width: '100%', top: 118, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 14, opacity: prodOut}}>
          <div style={{transform: `scale(${sp(f, K.prodText, 12, 200)})`}}><Tag text={T.productBrand} size={58} rot={-1.5} /></div>
          <div style={{transform: `scale(${sp(f, K.prodText + 6, 12, 200)})`}}><Chip size={74} rot={-1} seed={41}>{T.productTitle[0]}</Chip></div>
          <div style={{transform: `scale(${sp(f, K.prodText + 12, 12, 200)})`}}><Chip size={60} rot={1} seed={42} bg={C.accent} color="#fff">{T.productTitle[1]}</Chip></div>
        </div>
      )}

      {/* ===== Финальная композиция: стол + телефон ===== */}
      {f >= K.pull[0] && (
        <AbsoluteFill style={{opacity: calmOp, zIndex: -1}}>
          <Img src={staticFile(A.desk)} style={{width: '100%', height: '100%', objectFit: 'cover', transform: 'scale(1.04)'}} />
          <div style={{position: 'absolute', left: interpolate(c1, [0, 1], [-420, 24]), top: 1060, transform: `rotate(${-9 + sway}deg) scale(.7)`, transformOrigin: '0 0'}}><StickyNote /></div>
          <div style={{position: 'absolute', left: interpolate(c2, [0, 1], [1200, 800]), top: 1010, transform: `rotate(${7 - sway * 0.8}deg) scale(.6)`, transformOrigin: '0 0'}}><ScriptPage /></div>
          <div style={{position: 'absolute', left: -170, top: interpolate(c3, [0, 1], [2100, 1700]), transform: `rotate(${-5 + sway * 0.5}deg) scale(.62)`, transformOrigin: '0 0'}}><EditorWindow t={60} /></div>
          <div style={{position: 'absolute', left: 350, top: 950 + sway * 3, width: 380, height: 780, borderRadius: 58, background: '#121316',
            boxShadow: '0 40px 60px rgba(20,28,33,.4)', opacity: phoneIn, transform: `scale(${mix(1.12, 1, phoneIn)})`}} />
        </AbsoluteFill>
      )}

      {/* ===== Ссылка в описании ===== */}
      {f >= K.link && (
        <div style={{position: 'absolute', width: '100%', top: 846, display: 'flex', justifyContent: 'center', transform: `scale(${sp(f, K.link, 13, 200)})`}}>
          <Tag text={T.link} size={58} rot={-1.5} />
        </div>
      )}

      {/* ===== Заголовок промо + выгода ===== */}
      {f >= K.final && (
        <div style={{position: 'absolute', width: '100%', top: 196, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 10}}>
          <div style={{transform: `translateY(${interpolate(sp(f, K.final, 14, 200), [0, 1], [-60, 0])}px)`, opacity: sp(f, K.final, 14, 200)}}><Chip size={70} rot={-1.5} seed={51}>{T.promoHeader[0]}</Chip></div>
          <div style={{transform: `translateY(${interpolate(sp(f, K.final + 5, 14, 200), [0, 1], [-60, 0])}px)`, opacity: sp(f, K.final + 5, 14, 200)}}><Chip size={56} rot={1} seed={52}>{T.promoHeader[1]}</Chip></div>
          <div style={{marginTop: 6, transform: `scale(${sp(f, K.final + 12, 11, 220)})`}}><Chip size={54} rot={-2} seed={53} bg={C.accent} color="#fff">{T.promoBenefit}</Chip></div>
        </div>
      )}
      {f >= K.final && (
        <div style={{position: 'absolute', width: '100%', top: 150, textAlign: 'center', fontFamily: 'M', fontSize: 24, color: 'rgba(20,28,33,.6)'}}>{T.adLabel}</div>
      )}

      {/* ===== Полоска (сквозной объект) ===== */}
      {f >= K.strip1 && (f < K.drag[1] + 2 || isPromo) && (
        <div style={{position: 'absolute', left: 540 - 490 + stripX, top: stripY - 115, transform: `rotate(${stripRot}deg) scaleX(${stripScaleX})`, transformOrigin: '0% 50%'}}>
          <Strip w={980} h={230} seed={isPromo ? 3 : 3}>
            {isPromo ? (
              <div style={{position: 'relative', fontFamily: 'M', fontSize: codeFs, letterSpacing: 6, color: C.accent, clipPath: `inset(0 ${codeReveal}% 0 0)`}}>
                {cfg.promoCode}
                {/* один блик по коду в начале финала (код не двигается) */}
                <div style={{position: 'absolute', inset: 0, background: 'linear-gradient(105deg, transparent 35%, rgba(255,255,255,.85) 50%, transparent 65%)',
                  transform: `translateX(${lerp(f, K.final + 2, K.final + 20, -120, 120)}%)`, mixBlendMode: 'screen'}} />
              </div>
            ) : <QText />}
          </Strip>
        </div>
      )}

      {/* ===== Курсор ===== */}
      {f >= K.cursorIn && f < K.drag[1] && (
        <div style={{position: 'absolute', left: cx, top: cy}}>
          {press > 0 && <div style={{position: 'absolute', left: -30, top: -30, width: 60, height: 60, borderRadius: 30, border: `5px solid ${C.accent}`, opacity: 1 - press * 0.6, transform: `scale(${0.6 + press})`}} />}
          <Cursor press={press} />
        </div>
      )}

      <Audio src={staticFile(A.audio)} />
    </AbsoluteFill>
  );
};
