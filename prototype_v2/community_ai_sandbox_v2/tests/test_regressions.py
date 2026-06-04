import random
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent.parent
PROTO = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(PROTO))

from src.cognition_engine import update_player_knowledge
from src.influence_engine import create_disturbance, propagate_all_disturbances
from src.models import DisturbanceType
from src.signal_engine import create_signal
from src.world import create_default_world


def test_disturbance_effects_use_own_source_attribution():
    random.seed(1001)
    world = create_default_world()

    trust_to_chief_before = world.social_edges["A2->CHIEF"].trust
    trust_to_a1_before = world.social_edges["A2->A1"].trust

    create_disturbance(
        world,
        DisturbanceType.FUNDING.value,
        source_node_id="CHIEF",
        entry_nodes=["A2"],
        intensity=60.0,
        channels=["authority"],
    )
    create_disturbance(
        world,
        DisturbanceType.COERCION.value,
        source_node_id="A1",
        entry_nodes=["A2"],
        intensity=60.0,
        channels=["authority"],
    )

    propagate_all_disturbances(world)

    assert world.social_edges["A2->CHIEF"].trust > trust_to_chief_before
    assert world.social_edges["A2->A1"].trust < trust_to_a1_before


def test_intended_receiver_does_not_create_player_knowledge_before_delivery():
    random.seed(1002)
    world = create_default_world()

    signal = create_signal(
        world,
        "report",
        source_node_id="A2",
        intended_receivers=["CHIEF"],
        content="尚未送达区长的汇报",
        truth_status="true",
        intensity=50.0,
    )

    update_player_knowledge(world)
    assert not world.player_knowledge
    assert "CHIEF" not in signal.current_holder_ids

    signal.current_holder_ids.append("CHIEF")
    update_player_knowledge(world)

    assert any("尚未送达区长的汇报" in pk.summary for pk in world.player_knowledge.values())
