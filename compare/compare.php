<?php
function checkLegit($text){
	if (in_array("REDIRECT", $text)){
		return false;
	};
	return true;
}


ini_set('memory_limit', '-1'); //json files are big. let the server use all the memory it wants
require('DiffEngine.php');
$my_diff_engine = new DiffEngine();
$unprocessed_data_path = 'data/unprocessed/';
$processed_data_path = 'data/processed/';
//Get data from existing json file
$dir = new DirectoryIterator($unprocessed_data_path);
$handle = fopen("data/unprocessed/outputfile", "r");
$file = fopen($processed_data_path . 'processed_outputfile', 'a');
if ($handle) {
	$isFirst = true;
    while (($line = fgets($handle)) !== false) {
        // process the line read.
        if ($isFirst){
        	$first_revision = json_decode($line, true);
        	$isFirst = false;
        }else {
        	$second_revision = json_decode($line, true);
        	$deleted= array();
			$added = array();
			$from_lines = $first_revision['text'];
			$to_lines = $second_revision['text'];
			$results = $my_diff_engine->diff($from_lines, $to_lines);
			$first_revision = $second_revision;
			foreach ($results as $object) {
				//If there are changes
				if (!$object->isEmpty()){
					//Group all deleted and added parts
				    if ($object->getType() === "change"){
				    	//if no one deletes the whole document
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
						//if no one deletes the whole document
			    		foreach ($object->getOrig() as $result_array){
							$deleted[] = $result_array;
						}
					};
				};
			};
				$should_store = true;
				if (!checkLegit($deleted) || !checkLegit($added) || !checkLegit($from_lines) || (count($deleted) == count($from_lines)) || ((count($deleted) == 0) && (count($added) == 0)) ){
					$should_store = false;
				};
				if ($should_store){
					//Create updated json file
					$updated_data = json_encode(array('original' => $from_lines, 'deleted' => $deleted, 'added' => $added),JSON_PRETTY_PRINT);	
					//Write to a new file
					fwrite($file, $updated_data);
				}
				//Clear data for next iteration
				$from_lines = array();
				$to_lines = array();
				$results = array();
				$added = array();
				$deleted = array();
			}
		}
	fclose($file);
    fclose($handle);
} else {
    // error opening the file.
} 
// foreach ($dir as $fileinfo) {
//     if (!$fileinfo->isDot() && $fileinfo->getFilename() == 'input' ) {
//         $data_file = file_get_contents($unprocessed_data_path . $fileinfo->getFilename());
// 		// converts json data into array
// 		echo $data_file
// 		$json_file = json_decode($data_file, true);
// 		$deleted= array();
// 		$added = array();
// 		$file = fopen($processed_data_path . 'processed_' . $fileinfo->getFilename(), 'a');
// 		for ($i = 1; $i < count($json_file); $i++) {
// 			$from_lines = $json_file["$i"][0];
// 			$k = $i + 1;
// 			$to_lines = $json_file["$k"][0];
// 			$results = $my_diff_engine->diff($from_lines, $to_lines);
// 			foreach ($results as $object) {
// 				//If there are changes
// 				if (!$object->isEmpty()){
// 					//Group all deleted and added parts
// 				    if ($object->getType() === "change"){
// 				    	//if no one deletes the whole document
// 			    		foreach ($object->getOrig() as $result_array){
// 							$deleted[] = $result_array;
// 						}
// 						foreach ($object->getClosing() as $result_array){
// 							$added[] = $result_array;
// 						}
// 					}
// 					else if ($object->getType() === "add"){
// 						foreach ($object->getClosing() as $result_array){
// 							$added[] = $result_array;
// 						}
// 					}
// 					else if ($object->getType() === "delete"){
// 						//if no one deletes the whole document
// 			    		foreach ($object->getOrig() as $result_array){
// 							$deleted[] = $result_array;
// 						}
// 					};
// 				};
// 			};
// 			$should_store = true;
// 			if (!checkLegit($deleted) || !checkLegit($added) || !checkLegit($from_lines) || (count($deleted) == count($from_lines)) || ((count($deleted) == 0) && (count($added) == 0)) ){
// 				$should_store = false;
// 			};
// 			if ($should_store){
// 				//Create updated json file
// 				$updated_data = json_encode(array('original' => $from_lines, 'category' => $json_file["$i"][1], 'references' => $json_file["$i"][2], 'deleted' => $deleted, 'added' => $added),JSON_PRETTY_PRINT);	
// 				//Write to a new file
// 				fwrite($file, $updated_data);
// 			}
// 			//Clear data for next iteration
// 			$from_lines = array();
// 			$to_lines = array();
// 			$results = array();
// 			$added = array();
// 			$deleted = array();
// 			}
// 		fclose($file);
// 	}
//}
?>