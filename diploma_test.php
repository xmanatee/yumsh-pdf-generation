<?php

require_once("diploma.module");

function testGenerateDiploma() {
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

    $filename = generate_diploma($student_details, false);
    print("Returned filename : " . $filename . "\n");
}

testGenerateDiploma();

?>
