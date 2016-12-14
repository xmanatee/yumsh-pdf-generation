<?php

require_once('fpdf.php');
require_once('fpdi.php');

// require_once('fpdf/makefont/makefont.php');

function getFilename($string) {
    // $filename = str_replace(' ', '_', $fullname.$school.$year)
    $filename = hash('sha256', $string);
    $filename = substr($filename, -8);
    return $filename;
}

function writeInCenter($pdf, $style, $size, $height, $text) {
    $pdf->SetFont('x', $style, $size);
    $pdf->SetX($pdf->lMargin);
    $formattedText = iconv('utf-8','cp1251',$text);
    $pdf->Cell(0, $height, $formattedText, 0, 0, 'C');
    return $pdf;
}

function generateDiploma($fullname, $paral, $school, $year) {
    echo $fullname."\r\n";
    echo ">>".mb_detect_encoding($fullname)."\r\n";
    $filename = getFilename($fullname.$school.$year).'.pdf';
    /*
    if (file_exists('diplomas/'.$filename)) {
        return $filename;
    }
    */
    // $pdf->header("content-type:text/html; charset=utf-8");
    $pdf = new FPDI();
    $pdf->setSourceFile("assets/template_1.pdf");
    $tplIdx = $pdf->importPage(1, '/MediaBox');
    $pdf->AddFont('x', '', 'georgia.php');
    $pdf->addPage();
    $pdf->useTemplate($tplIdx, 0, 0, 0, 0, true);

    $pdf->SetTextColor(0, 0, 0);

    writeInCenter($pdf, '', 40, 150, 'Диплом');
    writeInCenter($pdf, '', 40, 180, 'I степени');
    writeInCenter($pdf, '', 20, 200, 'награждается');
    writeInCenter($pdf, '', 40, 232, $fullname);
    writeInCenter($pdf, '', 20, 252, 'ученик ' . $paral . ' класса');
    writeInCenter($pdf, '', 20, 266, $school);

//    writeInCenter($pdf, '', 20, 295, 'за все хорошее');
//    writeInCenter($pdf, '', 20, 50, $fullname);
//    writeInCenter($pdf, '', 20, 75, $school);
//    writeInCenter($pdf, '', 20, 100, $year);


    $pdf->Output('diplomas/'.$filename);

    return $filename;
}

function testGenerateDiploma() {
    $fullname = "Михаил Немилов";
    $paral = "11";
    $school = "MIPT (SU)";
    $year = "2017";

    $filename = generateDiploma($fullname, $paral, $school, $year);
    echo "SUCCESS\r\n";
}

testGenerateDiploma();

?>
