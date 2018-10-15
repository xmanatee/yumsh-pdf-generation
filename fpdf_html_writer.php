<?php
/**
 * Created by PhpStorm.
 * User: xmanatee
 * Date: 10/15/18
 * Time: 03:19
 */

class FpdfHmtlWriter
{
    const LINE_SPACE = 6;

    var $B;
    var $I;
    var $U;
    var $HREF;

    function FpdfHmtlWriter()
    {
        //Initialization
        $this->B=0;
        $this->I=0;
        $this->U=0;
        $this->HREF='';
    }

    function WriteHTML($pdf, $html)
    {
        //HTML parser
        $html=str_replace("\n",' ',$html);
        $a=preg_split('/<(.*)>/U',$html,-1,PREG_SPLIT_DELIM_CAPTURE);
        foreach($a as $i=>$e)
        {
            if($i%2==0)
            {
                //Text
                if($this->HREF)
                    $this->PutLink($pdf, $this->HREF,$e);
                else
                    $pdf->Write(FpdfHmtlWriter::LINE_SPACE,$e);
//                    $pdf->Multicell(0, 3, $e, 0);
            }
            else
            {
                //Tag
                if($e{0}=='/')
                    $this->CloseTag($pdf, strtoupper(substr($e,1)));
                else
                {
                    //Extract properties
                    $a2=preg_split('/ /',$e);
                    $tag=strtoupper(array_shift($a2));
                    $prop=array();
                    foreach($a2 as $v)
                        if(preg_match('/^([^=]*)=["\']?([^"\']*)["\']?$/',$v,$a3))
                            $prop[strtoupper($a3[1])]=$a3[2];
                    $this->OpenTag($pdf, $tag,$prop);
                }
            }
        }
    }

    function OpenTag($pdf, $tag,$prop)
    {
        //Opening tag
        if($tag=='B' or $tag=='I' or $tag=='U')
            $this->SetStyle($pdf, $tag,true);
        if($tag=='A')
            $this->HREF=$prop['HREF'];
        if($tag=='BR')
            $pdf->Ln(FpdfHmtlWriter::LINE_SPACE);
    }

    function CloseTag($pdf, $tag)
    {
        //Closing tag
        if($tag=='B' or $tag=='I' or $tag=='U')
            $this->SetStyle($pdf, $tag,false);
        if($tag=='A')
            $this->HREF='';
    }

    function SetStyle($pdf, $tag,$enable)
    {
        //Modify style and select corresponding font
        $this->$tag+=($enable ? 1 : -1);
        $style='';
        foreach(array('B','I','U') as $s)
            if($this->$s>0)
                $style.=$s;
        $pdf->SetFont('DejaVuSerifCondensed',$style);
    }

    function PutLink($pdf, $URL, $txt)
    {
        //Put a hyperlink
        $pdf->SetTextColor(0,0,255);
        $this->SetStyle($pdf, 'U',true);
        $pdf->Write(FpdfHmtlWriter::LINE_SPACE,$txt,$URL);
        $this->SetStyle($pdf, 'U',false);
        $pdf->SetTextColor(0);
    }
}

?>