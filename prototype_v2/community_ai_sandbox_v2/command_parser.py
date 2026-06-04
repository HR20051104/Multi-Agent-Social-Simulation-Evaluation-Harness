"""Command parser for the v2 rule-mode CLI."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))

from src.evidence_engine import hold_meeting, plant_informant, run_audit
from src.report_engine import generate_debug, generate_status
from src.world import create_default_world, run_tick
from src.models import WorldState


def parse_and_execute(world: WorldState, command: str) -> str:
    parts = command.strip().split()
    if not parts:
        return ""

    cmd = parts[0].lower()

    if cmd == "help":
        return _help()
    if cmd == "quit":
        return "__QUIT__"

    if cmd in {"status", "report"}:
        return generate_status(world)
    if cmd == "nodes":
        return _cmd_nodes(world)
    if cmd == "node" and len(parts) >= 2:
        return _cmd_node(world, parts[1])
    if cmd == "edges" and len(parts) >= 2:
        return _cmd_edges(world, parts[1])
    if cmd == "objects":
        return _cmd_objects(world)
    if cmd == "object" and len(parts) >= 2:
        return _cmd_object(world, parts[1])
    if cmd == "backgrounds":
        return _cmd_backgrounds(world)
    if cmd == "background" and len(parts) >= 2:
        return _cmd_background(world, parts[1])
    if cmd == "promotion_candidates":
        return _cmd_promotion_candidates(world)
    if cmd == "promote_debug":
        return _cmd_promote_debug(world)
    if cmd == "tasks":
        return _cmd_tasks(world)
    if cmd == "signals":
        return _cmd_signals(world)
    if cmd == "knowledge":
        return _cmd_knowledge(world)

    if cmd == "tick":
        return _cmd_tick(world)
    if cmd == "wait" and len(parts) >= 2:
        return _cmd_wait(world, parts[1])

    if cmd == "assign_task" and len(parts) >= 6:
        return _cmd_assign_task(world, parts[1], parts[2], int(parts[3]), int(parts[4]), int(parts[5]))
    if cmd == "approve_task" and len(parts) >= 5:
        return _cmd_approve_task(world, parts[1], int(parts[2]), int(parts[3]), int(parts[4]))
    if cmd == "force_task" and len(parts) >= 2:
        return _cmd_force_task(world, parts[1])

    if cmd == "appoint" and len(parts) >= 3:
        return _cmd_appoint(world, parts[1], parts[2])
    if cmd == "appoint_deputy" and len(parts) >= 3:
        return _cmd_appoint_deputy(world, parts[1], parts[2])
    if cmd == "promise" and len(parts) >= 4:
        return _cmd_promise(world, parts[1], parts[2], int(parts[3]))
    if cmd == "public_rebuke" and len(parts) >= 2:
        return _cmd_public_rebuke(world, parts[1])
    if cmd == "private_warning" and len(parts) >= 2:
        return _cmd_private_warning(world, parts[1])

    if cmd == "audit" and len(parts) >= 2:
        return _cmd_audit(world, parts[1])
    if cmd == "plant_informant" and len(parts) >= 2:
        return _cmd_plant_informant(world, parts[1])
    if cmd == "meeting":
        return "\n".join(hold_meeting(world))

    if cmd == "debug_true":
        return generate_debug(world)

    return f"Unknown command: {command}\nType 'help' to see available commands."


def _help() -> str:
    return """
=== v2 Commands ===
  help
  status / report
  nodes
  node <id>
  edges <id>
  objects
  object <id>
  backgrounds
  background <id>
  promotion_candidates
  promote_debug
  tasks
  signals
  knowledge
  tick
  wait <n>
  assign_task <agent> <type> <budget> <mat> <labor>
  approve_task <task_id> <budget> <mat> <labor>
  force_task <task_id>
  appoint <node_id> <position_id>
  appoint_deputy <node_id> <position_id>
  promise <target> <topic> <deadline_ticks>
  public_rebuke <node_id>
  private_warning <node_id>
  audit <target_id>
  plant_informant <target_id>
  meeting
  debug_true
  quit
""".strip()


def _cmd_nodes(world: WorldState) -> str:
    lines = ["=== Nodes ==="]
    for node in world.social_nodes.values():
        lines.append(
            f"  {node.id}: {node.name} ({node.node_type}) "
            f"stress={node.stress:.0f} fear={node.fear:.0f} "
            f"honesty={node.report_honesty:.0f} core={node.overall_core_score:.0f} "
            f"sustained={node.sustained_core_score:.0f}"
        )
    return "\n".join(lines)


def _cmd_node(world: WorldState, node_id: str) -> str:
    node = world.social_nodes.get(node_id)
    if not node:
        return f"Node {node_id} does not exist."
    return (
        f"=== {node.id}: {node.name} ===\n"
        f"type={node.node_type} active={node.active}\n"
        f"stress={node.stress:.0f} fear={node.fear:.0f} anger={node.anger:.0f} "
        f"hope={node.hope:.0f} morale={node.morale:.0f} resentment={node.resentment:.0f}\n"
        f"compliance={node.compliance_tendency:.0f} conceal={node.concealment_tendency:.0f} "
        f"cooperate={node.cooperation_tendency:.0f} honesty={node.report_honesty:.0f}\n"
        f"authority={node.authority_centrality:.0f} info={node.information_centrality:.0f} "
        f"resource={node.resource_centrality:.0f} access={node.access_to_chief:.0f} "
        f"core={node.overall_core_score:.0f} sustained={node.sustained_core_score:.0f}\n"
        f"signal_exposure={node.signal_exposure_score:.0f} resource_control={node.resource_control_score:.0f} "
        f"task_relevance={node.task_relevance_score:.0f} contact_frequency={node.contact_frequency_score:.0f} "
        f"clue_relevance={node.clue_relevance_score:.0f} group_attention={node.group_attention_score:.0f}"
    )


def _cmd_edges(world: WorldState, node_id: str) -> str:
    from src.social_network import get_all_edges_for_node

    edges = get_all_edges_for_node(world, node_id)
    if not edges:
        return f"No edges found for {node_id}."
    lines = [f"=== Edges for {node_id} ==="]
    for edge in edges:
        lines.append(
            f"  {edge.source_id}->{edge.target_id}: trust={edge.trust:.0f} authority={edge.authority:.0f} "
            f"fear={edge.fear:.0f} obedience={edge.obedience:.0f} info_flow={edge.information_flow:.0f} "
            f"secrecy={edge.secrecy:.0f} empathy={edge.empathy:.0f} dependency={edge.dependency:.0f} "
            f"competition={edge.competition:.0f}"
        )
    return "\n".join(lines)


def _cmd_objects(world: WorldState) -> str:
    lines = ["=== Objects ==="]
    for obj in world.world_objects.values():
        lines.append(f"  {obj.id}: {obj.name} [{obj.object_type}] status={obj.status}")
    return "\n".join(lines)


def _cmd_backgrounds(world: WorldState) -> str:
    lines = ["=== Background Residents ==="]
    for resident in world.background_residents.values():
        lines.append(
            f"  {resident.id}: {resident.name} group={resident.home_group_id} "
            f"status={resident.status}"
        )
    return "\n".join(lines)


def _cmd_background(world: WorldState, resident_id: str) -> str:
    resident = world.get_background_resident(resident_id)
    if not resident:
        return f"Background resident {resident_id} does not exist."
    return (
        f"=== {resident.id}: {resident.name} ===\n"
        f"group={resident.home_group_id} building={resident.home_building_id} status={resident.status}\n"
        f"roles={','.join(resident.role_tags) if resident.role_tags else '-'} "
        f"locations={','.join(resident.location_tags) if resident.location_tags else '-'}\n"
        f"candidate_since={resident.candidate_since_tick} promoted_node={resident.promoted_node_id}"
    )


def _cmd_promotion_candidates(world: WorldState) -> str:
    residents = [resident for resident in world.background_residents.values() if resident.status == "candidate"]
    if not residents:
        return "No visible promotion candidates."
    lines = ["=== Promotion Candidates ==="]
    for resident in residents:
        lines.append(
            f"  {resident.id}: {resident.name} group={resident.home_group_id} "
            f"pressure={resident.promotion_pressure:.0f} reason={resident.promotion_reason or 'emerging'}"
        )
    return "\n".join(lines)


def _cmd_promote_debug(world: WorldState) -> str:
    lines = ["=== Promotion Debug ==="]
    for resident in world.background_residents.values():
        lines.append(
            f"  {resident.id}: status={resident.status} pressure={resident.promotion_pressure:.0f} "
            f"signal={resident.signal_exposure_score:.0f} clue={resident.clue_relevance_score:.0f} "
            f"resource={resident.resource_position_score:.0f} attention={resident.group_attention_score:.0f} "
            f"event={resident.event_relevance_score:.0f} contact={resident.contact_with_core_score:.0f} "
            f"reason={resident.promotion_reason or '-'}"
        )
    return "\n".join(lines)


def _cmd_object(world: WorldState, obj_id: str) -> str:
    obj = world.world_objects.get(obj_id)
    if not obj:
        return f"Object {obj_id} does not exist."
    return str({key: value for key, value in obj.__dict__.items() if not key.startswith("_")})


def _cmd_tasks(world: WorldState) -> str:
    tasks = world.get_active_tasks()
    if not tasks:
        return "No active tasks."
    lines = ["=== Tasks ==="]
    for task in tasks:
        lines.append(
            f"  {task.id}: {task.name} [{task.status}] "
            f"true={task.progress_true:.0f}% reported={task.progress_reported:.0f}% "
            f"budget={task.reserved_budget}/{task.required_budget} "
            f"false_report_risk={task.false_report_risk:.0f}"
        )
        if task.blocked_reason:
            lines.append(f"    blocked: {task.blocked_reason}")
    return "\n".join(lines)


def _cmd_signals(world: WorldState) -> str:
    active = world.get_active_signals()
    if not active:
        return "No active signals."
    lines = ["=== Signals ==="]
    for signal in active:
        lines.append(
            f"  {signal.id}: [{signal.signal_type}] '{signal.content_summary[:50]}' "
            f"holders={signal.current_holder_ids} secrecy={signal.secrecy_level:.0f} "
            f"intensity={signal.intensity:.0f} status={signal.promise_status}"
        )
    return "\n".join(lines)


def _cmd_knowledge(world: WorldState) -> str:
    if not world.player_knowledge:
        return "No player knowledge entries."
    lines = ["=== Knowledge ==="]
    for knowledge in world.player_knowledge.values():
        lines.append(f"  [{knowledge.status}] {knowledge.topic}: {knowledge.summary}")
    return "\n".join(lines)


def _cmd_tick(world: WorldState) -> str:
    summary = run_tick(world)
    return (
        f"=== Tick {summary['tick']} / Day {summary['day']} ({summary['time_of_day']}) ===\n"
        f"new_signals={summary['new_signals']} new_clues={summary['new_clues']} memories={summary['memories_deposited']}\n"
        f"active_tasks={summary['active_tasks']} active_disturbances={summary['active_disturbances']} active_signals={summary['active_signals']}"
    )


def _cmd_wait(world: WorldState, n_str: str) -> str:
    try:
        count = int(n_str)
    except ValueError:
        return "wait requires an integer tick count."
    count = min(count, 20)
    for _ in range(count):
        run_tick(world)
    return f"Advanced {count} ticks. Now at Tick {world.clock.current_tick} / Day {world.clock.current_day} ({world.clock.time_of_day})."


def _cmd_assign_task(world: WorldState, agent: str, task_type: str, budget: int, materials: int, labor: int) -> str:
    action = {
        "type": "assign_task",
        "title": task_type,
        "task_type": task_type,
        "assignee_id": agent,
        "budget": budget,
        "materials": materials,
        "labor": labor,
    }
    run_tick(world, player_actions=[action])
    latest_task = [obj for obj in world.world_objects.values() if hasattr(obj, "task_type")][-1]
    return f"Created task {latest_task.id} for {agent}: {task_type}."


def _cmd_approve_task(world: WorldState, task_id: str, budget: int, materials: int, labor: int) -> str:
    run_tick(world, player_actions=[{"type": "approve_task", "task_id": task_id, "budget": budget, "materials": materials, "labor": labor}])
    return f"Approved resources for {task_id}."


def _cmd_force_task(world: WorldState, task_id: str) -> str:
    run_tick(world, player_actions=[{"type": "force_task", "task_id": task_id}])
    return f"Forced task {task_id}."


def _cmd_appoint(world: WorldState, node_id: str, pos_id: str) -> str:
    if not world.get_node(node_id) and not world.get_background_resident(node_id):
        return f"Node {node_id} does not exist."
    if not world.get_position(pos_id):
        return f"Position {pos_id} does not exist; appointment failed."
    run_tick(world, player_actions=[{"type": "appoint", "node_id": node_id, "position_id": pos_id}])
    return f"Appointed {node_id} to {pos_id}."


def _cmd_appoint_deputy(world: WorldState, node_id: str, pos_id: str) -> str:
    if not world.get_node(node_id):
        return f"Node {node_id} does not exist."
    if not world.get_position(pos_id):
        return f"Position {pos_id} does not exist; deputy appointment failed."
    run_tick(world, player_actions=[{"type": "appoint_deputy", "node_id": node_id, "position_id": pos_id}])
    return f"Appointed {node_id} as deputy of {pos_id}."


def _cmd_promise(world: WorldState, target: str, topic: str, deadline: int) -> str:
    run_tick(
        world,
        player_actions=[{
            "type": "promise",
            "targets": [target],
            "content": f"Promise: {topic} (deadline tick +{deadline})",
            "deadline_ticks": deadline,
            "promise_topic": topic,
        }],
    )
    return f"Promised {topic} to {target}."


def _cmd_public_rebuke(world: WorldState, target: str) -> str:
    run_tick(world, player_actions=[{"type": "public_rebuke", "target_id": target}])
    return f"Publicly rebuked {target}."


def _cmd_private_warning(world: WorldState, target: str) -> str:
    run_tick(world, player_actions=[{"type": "private_warning", "target_id": target}])
    return f"Privately warned {target}."


def _cmd_audit(world: WorldState, target: str) -> str:
    clues = run_audit(world, target)
    if not clues:
        return f"Audit on {target} found no new clues."
    lines = [f"=== Audit on {target} ==="]
    for clue in clues:
        lines.append(f"  [{clue.source_channel}] confidence={clue.confidence:.0f}%: {clue.content}")
    return "\n".join(lines)


def _cmd_plant_informant(world: WorldState, target: str) -> str:
    _, message = plant_informant(world, target)
    return message
