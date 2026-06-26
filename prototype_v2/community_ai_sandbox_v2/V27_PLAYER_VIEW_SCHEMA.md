# v2.7 Player-Facing View Schemas

## PlayerDashboardView
- view_id, title, summary, current_day, visible_situation, known_risks, unresolved_issues, known_active_norms, known_contested_norms, recent_reports, suggested_attention, confidence_label, uncertainty_note

## VisibleReportView
- view_id, title, body, confidence_label, channel_label, uncertainty_note, created_tick

## KnownClueView
- view_id, title, summary, confidence_label, source_channel_type, verification_suggested, safe_display_category

## VisibleNormView
- view_id, norm_title, player_status (proposed/emerging/active/contested/weakened/expired/unclear), summary, uncertainty_note, recent_evidence_summary

## VisibleResidentView
- view_id, name, public_role, visible_concerns, visible_recent_actions, uncertainty_note

## RecentEventView
- view_id, title, summary, visibility_level, confidence_label, round_index

## PlayerCommandContextView
- view_id, visible_situation, unresolved_issues, known_actors, known_norms, known_clues, uncertainty_warning

## ProjectionApiSnapshot
- dashboard, reports, clues, norms, residents, events, context

## Forbidden Fields (never in any view)
source_record_id, source_signal_id, source_trace_id, semantic_tags, private_resonance_score, recognition_score, contestation_score, lifecycle_delta, interaction_score, hidden_summary

## Future Helpers
get_player_dashboard_view, get_visible_report_view, get_known_clues_view, get_visible_norms_view, get_visible_residents_view, get_recent_events_view, get_player_command_context_view, get_projection_api_snapshot
