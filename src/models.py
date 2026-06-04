"""Core data models for Community AI Sandbox v2."""

from __future__ import annotations

import uuid
from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Optional


def _new_id(prefix: str = "") -> str:
    uid = uuid.uuid4().hex[:8]
    return f"{prefix}{uid}" if prefix else uid


def clamp(value: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, float(value)))


def clamp_bipolar(value: float, lo: float = -100.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, float(value)))


class NodeType(StrEnum):
    CHIEF = "chief"
    LEADER = "leader"
    DEPUTY = "deputy"
    PROPERTY = "property"
    SECURITY = "security"
    TREASURER = "treasurer"
    RESIDENT_GROUP = "resident_group"
    RESIDENT = "resident"
    EMERGENT_ACTOR = "emergent_actor"
    FACTION = "faction"
    EXTERNAL = "external"


class ObjectType(StrEnum):
    BUILDING = "building"
    FACILITY = "facility"
    RESOURCE_POOL = "resource_pool"
    TASK = "task"
    POSITION = "position"
    DOCUMENT = "document"
    LOCATION = "location"


class SignalType(StrEnum):
    ORDER = "order"
    APPOINTMENT = "appointment"
    PROMISE = "promise"
    BROKEN_EXPECTATION = "broken_expectation"
    REQUEST = "request"
    WARNING = "warning"
    THREAT = "threat"
    REPORT = "report"
    RUMOR = "rumor"
    CLUE = "clue"
    AUDIT_RESULT = "audit_result"
    COMPLAINT = "complaint"
    PROPAGANDA = "propaganda"
    CONCEALMENT = "concealment"
    CONFESSION = "confession"
    ACCUSATION = "accusation"
    COORDINATION = "coordination"
    CONSPIRACY = "conspiracy"
    LEAK = "leak"
    MEMORY = "memory"
    SILENCE = "silence"
    PUBLIC_GESTURE = "public_gesture"
    DISAPPOINTMENT = "disappointment"
    ACTOR_PROMOTION = "actor_promotion"
    WITNESS_EMERGENCE = "witness_emergence"
    SELF_NOMINATION = "self_nomination"


class TruthStatus(StrEnum):
    TRUE = "true"
    FALSE = "false"
    MIXED = "mixed"
    UNKNOWN = "unknown"


class ClueStatus(StrEnum):
    UNVERIFIED = "unverified"
    SUSPECTED = "suspected"
    CONFIRMED = "confirmed"
    FALSE = "false"


class KnowledgeStatus(StrEnum):
    UNKNOWN = "unknown"
    WEAK_SUSPICION = "weak_suspicion"
    SUSPECTED = "suspected"
    PROBABLE = "probable"
    CONFIRMED = "confirmed"
    MISLED = "misled"


class DisturbanceType(StrEnum):
    COERCION = "coercion"
    FUNDING = "funding"
    APPOINTMENT = "appointment"
    AUDIT = "audit"
    RESOURCE_SHORTAGE = "resource_shortage"
    TASK_DELAY = "task_delay"
    PUBLIC_SUPPORT = "public_support"
    BROKEN_PROMISE = "broken_promise"
    PUBLIC_REBUKE = "public_rebuke"
    PRIVATE_WARNING = "private_warning"
    RUMOR_BURST = "rumor_burst"
    ACTOR_PROMOTION = "actor_promotion"


class ChannelType(StrEnum):
    AUDIT = "audit"
    INFORMANT = "informant"
    PATROL = "patrol"
    MEETING = "meeting"
    ROUTINE_REPORT = "routine_report"
    ACCIDENT_EXPOSURE = "accident_exposure"
    BUDGET_REVIEW = "budget_review"


@dataclass
class WorldClock:
    current_tick: int = 0
    current_day: int = 1
    time_of_day: str = "morning"
    ticks_per_day: int = 2
    paused: bool = False
    speed: float = 1.0

    def advance(self) -> None:
        self.current_tick += 1
        self.time_of_day = "night" if self.current_tick % self.ticks_per_day == 0 else "morning"
        if self.current_tick % self.ticks_per_day == 0:
            self.current_day += 1

    @property
    def is_new_day(self) -> bool:
        return self.current_tick % self.ticks_per_day == 0

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "WorldClock":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class SocialNode:
    id: str
    name: str
    node_type: str = NodeType.RESIDENT.value

    active: bool = True
    roles: list[str] = field(default_factory=list)
    group_tags: list[str] = field(default_factory=list)

    stress: float = 20.0
    fear: float = 10.0
    anger: float = 10.0
    hope: float = 50.0
    morale: float = 50.0
    resentment: float = 0.0

    compliance_tendency: float = 50.0
    concealment_tendency: float = 20.0
    cooperation_tendency: float = 50.0
    sabotage_tendency: float = 0.0
    report_honesty: float = 60.0

    competence: float = 50.0
    honesty_trait: float = 50.0
    greed_trait: float = 20.0
    risk_tolerance: float = 40.0
    moral_constraint: float = 50.0

    health: float = 80.0
    available: bool = True

    authority_centrality: float = 0.0
    information_centrality: float = 0.0
    resource_centrality: float = 0.0
    access_to_chief: float = 0.0
    issue_relevance: float = 0.0
    overall_core_score: float = 0.0
    signal_exposure_score: float = 0.0
    resource_control_score: float = 0.0
    task_relevance_score: float = 0.0
    contact_frequency_score: float = 0.0
    clue_relevance_score: float = 0.0
    group_attention_score: float = 0.0
    sustained_core_score: float = 0.0

    memory_ids: list[str] = field(default_factory=list)
    known_signal_ids: list[str] = field(default_factory=list)
    current_task_ids: list[str] = field(default_factory=list)

    def clamp_all(self) -> None:
        for attr in (
            "stress", "fear", "anger", "hope", "morale", "resentment",
            "compliance_tendency", "concealment_tendency", "cooperation_tendency",
            "sabotage_tendency", "report_honesty", "competence", "honesty_trait",
            "greed_trait", "risk_tolerance", "moral_constraint", "health",
            "authority_centrality", "information_centrality", "resource_centrality",
            "access_to_chief", "issue_relevance", "overall_core_score",
            "signal_exposure_score", "resource_control_score", "task_relevance_score",
            "contact_frequency_score", "clue_relevance_score", "group_attention_score",
            "sustained_core_score",
        ):
            setattr(self, attr, clamp(getattr(self, attr)))

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "SocialNode":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class SocialEdge:
    id: str
    source_id: str
    target_id: str

    trust: float = 50.0
    authority: float = 0.0
    obedience: float = 50.0
    fear: float = 0.0
    hostility: float = 0.0
    empathy: float = 0.0
    dependency: float = 0.0
    interest_alignment: float = 0.0
    secrecy: float = 0.0
    competition: float = 0.0
    reputation_weight: float = 0.0

    information_flow: float = 20.0
    bandwidth: float = 20.0
    latency: int = 1
    distortion: float = 0.1
    visibility: float = 0.5
    volatility: float = 0.2

    tags: list[str] = field(default_factory=list)
    last_updated_tick: int = 0

    def clamp_all(self) -> None:
        for attr in (
            "trust", "authority", "obedience", "fear", "hostility", "empathy",
            "dependency", "interest_alignment", "secrecy", "competition",
            "reputation_weight", "information_flow", "bandwidth",
        ):
            setattr(self, attr, clamp(getattr(self, attr)))
        for attr in ("distortion", "visibility", "volatility"):
            setattr(self, attr, clamp(getattr(self, attr), 0, 1.0))

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "SocialEdge":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class WorldObject:
    id: str
    name: str
    object_type: str = ObjectType.BUILDING.value

    status: str = "active"
    location: Optional[str] = None
    owner_node_id: Optional[str] = None
    manager_node_id: Optional[str] = None

    visibility: float = 0.5
    condition: float = 100.0
    importance: float = 50.0

    tags: list[str] = field(default_factory=list)
    linked_signal_ids: list[str] = field(default_factory=list)
    linked_trace_ids: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "WorldObject":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class TaskObject(WorldObject):
    task_type: str = "generic"
    assignee_node_id: Optional[str] = None
    requester_node_id: Optional[str] = None

    progress_true: float = 0.0
    progress_reported: float = 0.0

    required_budget: int = 0
    reserved_budget: int = 0
    required_materials: int = 0
    reserved_materials: int = 0
    required_labor: int = 0
    reserved_labor: int = 0

    difficulty: float = 50.0
    risk: float = 20.0
    pressure_level: float = 0.0
    deadline_tick: Optional[int] = None

    blocked_reason: Optional[str] = None
    failure_risk: float = 0.0
    false_report_risk: float = 0.0
    misuse_risk: float = 0.0

    tick_created: int = 0
    logs: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.object_type = ObjectType.TASK.value

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "TaskObject":
        d.pop("object_type", None)
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class ResourcePool(WorldObject):
    resource_type: str = "budget"
    amount_available: float = 0.0
    amount_reserved: float = 0.0
    amount_spent: float = 0.0
    amount_misused: float = 0.0

    def __post_init__(self) -> None:
        self.object_type = ObjectType.RESOURCE_POOL.value

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "ResourcePool":
        d.pop("object_type", None)
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class PositionObject(WorldObject):
    title: str = ""
    holder_node_id: Optional[str] = None
    deputy_node_ids: list[str] = field(default_factory=list)

    permission_tags: list[str] = field(default_factory=list)
    scope: str = ""
    nominal_authority: float = 50.0
    actual_authority: float = 50.0
    accountability: float = 50.0
    budget_limit: int = 0

    def __post_init__(self) -> None:
        self.object_type = ObjectType.POSITION.value

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "PositionObject":
        d.pop("object_type", None)
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class BackgroundResident:
    id: str
    name: str
    home_group_id: str
    home_building_id: Optional[str] = None
    status: str = "background"

    age_group: str = "adult"
    role_tags: list[str] = field(default_factory=list)
    location_tags: list[str] = field(default_factory=list)

    ambition: float = 50.0
    initiative: float = 50.0
    opportunism: float = 50.0
    social_skill: float = 50.0
    risk_tolerance: float = 50.0
    information_sensitivity: float = 50.0
    leadership_potential: float = 50.0
    resourcefulness: float = 50.0
    moral_flexibility: float = 50.0
    visibility_seeking: float = 50.0

    signal_exposure_score: float = 0.0
    clue_relevance_score: float = 0.0
    resource_position_score: float = 0.0
    group_attention_score: float = 0.0
    event_relevance_score: float = 0.0
    contact_with_core_score: float = 0.0

    promotion_pressure: float = 0.0
    promotion_reason: Optional[str] = None
    candidate_since_tick: Optional[int] = None
    promoted_node_id: Optional[str] = None

    known_signal_ids: list[str] = field(default_factory=list)
    linked_trace_ids: list[str] = field(default_factory=list)
    linked_clue_ids: list[str] = field(default_factory=list)
    memory_seed_ids: list[str] = field(default_factory=list)

    created_tick: int = 0
    last_updated_tick: int = 0

    def clamp_all(self) -> None:
        for attr in (
            "ambition", "initiative", "opportunism", "social_skill", "risk_tolerance",
            "information_sensitivity", "leadership_potential", "resourcefulness",
            "moral_flexibility", "visibility_seeking", "signal_exposure_score",
            "clue_relevance_score", "resource_position_score", "group_attention_score",
            "event_relevance_score", "contact_with_core_score", "promotion_pressure",
        ):
            setattr(self, attr, clamp(getattr(self, attr)))

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "BackgroundResident":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class Signal:
    id: str
    day_created: int = 0
    tick_created: int = 0

    signal_type: str = SignalType.REPORT.value
    source_node_id: Optional[str] = None
    intended_receiver_ids: list[str] = field(default_factory=list)
    current_holder_ids: list[str] = field(default_factory=list)

    content_summary: str = ""
    truth_status: str = TruthStatus.UNKNOWN.value
    confidence: float = 50.0

    intensity: float = 50.0
    secrecy_level: float = 0.0
    spread_rate: float = 50.0
    decay_rate: float = 10.0
    distortion_rate: float = 10.0
    memory_strength: float = 50.0

    blocked_by_node_ids: list[str] = field(default_factory=list)
    linked_world_object_ids: list[str] = field(default_factory=list)
    linked_trace_ids: list[str] = field(default_factory=list)
    pending_holder_arrivals: dict[str, int] = field(default_factory=dict)
    deadline_tick: Optional[int] = None
    promise_topic: Optional[str] = None
    related_signal_id: Optional[str] = None
    fulfilled: bool = False
    promise_status: str = "pending"
    fulfillment_conditions: list[str] = field(default_factory=list)
    linked_fulfillment_targets: list[str] = field(default_factory=list)
    fulfillment_progress: float = 0.0

    tags: list[str] = field(default_factory=list)
    active: bool = True

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Signal":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class Trace:
    id: str
    tick_created: int = 0
    trace_type: str = ""
    source_event_id: Optional[str] = None
    linked_world_object_id: Optional[str] = None
    location: Optional[str] = None

    strength: float = 50.0
    decay_rate: float = 5.0
    detectable_by: list[str] = field(default_factory=list)
    discovered: bool = False
    misleading_possibility: float = 15.0

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Trace":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class Clue:
    id: str
    tick_created: int = 0
    source_channel: str = ""
    holder_node_id: str = "CHIEF"
    related_trace_id: Optional[str] = None
    related_signal_id: Optional[str] = None

    content: str = ""
    confidence: float = 30.0
    source_reliability: float = 50.0
    misleading_risk: float = 20.0
    status: str = ClueStatus.UNVERIFIED.value
    possible_explanations: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Clue":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class Memory:
    id: str
    holder_node_id: str = ""
    source_signal_id: str = ""
    topic: str = ""
    sentiment: float = 0.0
    strength: float = 50.0
    decay_rate: float = 2.0
    created_tick: int = 0
    last_reinforced_tick: int = 0

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Memory":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class Disturbance:
    id: str
    tick_created: int = 0
    disturbance_type: str = DisturbanceType.COERCION.value
    source_node_id: Optional[str] = None

    entry_social_node_ids: list[str] = field(default_factory=list)
    entry_world_object_ids: list[str] = field(default_factory=list)
    entry_signal_ids: list[str] = field(default_factory=list)

    intensity: float = 50.0
    duration_ticks: int = 3
    age_ticks: int = 0
    decay_rate: float = 20.0

    propagation_channels: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    active: bool = True

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Disturbance":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class PlayerKnowledge:
    id: str
    topic: str = ""
    confidence: float = 20.0
    summary: str = ""
    source_ids: list[str] = field(default_factory=list)
    status: str = KnowledgeStatus.UNKNOWN.value
    last_updated_tick: int = 0

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "PlayerKnowledge":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class WorldState:
    clock: WorldClock = field(default_factory=WorldClock)
    social_nodes: dict[str, SocialNode] = field(default_factory=dict)
    social_edges: dict[str, SocialEdge] = field(default_factory=dict)
    background_residents: dict[str, BackgroundResident] = field(default_factory=dict)
    world_objects: dict[str, WorldObject] = field(default_factory=dict)
    signals: dict[str, Signal] = field(default_factory=dict)
    traces: dict[str, Trace] = field(default_factory=dict)
    clues: dict[str, Clue] = field(default_factory=dict)
    memories: dict[str, Memory] = field(default_factory=dict)
    disturbances: dict[str, Disturbance] = field(default_factory=dict)
    player_knowledge: dict[str, PlayerKnowledge] = field(default_factory=dict)
    history_log: list[str] = field(default_factory=list)
    debug_log: list[str] = field(default_factory=list)
    _id_counter: int = 0

    def next_id(self, prefix: str = "") -> str:
        self._id_counter += 1
        return f"{prefix}{self._id_counter}"

    def get_node(self, node_id: str) -> Optional[SocialNode]:
        return self.social_nodes.get(node_id)

    def get_edge(self, source_id: str, target_id: str) -> Optional[SocialEdge]:
        return self.social_edges.get(f"{source_id}->{target_id}")

    def set_edge(self, edge: SocialEdge) -> None:
        self.social_edges[f"{edge.source_id}->{edge.target_id}"] = edge

    def get_background_resident(self, resident_id: str) -> Optional[BackgroundResident]:
        return self.background_residents.get(resident_id)

    def get_object(self, obj_id: str) -> Optional[WorldObject]:
        return self.world_objects.get(obj_id)

    def get_task(self, task_id: str) -> Optional[TaskObject]:
        obj = self.world_objects.get(task_id)
        return obj if isinstance(obj, TaskObject) else None

    def get_resource(self, res_id: str) -> Optional[ResourcePool]:
        obj = self.world_objects.get(res_id)
        return obj if isinstance(obj, ResourcePool) else None

    def get_position(self, pos_id: str) -> Optional[PositionObject]:
        obj = self.world_objects.get(pos_id)
        return obj if isinstance(obj, PositionObject) else None

    def get_active_tasks(self) -> list[TaskObject]:
        return [
            obj for obj in self.world_objects.values()
            if isinstance(obj, TaskObject) and obj.status not in ("completed", "failed", "abandoned", "cancelled")
        ]

    def get_active_disturbances(self) -> list[Disturbance]:
        return [disturbance for disturbance in self.disturbances.values() if disturbance.active]

    def get_active_signals(self) -> list[Signal]:
        return [signal for signal in self.signals.values() if signal.active]

    def add_history(self, msg: str) -> None:
        self.history_log.append(f"Tick {self.clock.current_tick} Day {self.clock.current_day}: {msg}")

    def add_debug(self, msg: str) -> None:
        self.debug_log.append(f"Tick {self.clock.current_tick}: {msg}")

    def to_dict(self) -> dict:
        return {
            "clock": self.clock.to_dict(),
            "social_nodes": {k: v.to_dict() for k, v in self.social_nodes.items()},
            "social_edges": {k: v.to_dict() for k, v in self.social_edges.items()},
            "background_residents": {k: v.to_dict() for k, v in self.background_residents.items()},
            "world_objects": {k: v.to_dict() for k, v in self.world_objects.items()},
            "signals": {k: v.to_dict() for k, v in self.signals.items()},
            "traces": {k: v.to_dict() for k, v in self.traces.items()},
            "clues": {k: v.to_dict() for k, v in self.clues.items()},
            "memories": {k: v.to_dict() for k, v in self.memories.items()},
            "disturbances": {k: v.to_dict() for k, v in self.disturbances.items()},
            "player_knowledge": {k: v.to_dict() for k, v in self.player_knowledge.items()},
            "history_log": self.history_log,
            "debug_log": self.debug_log,
            "_id_counter": self._id_counter,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "WorldState":
        world = cls(
            clock=WorldClock.from_dict(d.get("clock", {})),
            history_log=d.get("history_log", []),
            debug_log=d.get("debug_log", []),
        )
        world._id_counter = d.get("_id_counter", 0)

        for key, value in d.get("social_nodes", {}).items():
            world.social_nodes[key] = SocialNode.from_dict(value)
        for key, value in d.get("social_edges", {}).items():
            world.social_edges[key] = SocialEdge.from_dict(value)
        for key, value in d.get("background_residents", {}).items():
            world.background_residents[key] = BackgroundResident.from_dict(value)
        for key, value in d.get("world_objects", {}).items():
            obj_type = value.get("object_type", "")
            if obj_type == ObjectType.TASK.value:
                world.world_objects[key] = TaskObject.from_dict(value)
            elif obj_type == ObjectType.RESOURCE_POOL.value:
                world.world_objects[key] = ResourcePool.from_dict(value)
            elif obj_type == ObjectType.POSITION.value:
                world.world_objects[key] = PositionObject.from_dict(value)
            else:
                world.world_objects[key] = WorldObject.from_dict(value)
        for key, value in d.get("signals", {}).items():
            world.signals[key] = Signal.from_dict(value)
        for key, value in d.get("traces", {}).items():
            world.traces[key] = Trace.from_dict(value)
        for key, value in d.get("clues", {}).items():
            world.clues[key] = Clue.from_dict(value)
        for key, value in d.get("memories", {}).items():
            world.memories[key] = Memory.from_dict(value)
        for key, value in d.get("disturbances", {}).items():
            world.disturbances[key] = Disturbance.from_dict(value)
        for key, value in d.get("player_knowledge", {}).items():
            world.player_knowledge[key] = PlayerKnowledge.from_dict(value)
        return world
