<?php
require('DiffEngine.php');
$my_diff_engine = new DiffEngine();
$unprocessed_data_path = 'data/unprocessed/';
$processed_data_path = 'data/processed/';
//Get data from existing json file
$dir = new DirectoryIterator($unprocessed_data_path);
foreach ($dir as $fileinfo) {
    if (!$fileinfo->isDot()) {
        $data_file = file_get_contents($unprocessed_data_path . $fileinfo->getFilename());
		// converts json data into array
		$json_file = json_decode($data_file, true);
		$deleted= array();
		$added = array();
		$file = fopen($processed_data_path . 'processed_' . $fileinfo->getFilename(), 'a');
		for ($i = 1; $i < count($json_file); $i++) {
			$from_lines = preg_split('/[\s]+/', $json_file["$i"][0]);
			$k = $i + 1;
			$to_lines = preg_split('/[\s]+/', $json_file["$k"][0]);
			$results = $my_diff_engine->diff($from_lines, $to_lines);
			foreach ($results as $object) {
				//If there are changes
				if (!$object->isEmpty()){
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
			};
			$should_store = true;
			if (count($deleted) > 0 && count($added) > 0){
				$should_store == false;
			} else if (count($deleted) == count($from_limes)){ //Someone deletes the whole article...vandalism?
				$should_store == false;
				$i++; //skip the next revision as well
			}
			if ($should_store){
			//Create updated json file
				$updated_data = json_encode(array('original' => $from_lines, 'category' => $json_file["$i"][1], 'references' => $json_file["$i"][2], 'deleted' => $deleted, 'added' => $added),JSON_PRETTY_PRINT);
				
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
	}
}
?>