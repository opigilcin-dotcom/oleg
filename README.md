# 🎬 Oleg — AI YouTube Channel Studio

A team of specialized AI sub-agents + analytics tooling for building and running a
faceless / AI-generated YouTube channel end-to-end: from picking a profitable niche
to producing finished videos.

## 🤖 The agent team (`.claude/agents/`)

| Agent | Role | Powered by |
|-------|------|-----------|
| **niche-researcher** | Finds & validates profitable niches with a data-backed GO/NO-GO scorecard | NexLev + vidiq |
| **competitor-analyst** | Reverse-engineers winning channels into a "steal this" playbook | NexLev + vidiq |
| **scriptwriter** | Writes retention-optimized scripts with hooks + visual cues | vidiq + web |
| **thumbnail-titler** | Designs high-CTR thumbnails + titles (the "package"), scored & A/B'd | vidiq + higgsfield |
| **video-producer** | Turns a script into voiceover + AI visuals + a virality-checked cut | higgsfield + vidiq |

Invoke any agent from Claude Code, e.g.:
> "Use the **niche-researcher** to validate the true-crime faceless niche."
> "Have the **competitor-analyst** tear down @ChannelHandle."

## 🔁 The production pipeline

```
1. niche-researcher   →  pick the niche (data-backed)
2. competitor-analyst →  steal the winning formula
3. scriptwriter       →  hook + script + visual cues
4. thumbnail-titler   →  high-CTR package (title + thumb)
5. video-producer     →  voiceover + visuals + final cut
                          ↓
                      publish → analyze → iterate
```

## 🧰 Tooling available
- **NexLev** — 50k+ channel analytics: niches, RPM, revenue, outliers, faceless detection, transcripts.
- **vidiq** — keywords, trends, titles, thumbnails, scoring, voiceover, clips, b-roll.
- **higgsfield** — AI image/video/audio generation, voices, motion, upscaling, virality prediction.

## 📊 Niche research snapshot (2026-06)
Top faceless/AI niches breaking out right now (outlier ≥ 2):
- **History/Culture explainers** — RPM ~$4.6+, $4-6K/mo within weeks
- **True-crime / forensics** — highest RPM (~$5-7), evergreen
- **Manhwa/anime recaps** — fastest breakout (outlier 8-12 in ~40 days)
- **Paranormal/horror stories** — top earner in sample ($20K/mo)

> Run the niche-researcher for a fresh, full scorecard before committing.
