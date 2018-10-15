<?php

require_once("fpdf/src/pdf_parser.php");

require_once("fpdf/src/tfpdf.php");
require_once("fpdf/src/fpdf_tpl.php");
require_once("fpdf/src/fpdi.php");

class INVITE_PDF extends fpdi\FPDI {
    protected $_tplIdx;

    public $BIG_FONT_SIZE = 40;
    public $SMALL_FONT_SIZE = 12;

    public function Header() {
        if (is_null($this->_tplIdx)) {
            $this->setSourceFile('assets/invite_template.pdf');
            $this->_tplIdx = $this->importPage(1);
        }

        $size = $this->useTemplate($this->_tplIdx, 0, 0, 0, 0, true);
    }
}
