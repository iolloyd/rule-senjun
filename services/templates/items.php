<?php $this->layout('layout', ['title' => 'The items']) ?>

<h1>Items</h1>

<p>
<? foreach($this->e($items) as $item):?>
<?=$this->e($item['id'])?>
<? endforeach; ?>

