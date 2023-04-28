<?php

#IPP 2. projekt 2020
#Author: Šimon Galba 
#login: xgalba03

$html_tests = "";		//Vytvorenie hlavičiek výslednýh HTML dokumentov, do html_tests budeme pridávať výsledky testov
$html = "<!DOCTYPE html>	
		<html>
		<head>
		    <!-- Hlavicka dokumentu -->
		    <meta charset=\"utf-8\">
		    <title>ITW - tvorba webových stránek</title>
		    <style>
		    h2{text-align:center;font-size:30px;}
		    h3{text-align:center;font-size:18px;}
		    body{background-color:#d7dbdd}
			table, th, td{ border;margin:auto;text-align:center;padding:8px;border-radius: 10px;border: 1px solid black;} 
		</style>
		</head>
		<body>	
		<h2>Prehľad výsledkov testovania<br>IPPcode20:</h2>
			<table>
			<th>Názov testu</th>
	<th>Výsledok</th>
	<th>Očakávaný návrat. kód</th>
	<th>Návratový kód</th>
	</tr>\n\n";

function error($code, $message){
	fwrite(STDERR, "$message\n");
	exit($code);
}


if($argc==1){
	error(STDERR, "Zle zadané argumenty\n");
}
else{
	if(array_search("--help", $argv)){
		if(count($argv) != 2){
			error("Argument '--help' je možné použiť len samostatne!\n", 10);
		}
		echo "Skript typu test (test.php v jazyce PHP 7.4) otestuje zadané skripty 'parse.php' alebo 'interpret.py' a vytvorí prehľadný HTML dokument s výsledkami.\n";
		echo "Parametre:\n";
		echo "--directory=path\n";
		echo "--recursive\n";
		echo "--parse-script=file\n";
		echo "---int-script=file\n";
		echo "---parse-only\n";
		echo "---int-only\n";
		echo "--jexamxml=file\n";
		echo "Všetky voliteľné parametre musia byť zadané spolu s argumentom --stats=file ktorý odkazuje na cieľový súbor ukladania štatistík.\n";
		exit(0);
	}	
	$recursive = 0;											//deklarácie všetkých potrebných premenných
	$parse_only = 0;
	$int_only = 0;
	$directory = 0;
	$parse_script = 0;
	$int_script = 0;
	$jexam = 0;
	$total_tests = 0;
	$fail_tests = 0;
	$success_tests = 0;	
	$first = True;
	$only = 0;
		// --------------------------------- Spracovanie argumentov 
	    foreach ($argv as $argument) {
	    	if(("test.php" == $argument) && ($first == True)){
	    		$first = False;
	    		continue;
	    	}
	    	if("--recursive" == $argument){
	    		$recursive = 1;
		    }
		    else if("--int-only" == $argument){
		    	$int_only = 1;
		    	$only++;
		    }
		    else if("--parse-only" == $argument){
		    	$parse_only = 1;
		    	$only++;
		    }
			else if (preg_match('/^--directory=(.)*$/u', $argument)) {
				$directory = 1;
				$directory_path = explode('=',$argument)[1];
			}
			else if (preg_match('/^--parse-script=(.)*$/u', $argument)) {
				$parse_script = 1;
				$parse_file = explode('=',$argument)[1];
			}
			else if (preg_match('/^--int-script=(.)*$/u', $argument)) {
				$int_script = 1;
				$int_file = explode('=',$argument)[1];
			}
			else if (preg_match('/^--jexamxml=(.)*$/u', $argument)) {
				$jexam = 1;
				$jexamxml_file = explode('=',$argument)[1];
			}
			else{
		    	error(10, "Zakazany parameter: ".$argument."\n");
	      		exit(10);
		    }
		}
	if ($directory != 1){			//ak nie sú tieto argumenty zadané, implicitne nastavíme cestu 
		$directory_path = '.';
	}
	if ($parse_script != 1){
		$parse_file = './parse.php';
	}
	if ($int_script != 1){
		$int_file = './interpret.py';
	}
	if ($jexam != 1){
		$jexamxml_file = "/pub/courses/ipp/jexamxml/jexamxml.jar";
	}

		// --------------- TEST existencie skriptov a dobre zadaných 'only' argumentov 
	if($only > 1){
		error(10, "Zle zadané argumenty0\n");
	    exit(10);
	}
	else if($int_only == 1){
		if(file_exists($int_file) == False){
			error(11,"parse.php nenájdený	");
		}	
	}
	else if($int_only == 1){
		if(file_exists($parse_file) == False){
			error(11,"parse.php nenájdený	");
		}
	}
	else{
		if((file_exists($parse_file) == False)||(file_exists($int_file) == False)){
			error(11,"pre beh testov je potrebné zadať cestu k parse.php aj interpet.py alebo ich umiestniť to adresára tohto testu");
		}
	}

	if(is_dir($directory_path) == False){ // Existencia testov
		error(11, "Testy nenájdené");
	}
	
}


if($recursive==1){	//testy chceme vykonávať rekurzívne (zložky v zložke)
	$Directory = new RecursiveDirectoryIterator($directory_path); 	//vytvorenie iterácií
	$Iterator = new RecursiveIteratorIterator($Directory);

    foreach ($Iterator as $file) {
	    if (is_dir($file) == true) {
	      continue;
	    }
	    else{
	    	$files[] = $file->getPathname();
	    	$files = array_diff($files, [".",".."]);
	    }	  
	} 
}
else { 			//alebo sa testuje len jedna zložka
	$dir = glob($directory_path.'/*.*');
	foreach($dir as $file){
		$files[] = $file;
	}
}

$empty_src = True;
foreach ($files as $src) {		//Vytvorenie listu src file - skript < test_name.src 
  if(preg_match('/.+.src$/u', $src)){
    $src_files[] = $src;
    $empty_src = False;
  }
}
if($empty_src){
	error(11, "Žiadne .SRC súbory na testovanie neboli nájdené");
}

$total_tests = count($src_files);

foreach ($src_files as $test) {		//Spustenie každého testu - parsovanie súboro potrebných na testovanie
  
	$test_name = str_replace(".src","", $test);
	$in_name = $test_name.".in";
	$out_name = $test_name.".out";
	$rc_name = $test_name.".rc";

	$res_in = fopen($in_name, "c+");
	  	if ($res_in==0){
			error(11, "Nepodarilo sa otvoriť súbor");
	    }
    fclose($res_in);

  	$res_out = fopen($out_name, "c+");
    	if ($res_out==0){
    		error(11, "Nepodarilo sa otvoriť súbor");
    	}
  	fclose($res_out);

	if (in_array($rc_name, $files)) {
		$ret_rc = file_get_contents($rc_name, $test);
	}
	else {
	    $res_rc = fopen($rc_name, "w");
	    if (!$res_rc){exit(11);}
	    fwrite($res_rc, "0\n");
	    $ret_rc = 0;
	    fclose($res_rc);
	  }
 //----------------------------- PARSER
  if($parse_only){
  	$tmp_file = $test_name.".tmp";
	  $input_inter = $test_name.".in";

	  exec("php7.4 $parse_file < $test > $tmp_file", $output_parse, $return_parse);
	  if($return_parse != 0){
	    if ($ret_rc == $return_parse){
	      $html_tests .= "<tr style=\"text-align:center;background-color:#33CC00;padding:10px;border: 1px solid black;height:15px;\"> 
							<td>$test_name</td>
							<td>success</td>
							<td>$ret_rc</td>
						  <td>$int_ret</td>
							</tr>\n";	
	      $success_tests++;
	    }
	    else {
	      $html_tests .= "<tr style=\"text-align:center;background-color:#FF0033;padding:10px;border: 1px solid black;height:15px;\"> 
							<td>$test_name</td>
							<td>fail</td>
							<td>$ret_rc</td>
						  <td>$int_ret</td>
							</tr>\n";	
	      $fail_tests++;
	    }
	  }
	  else {
	  	$out_file = $test_name.".out";
	  	exec("java -classpath $jexamxml_file com.a7soft.examxml.ExamXML $tmp_file $out_file", $diff, $rc_diff);
	    if ($rc_diff == 0){
	      $html_tests .= "<tr style=\"text-align:center;background-color:#33CC00;padding:10px;border: 1px solid black;height:15px;\"> 
							<td>$test_name</td>
							<td>success</td>
							<td>$ret_rc</td>
						  <td>$int_ret</td>
							</tr>\n";	
	      $success_tests++;
	    }
	    else {
	      $html_tests .= "<tr style=\"text-align:center;background-color:#FF0033;padding:10px;border: 1px solid black;height:15px;\"> 
							<td style= padding: 50px>$test_name</td>
							<td>fail</td>
							<td>$ret_rc</td>
						  <td>$int_ret</td>
							</tr>\n";	
	      $fail_tests++;
	    }
	  }
	  unlink($tmp_file);
  }
 //----------------------------- INTERPRET
  else if($int_only){
  	  $diff = 0;
  	  $tmp_file = $test_name.".tmp";
	  $input_inter = $test_name.".in";
	  $source = $test_name.".src";
	  exec("python3.8 $int_file --source=".$source. " < ".$input_inter." > " .$tmp_file, $int_out, $int_ret);
	    if ($int_ret != $ret_rc) {
	      $html_tests .= "<tr style=\"text-align:center;background-color:#FF0033;padding:10px;border: 1px solid black;height:15px;\"> 
							<td style= padding: 50px>$test_name</td>
							<td>fail</td>
							<td>$ret_rc</td>
						  <td>$int_ret</td>
							</tr>\n";	
	      $fail_tests++;
	    }
	    else {
	      if($int_ret == 0){
	        $out_file = $test_name.".out";       
	        exec("diff $tmp_file $out_file", $diff, $rc_diff);	
	        if (count($diff) == 0){ 
	          $html_tests .= "<tr style=\"text-align:center;background-color:#33CC00;padding:10px;border: 1px solid black;height:15px;\"> 
							<td>$test_name</td>
							<td>success</td>
							<td>$ret_rc</td>
						  <td>$int_ret</td>
							</tr>\n";	
	          $success_tests++;
	        }
	        else {
	          $html_tests .= "<tr style=\"text-align:center;background-color:#FF0033;padding:10px;border: 1px solid black;height:15px;\"> 
							<td>$test_name</td>
							<td>fail</td>
							<td>$ret_rc</td>
						  <td>$int_ret</td>
							</tr>\n";	
	          $fail_tests++;
	        }
	      }
	      else {
	        $html_tests .= "<tr style=\"text-align:center;background-color:#33CC00;padding:10px;border: 1px solid black;height:15px;\"> 
							<td>$test_name</td>
							<td>success</td>
							<td>$ret_rc</td>
						  <td>$int_ret</td>
							</tr>\n";	
	        $success_tests++;
	      }
	    }
  }
 //----------------------------- BOTH
  else{
  	$tmp_file = $test_name.".tmp";
	  $input_inter = $test_name.".in";
	  exec("php7.4 $parse_file < $test", $output_parse, $return_parse);
	  if($return_parse == 0){
	    if ($ret_rc != $return_parse){
	    	 $html_tests .= "<tr style=\"text-align:center;background-color:#33CC00;padding:10px;border: 1px solid black;height:15px;\"> 
							<td>$test_name</td>
							<td>success</td>
							<td>$ret_rc</td>
						  <td>$int_ret</td>
							</tr>\n";	
	      $success_tests++;
	    }
	    else {
	      $html_tests .= "<tr style=\"text-align:center;background-color:#FF0033;padding:10px;border: 1px solid black;height:15px;\"> 
							<td>$test_name</td>
							<td>fail</td>
							<td>$ret_rc</td>
						  <td>$int_ret</td>
							</tr>\n";	
	      $fail_tests++;
	    }
	  }
	  else {
	    
	    $output_parse = implode("\n", $output_parse);
	    $temp = tmpfile();
	    fwrite($temp, $output_parse);
	    exec("python3.8 $int_file --source=".stream_get_meta_data($temp)['uri']. " < ".$input_inter." > " .$tmp_file, $int_out, $int_ret);
	    fclose($temp);
	    if ($int_ret != $ret_rc) { 
	      $html_tests .= "<tr style=\"text-align:center;background-color:#FF0033;padding:10px;border: 1px solid black;height:15px;\"> 
							<td>$test_name</td>
							<td>fail</td>
							<td>$ret_rc</td>
						  <td>$int_ret</td>
							</tr>\n";	
	      $fail_tests++;
	    }
	    else {
	      if ($int_ret == 0) {
	        $out_file = $test_name.".out";
	        exec("diff $tmp_file $out_file", $diff, $rc_diff);
	        if (count($diff) == 0){
	          $html_tests .= "<tr style=\"text-align:center;background-color:#33CC00;padding:10px;border: 1px solid black;height:15px;\"> 
							<td>$test_name</td>
							<td>success</td>
							<td>$ret_rc</td>
						  <td>$int_ret</td>
							</tr>\n";	
	          $success_tests++;
	        }
	        else {
	          $html_tests .= "<tr style=\"text-align:center;background-color:#FF0033;padding:10px;border: 1px solid black;height:15px;\"> 
							<td>$test_name</td>
							<td>fail</td>
							<td>$ret_rc</td>
						  <td>$int_ret</td>
							</tr>\n";	
	          $fail_tests++;
	        }
	      }
	      else {
	         $html_tests .= "<tr style=\"text-align:center;background-color:#33CC00;padding:10px;border: 1px solid black;height:15px;\"> 
							<td>$test_name</td>
							<td>success</td>
							<td>$ret_rc</td>
						  <td>$int_ret</td>
							</tr>\n";	
	        $success_tests++;
	      }
	    }
	    unlink($tmp_file);
	  }
  }
  if($total_tests != 0){
  	$rate = round(($success_tests / $total_tests) * 100);
  }
  else{
  	$rate = 0;
  }
}

$html .= "
<h2>Štatistiky:<br></h2>
<h3>
Úspešné testy: $success_tests<br>
Neúspešné testy: $fail_tests<br>
Úspešnosť: $rate %<br>
</h3>";
$html .= $html_tests;
$html.= "</table></body></html>";

echo $html;


?>