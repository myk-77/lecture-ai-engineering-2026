import json

from pydantic_ai import DeferredToolRequests, DeferredToolResults
from pydantic_ai.models.test import TestModel

from app import tools
from app.agent import agent, collect_approvals


def test_approval_waits_then_saves_the_proposed_content(tmp_path, monkeypatch):
    directory = tmp_path / "learning_log"
    monkeypatch.setattr(tools, "LEARNING_LOG_DIR", directory)
    model = TestModel(call_tools=["save_learning_log"])
    pending = agent.run_sync("学習記録を保存してください", model=model)
    assert isinstance(pending.output, DeferredToolRequests)
    assert not directory.exists()
    call = pending.output.approvals[0]
    expected = call.args_as_dict()
    result = agent.run_sync(
        message_history=pending.all_messages(),
        deferred_tool_results=DeferredToolResults(approvals={call.tool_call_id: True}),
        model=model,
        usage=pending.usage,
    )
    assert not isinstance(result.output, DeferredToolRequests)
    files = list(directory.glob("*.json"))
    assert len(files) == 1
    record = json.loads(files[0].read_text())
    assert record["topic"] == expected["topic"]
    assert record["note"] == expected["note"]
    assert record["created_at"]


def test_denial_does_not_create_a_file(tmp_path, monkeypatch):
    directory = tmp_path / "learning_log"
    monkeypatch.setattr(tools, "LEARNING_LOG_DIR", directory)
    model = TestModel(call_tools=["save_learning_log"])
    pending = agent.run_sync("学習記録を保存してください", model=model)
    assert isinstance(pending.output, DeferredToolRequests)
    decisions = {call.tool_call_id: False for call in pending.output.approvals}
    result = agent.run_sync(
        message_history=pending.all_messages(),
        deferred_tool_results=DeferredToolResults(approvals=decisions),
        model=model,
        usage=pending.usage,
    )
    assert not isinstance(result.output, DeferredToolRequests)
    assert not directory.exists()


def test_missing_cli_input_is_a_denial(tmp_path, monkeypatch):
    directory = tmp_path / "learning_log"
    monkeypatch.setattr(tools, "LEARNING_LOG_DIR", directory)
    pending = agent.run_sync(
        "学習記録を保存してください", model=TestModel(call_tools=["save_learning_log"])
    )
    def no_input(prompt):
        raise EOFError
    monkeypatch.setattr("builtins.input", no_input)
    decisions = collect_approvals(pending.output)
    assert decisions.approvals
    assert all(value is False for value in decisions.approvals.values())
    assert not directory.exists()
