# v2.7 Projection API Safety Rules

1. Projection API must not expose true_state.
2. Projection API must not expose raw WorldState internals.
3. Projection API must not expose hidden source IDs (source_record_id, source_signal_id, source_trace_id).
4. Projection API must not expose backend semantic_tags.
5. Projection API must not expose private resonance scores.
6. Projection API must not expose norm recognition/contestation scores, lifecycle deltas, interaction scores.
7. Projection API must not claim confirmed guilt/violation/corruption unless visible high-confidence evidence exists.
8. Rumor alone cannot become confirmed output.
9. Resonance alone cannot become confirmed output.
10. PlayerKnowledge is not true_state.
11. VisibleProjection is not true_state.
12. Projection API must use uncertainty language where evidence is incomplete.
13. High-risk coercive commands must remain safety/legitimacy/dispute pressure only.
14. Projection API must not describe operational harm instructions or successful harm outcomes.
15. Projection API must not create world changes.
16. Projection API is read-only.
