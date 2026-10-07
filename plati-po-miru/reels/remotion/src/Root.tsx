import {Composition} from 'remotion';
import {Reel} from './Reel';
import tl from '../public/timeline.json';

export const Root = () => (
  <Composition id="Reel" component={Reel} fps={30} width={1080} height={1920}
    durationInFrames={Math.ceil(tl.total * 30)} />
);
