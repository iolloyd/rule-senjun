<?php
namespace Service;
require_once './vendor/autoload.php';

$redis = new \Predis\Client();

require_once __DIR__ . '/conn.php';

$q = function ($stmt) use ($pdo) {
    $result = [];
    $stmt = $pdo->query($stmt);
    while($result[] = $stmt->fetch());
    return $result;
};

$items = $q('select id, description from bloomingdales_items');

$templates = new \League\Plates\Engine('templates');
echo $templates->render('items', [
    'name' => 'Some name',
    'items' => $items 
]);
