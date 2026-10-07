import {Composition} from 'remotion';
import {DeskReel} from './DeskReel';
import cfg from '../config.json';

export const Root = () => (
  <Composition id="DeskReel" component={DeskReel} fps={cfg.fps} width={1080} height={1920}
    durationInFrames={cfg.durationInFrames} />
);
