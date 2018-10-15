<?php

require_once("invite.module");

function test_generate_invite() {
    $student_details = array(
        'id_pupil' => 124,
        'name' => 'Михаил',
        'family' => 'Немилов',
        'paral' => 11,
        'year' => 2016,
        'school_name' => 'Президентского физико-математического лицея № 239',
        'district' => 'Кировского района',
        'sex' => 'м',
        'type' => 'Д1',
        'tour' => 'отборочном (заочном)'
    );

    $filename = generate_invite($student_details, false);
    print("Returned filename : " . $filename . "\n");
}

function test_generate_invite_2() {
    $student_details = array(
        'name' => 'Иван',
        'family' => 'Иванов',
        'paral' => 7,
        'school_name' => '39 школы',
    );

    $filename = generate_invite($student_details, false);
    print("Returned filename : " . $filename . "\n");
}


test_generate_invite();

test_generate_invite_2();
