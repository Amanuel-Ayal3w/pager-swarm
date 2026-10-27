"""The CLI builds the same decision the board posts."""

from pager.graph.run import decision_from_answer


def test_yes_no_and_investigate():
    approved = decision_from_answer("y", version=2, typed="rollback api")
    assert approved is not None
    assert approved.decision == "approve"
    assert approved.typed_confirmation == "rollback api"
    assert approved.action_version == 2

    rejected = decision_from_answer("n", version=1, reason="Too wide.")
    assert rejected is not None
    assert rejected.decision == "reject"
    assert rejected.reason == "Too wide."

    more = decision_from_answer("i", version=1)
    assert more is not None
    assert more.decision == "investigate"

    assert decision_from_answer("maybe", version=1) is None
