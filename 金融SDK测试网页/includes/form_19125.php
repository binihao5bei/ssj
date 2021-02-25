<?php	
	if (empty($_POST['name2_30419_11176_34432_19125']) && strlen($_POST['name2_30419_11176_34432_19125']) == 0 || empty($_POST['email2_30419_11176_34432_19125']) && strlen($_POST['email2_30419_11176_34432_19125']) == 0 || empty($_POST['email2_30419_11176_34432_19125']) && strlen($_POST['email2_30419_11176_34432_19125']) == 0)
	{
		return false;
	}
	
	$name2_30419_11176_34432_19125 = $_POST['name2_30419_11176_34432_19125'];
	$email2_30419_11176_34432_19125 = $_POST['email2_30419_11176_34432_19125'];
	$email2_30419_11176_34432_19125 = $_POST['email2_30419_11176_34432_19125'];
	
	$to = 'receiver@yoursite.com'; // Email submissions are sent to this email

	// Create email	
	$email_subject = "Message from a Blocs website.";
	$email_body = "You have received a new message. \n\n".
				  "Name2_30419_11176_34432_19125: $name2_30419_11176_34432_19125 \nEmail2_30419_11176_34432_19125: $email2_30419_11176_34432_19125 \nEmail2_30419_11176_34432_19125: $email2_30419_11176_34432_19125 \n";
	$headers = "MIME-Version: 1.0\r\nContent-type: text/plain; charset=UTF-8\r\n";	
	$headers .= "From: contact@yoursite.com\n";
	$headers .= "Reply-To: DoNotReply@yoursite.com";	
	
	mail($to,$email_subject,$email_body,$headers); // Post message
	return true;			
?>