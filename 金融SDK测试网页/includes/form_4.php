<?php	
	if (empty($_POST['email3']) && strlen($_POST['email3']) == 0 || empty($_POST['email3']) && strlen($_POST['email3']) == 0 || empty($_POST['email3']) && strlen($_POST['email3']) == 0)
	{
		return false;
	}
	
	$email3 = $_POST['email3'];
	$email3 = $_POST['email3'];
	$email3 = $_POST['email3'];
	$email3 = $_POST['email3'];
	$email3 = $_POST['email3'];
	
	$to = 'receiver@yoursite.com'; // Email submissions are sent to this email

	// Create email	
	$email_subject = "Message from a Blocs website.";
	$email_body = "You have received a new message. \n\n".
				  "Email3: $email3 \nEmail3: $email3 \nEmail3: $email3 \nEmail3: $email3 \nEmail3: $email3 \n";
	$headers = "MIME-Version: 1.0\r\nContent-type: text/plain; charset=UTF-8\r\n";	
	$headers .= "From: contact@yoursite.com\n";
	$headers .= "Reply-To: DoNotReply@yoursite.com";	
	
	mail($to,$email_subject,$email_body,$headers); // Post message
	return true;			
?>