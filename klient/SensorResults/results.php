<?php

class CPU{
    public $system, $user;
    public $timestamp, $type;
    
    public function __construct($iSystem, $iUser) {
        $this->system = $iSystem;
        $this->user = $iUser;
        $this->timestamp = date("r");
        $this->type = 'CPU';
    }
    
    public function getResult()
    {
        $result = "system=".$this->system.";user=".$this->user;
        return $result;
    }
}

class RAM{
    public $free, $used, $total;
    public $timestamp, $type;
    
    public function __construct($iFree, $iUsed, $iTotal) {
        $this->free = $iFree;
        $this->total = $iTotal;
        $this->used = $iUsed;
        $this->timestamp = date("r");
        $this->type = 'RAM';
    }
    
    public function getResult()
    {
        $result = "free=".$this->free.";total=".$this->total.";used=".$this->used;
        return $result;
    }
}

class HDD{
    public $free, $used, $total, $name;
    public $timestamp, $type;
    
    public function __construct($iFree, $iUsed, $iTotal, $iName) {
        $this->free = $iFree;
        $this->total = $iTotal;
        $this->used = $iUsed;
        $this->name = $iName;
        $this->timestamp = date("r");
        $this->type = 'HDD';
    }
    
    public function getResult()
    {
        $result = "free=".$this->free.";total=".$this->total.";used=".$this->used;
        return $result;
    }
}

?>