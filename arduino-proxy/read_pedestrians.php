<?php
require_once('firebaseLib.php');
// --- This is your Firebase URL
$url = 'https://traffic-control-simulator-default-rtdb.europe-west1.firebasedatabase.app/';
// --- Use your token from Firebase here
$token = '6hHWU3DYnbqcE5TAaBuBqLpErgNlHWzbwrXjHJEM';
// --- $arduino_data_post = $_POST['name'];
// --- Set up your Firebase url structure here
$firebasePath = '/crossing/street1_pedestrians';
/// --- Making calls
$fb = new fireBase($url, $token);
$response = $fb->get($firebasePath);
echo $arduino_data;
echo $response;

// http://127.0.0.1:8000/arduino.php?arduino_data[street1_cars]=7&arduino_data[street_1]=Green
// php -S 127.0.0.1:8000