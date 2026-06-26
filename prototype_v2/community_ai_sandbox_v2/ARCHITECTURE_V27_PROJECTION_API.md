# v2.7 Projection API Architecture

## 1. Goal

Define the Projection API contract that converts internal world_state into safe, player-facing views without exposing true_state or hidden backend internals.

## 2. Why Projection API Is Needed

v2.6's Cognitive Projection creates PlayerKnowledge and VisibleProjection records inside the simulation. The Projection API is the next layer — it formats those internal records into safe player-facing payloads for CLI/UI.

## 3. Relation to v2.6

Projection API reads v2.6's Cognitive Projection outputs. It does not replace them. It is a formatting boundary, not a new simulation mechanism.

## 4. Projection API vs Cognitive Projection

- **Cognitive Projection** (v2.5-v2.6): internal simulation mechanism creating PlayerKnowledge and VisibleProjection records from evidence-signal history.
- **Projection API** (v2.7): player-facing data boundary formatting safe views for CLI/UI.

## 5. Player-Facing View Types

1. PlayerDashboardView — main overview
2. VisibleReportView — recent reports
3. KnownClueView — clues known to player
4. VisibleNormView — norms as player understands them
5. VisibleResidentView — safe resident summaries
6. RecentEventView — recent visible events
7. PlayerCommandContextView — context for next command
8. ProjectionApiSnapshot — combined payload

## 6. Hidden vs Visible Boundary

Hidden (never in player view):
- source_record_id, source_signal_id, source_trace_id
- semantic_tags
- private_resonance_score
- recognition_score, contestation_score
- lifecycle_delta, interaction_score
- hidden_summary

Visible (allowed in player view):
- title, summary, confidence_label
- uncertainty_note, source_channel_label
- round_index, safe_tags

## 7. Confidence and Uncertainty

Confidence labels: unknown, weak_suspicion, suspected, plausible, high_confidence, confirmed_by_visible_evidence

Uncertainty required where evidence is incomplete.

## 8-14. (See companion docs)
