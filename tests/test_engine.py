from engine import Engine, Event

import pytest

import itertools

@pytest.fixture()
def engine():
    return Engine()


def assert_timestamps_equal(vals, engine):
	for actual_event, expected_timestamp in zip(engine, vals):
		assert actual_event.timestamp == expected_timestamp


def test_empty_engine(engine):
	assert engine.FEL == None


def test_engine_with_one_event(engine):
	engine.schedule(Event(0))
	assert_timestamps_equal([0], engine)
	assert engine.remove().timestamp == 0


@pytest.mark.parametrize("t1, t2", [
    (0, 1),
    (1, 0),
])
def test_engine_with_two_events(engine, t1, t2):
	engine.schedule(Event(t1))
	engine.schedule(Event(t2))
	assert_timestamps_equal([0, 1], engine)
	assert engine.remove().timestamp == 0
	assert engine.remove().timestamp == 1


@pytest.mark.parametrize("t1, t2, t3", list(itertools.permutations([1,2,3])))
def test_engine_with_three_events(engine, t1, t2, t3):
	engine.schedule(Event(t1))
	engine.schedule(Event(t2))
	engine.schedule(Event(t3))
	assert_timestamps_equal([1, 2, 3], engine)
	assert engine.remove().timestamp == 1
	assert_timestamps_equal([2, 3], engine)
	assert engine.remove().timestamp == 2
	assert_timestamps_equal([3], engine)
	assert engine.remove().timestamp == 3
