# tests/test_state.py
#
# Tests for solver/state.py
#
# Covers:
#   - Constants have the right values
#   - make_initial_state returns the correct shape and contents
#   - make_initial_state validates capacity, reserved labels, and uniqueness

import pytest
from inglenook_solver.solver.state import (
    make_initial_state,
    HEADSHUNT, TRACK2, TRACK3, TRACK4,
    CAPACITY, SIDINGS,
)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

class TestConstants:
    def test_track_indices_are_zero_based(self):
        assert HEADSHUNT == 0
        assert TRACK2    == 1
        assert TRACK3    == 2
        assert TRACK4    == 3

    def test_capacity_length_matches_track_count(self):
        assert len(CAPACITY) == 4

    def test_capacity_values(self):
        assert CAPACITY[HEADSHUNT] == 3
        assert CAPACITY[TRACK2]    == 5
        assert CAPACITY[TRACK3]    == 3
        assert CAPACITY[TRACK4]    == 3

    def test_sidings_excludes_headshunt(self):
        assert HEADSHUNT not in SIDINGS

    def test_sidings_contains_all_three_sidings(self):
        assert set(SIDINGS) == {TRACK2, TRACK3, TRACK4}


# ---------------------------------------------------------------------------
# make_initial_state — shape and contents
# ---------------------------------------------------------------------------

class TestMakeInitialState:
    def test_returns_tuple_of_four_tuples(self):
        state = make_initial_state(('A', 'B'), ('C',), ())
        assert isinstance(state, tuple)
        assert len(state) == 4
        assert all(isinstance(t, tuple) for t in state)

    def test_headshunt_starts_empty(self):
        state = make_initial_state(('A', 'B'), ('C',), ())
        assert state[HEADSHUNT] == ()

    def test_siding_contents_are_preserved(self):
        state = make_initial_state(('A', 'B', 'C'), ('D', 'E'), ('F',))
        assert state[TRACK2] == ('A', 'B', 'C')
        assert state[TRACK3] == ('D', 'E')
        assert state[TRACK4] == ('F',)

    def test_empty_sidings_are_valid(self):
        state = make_initial_state((), (), ())
        assert state[TRACK2] == ()
        assert state[TRACK3] == ()
        assert state[TRACK4] == ()

    def test_full_sidings_are_valid(self):
        state = make_initial_state(
            ('A', 'B', 'C', 'D', 'E'),
            ('F', 'G', 'H'),
            ('I', 'J', 'K'),
        )
        assert len(state[TRACK2]) == 5
        assert len(state[TRACK3]) == 3
        assert len(state[TRACK4]) == 3

    def test_state_is_hashable(self):
        state = make_initial_state(('A', 'B'), ('C',), ())
        # Should not raise — needed for the BFS visited set
        assert hash(state) is not None

    def test_state_can_be_used_as_dict_key(self):
        state = make_initial_state(('A',), ('B',), ('C',))
        d = {state: 'visited'}
        assert d[state] == 'visited'

    def test_input_sequences_are_converted_to_tuples(self):
        # Lists are valid inputs and should be stored as tuples
        state = make_initial_state(['A', 'B'], ['C'], [])
        assert isinstance(state[TRACK2], tuple)
        assert isinstance(state[TRACK3], tuple)
        assert isinstance(state[TRACK4], tuple)

    def test_standard_puzzle_setup(self):
        # The canonical 8-wagon Inglenook starting position
        state = make_initial_state(
            ('A', 'B', 'C', 'D', 'E'),
            ('F', 'G', 'H'),
            (),
        )
        assert state[HEADSHUNT] == ()
        assert state[TRACK2]    == ('A', 'B', 'C', 'D', 'E')
        assert state[TRACK3]    == ('F', 'G', 'H')
        assert state[TRACK4]    == ()


# ---------------------------------------------------------------------------
# make_initial_state — validation
# ---------------------------------------------------------------------------

class TestMakeInitialStateValidation:
    def test_track2_over_capacity_raises(self):
        with pytest.raises(ValueError, match="capacity"):
            make_initial_state(('A', 'B', 'C', 'D', 'E', 'F'), (), ())

    def test_track3_over_capacity_raises(self):
        with pytest.raises(ValueError, match="capacity"):
            make_initial_state((), ('A', 'B', 'C', 'D'), ())

    def test_track4_over_capacity_raises(self):
        with pytest.raises(ValueError, match="capacity"):
            make_initial_state((), (), ('A', 'B', 'C', 'D'))

    def test_reserved_label_L_raises(self):
        with pytest.raises(ValueError, match="reserved"):
            make_initial_state(('L', 'A'), (), ())

    def test_duplicate_wagon_across_tracks_raises(self):
        with pytest.raises(ValueError, match="unique"):
            make_initial_state(('A', 'B'), ('A',), ())

    def test_duplicate_wagon_within_track_raises(self):
        with pytest.raises(ValueError, match="unique"):
            make_initial_state(('A', 'A'), (), ())
