package Inglenook::State;

use strict;
use warnings;

sub new {
    my ($class) = @_;

    my $self = { tracks => [ [], [ 1, 2, 3, 4, 5 ], [ 6, 7, 8 ], [] ], };

    bless $self, $class;
    return $self;
}

sub get_track {
    my ( $self, $track_index ) = @_;

    return $self->{tracks}->[$track_index];
}

1;
