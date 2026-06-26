# v2.7 Projection API Contract

## What Projection API Is
A read-only formatting boundary over v2.6 world_state that converts internal Cognitive Projection records into safe player-facing view payloads.

## What It Reads
PlayerKnowledgeRecord, VisibleProjectionRecord, ClueCandidateRecord (if player-visible), safe norm summaries, safe resident summaries, recent visible event summaries.

## What It Writes
Nothing to world_state in M1. Only returns view payloads in future runtime.

## What It Must Never Write
World changes, outcome mutations, hidden truth exposure, backend IDs, scores, tags.

## Confidence Labels
unknown → weak_suspicion → suspected → plausible → high_confidence → confirmed_by_visible_evidence

## Visible Norm Status Mapping
active → "active", provisional → "emerging", contested → "contested", weakened → "weakened", expired → "expired", proposed → "proposed", uncertain → "unclear"

## Uncertainty Phrasing
Use "currently unclear", "insufficient evidence to confirm", "further verification recommended", "may require audit", "visible evidence suggests but does not prove".

## Hidden Leak Testing
Verify no source IDs, semantic tags, resonance scores, or recognition/contestation scores appear in player-facing output.

## Extension
Add new view types by following the same read-only, hidden-sealed contract.
