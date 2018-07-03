<?php
require('DiffEngine.php');
$my_diff_engine = new DiffEngine();
//Get data from existing json file
$data_file = file_get_contents('data.json');
// converts json data into array
$json_file = json_decode($data_file, true);

$deleted= array();
$added = array();
$file = fopen('final_data.json', 'a');
echo count($json_file);
for ($i = 1; $i < count($json_file); $i++) {
	$from_lines = preg_split('/[\ \n\,]+/', $json_file["$i"]);
	$k = $i + 1;
	$to_lines = preg_split('/[\ \n\,]+/', $json_file["$k"]);
	$results = $my_diff_engine->diff($from_lines, $to_lines);
	foreach ($results as $object) {
		//Group all deleted and added parts
	    if ($object->getType() === "change"){
			foreach ($object->getOrig() as $result_array){
				$deleted[] = $result_array;
			}
			foreach ($object->getClosing() as $result_array){
				$added[] = $result_array;
			}
		}
		else if ($object->getType() === "add"){
			foreach ($object->getClosing() as $result_array){
				$added[] = $result_array;
			}
		}
		else if ($object->getType() === "delete"){
			foreach ($object->getOrig() as $result_array){
				$deleted[] = $result_array;
			}
		}
	};
	if (isset($deleted) || isset($added)){
			//Create updated json file
			$updated_data = json_encode(array('original' => $json_file["$i"], 'deleted' => $deleted, 'added' => $added),JSON_PRETTY_PRINT);
			
			//Write to a new file
			fwrite($file, $updated_data);
			//Clear data for next iteration
			$from_lines = array();
			$to_lines = array();
			$results = array();
			$added = array();
			$deleted = array();
			}
}
fclose($file);
// foreach ($deleted as $deleted_part){
// 	$deleted_content = $deleted_part[0];
// 	$deleted_index = $deleted_part[1];
// 	echo "Deleted: $deleted_content -- index: $deleted_index <br> ";
// }
// foreach ($added as $added_part){
// 	$added_content = $added_part[0];
// 	$added_index = $added_part[1];
// 	echo "Added: $added_content -- index: $added_index <br>";
// }


?>