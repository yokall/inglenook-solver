use Test2::V0;

use Inglenook::State;

subtest 'new' => sub {
    my $state = Inglenook::State->new();

    is( $state->get_track(0), [], 'should not have any wagons on the headshunt' );
    is( $state->get_track(1),
        array {
            item match qr/[0-9]/;
            item match qr/[0-9]/;
            item match qr/[0-9]/;
            item match qr/[0-9]/;
            item match qr/[0-9]/;
        },
        'should have 5 wagons on the mainline'
    );
    is( $state->get_track(2),
        array {
            item match qr/[0-9]/;
            item match qr/[0-9]/;
            item match qr/[0-9]/;
        },
        ,
        'should have 3 wagons on siding 1'
    );
    is( $state->get_track(3), [], 'should not have any wagons on siding 2' );
};

done_testing();
