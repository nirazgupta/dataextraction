
// function validate(){
// 	var user = document.loginform.username.value;
// 	var pass = document.loginform.password.value;
// 	if(user == ""){
// 		document.getElementById('useralert').innerHTML="Please enter the username";
// 		document.getElementById('form_css1').style.borderColor = "red";
// 		return false;
// 	}
// 	else if(pass == ""){
// 		document.getElementById('passalert').innerHTML="Please enter the password";
// 		document.getElementById('form_css2').style.borderColor = "red";
// 		return false;
// 	}

// }

// setTimeout(function() {
//  $('.alert').fadeOut();
// }, 3000 );

// $("document").ready(function(){

//     $("#usr_trans_li").click(function(){
//         $('#content').load('/trans_view #trans_tbl', function() {
//             });
//     });

//     $("#usr_dash_li").click(function(){
//         $('#content').load('/dashboard #msg', function() {
//             });
//     });
// });



// //Attemp to do the calculation using javascript but decided to use python instead. And use javascript for making ajax and jquery calls
// var year;
// var month;
// var rate;
// var amount;
// var montyly_payment;

// $("document").ready(function() {
// 	$("#submit").click(function() {

// 		year = document.getElementById("year").value;
//   		month = document.getElementById("month").value;
//   		rate = document.getElementById("rate").value;
//   		amount = document.getElementById("amount").value;
//   		term_raw = year * 12;
//   		term = term_raw + month;
//   		rate = rate/1200;
// 		mPmt = calculatePayment();
		  
// 		var a = 5;
// 		var b = 6;
// 		var c = a + b;
// 		console.log(c);
//   		document.getElementById("pmt").value = "$" + mPmt.toFixed(2);
//   		document.getElementById("output").innerHTML = c;
// 	});
// });


// function calculatePayment()
// {
// 	var payment = amount*(apr * Math.pow((1 + rate), term))/(Math.pow((1 + rate), term) - 1);
	
// 	return payment;
// }



// jQuery.browser = {};
// (function () {
//     jQuery.browser.msie = false;
//     jQuery.browser.version = 0;
//     if (navigator.userAgent.match(/MSIE ([0-9]+)\./)) {
//         jQuery.browser.msie = true;
//         jQuery.browser.version = RegExp.$1;
//     }
// })();


// $("document").ready(function() {
	  
// 	$("#user_form").validate({
// 	  rules: {
// 			name: "required",
// 			email: {
// 				required: true,
// 				email: true
// 			},
// 			mortgage_config_name: "required",
// 		},
// 		messages: {
// 			name: "Please enter your first name",
// 			email: "Please enter a valid email address",
// 			mortgage_config_name: "Please enter a name for this mortgage",
// 		},

// 		submitHandler: function(form) {
// 			$.ajax({
// 				type: 'POST',
// 				url:'/user/',
// 				data: {
// 					name:$('#name').val(),
// 					email:$('#email').val(),
// 					mortgage_name:$('#mortgage_config_name').val(),
// 					csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
// 				},
// 				success: function(){
	
// 				}
				
// 			});

// 			$( "#user_form" ).toggle( "slow", function() {
// 				$('#content').load('/loan #loan_form', function() {
// 				});
// 			});
	
// 			$("#user_toggle").click(function(){
// 				$( "#user_form" ).toggle( "slow", function() {
// 					});
// 			});
// 		}
// 	});
	
// 	jQuery.validator.addMethod("lettersonly", function(value, element) {
// 	  return this.optional(element) || /^[a-z]+$/i.test(value);
// 	}, "Letters only please"); 

// });

// function validateForm() {
// 	var amount = document.forms["loan_form"]["loan_amount"].value;
// 	var year = document.forms["loan_form"]["year"].value;
// 	var month = document.forms["loan_form"]["month"].value;
// 	var rate = document.forms["loan_form"]["rate"].value;
// 	var extra_monthly = document.forms["loan_form"]["add_per_month"].value;
// 	var extra_yearly = document.forms["loan_form"]["add_per_year"].value;

//     if (amount == "") {
//         alert("Loan amount must be filled out");
//         return false;
// 	} else if (amount !=="" && !$.isNumeric(amount)){
// 		alert("Please enter only numbers for Loan amount")
// 		return false;
// 	} else if(year == '' || year > 30){
// 		alert("Please choose year between range of 1 to 30");
//         return false;
// 	} else if(year !=="" && !$.isNumeric(year)){
// 		alert("Please choose year between range of 1 to 30");
//         return false;
// 	}else if (rate == ''){
// 		alert("Rate must be filled out");
// 		return false;
// 	} else if(rate !=="" && !$.isNumeric(rate)){
// 		alert("Please enter only numbers for rate amount. Example: 5, 4.5, etc.");
//         return false;
// 	} else if(extra_monthly =="" || extra_yearly ==""){
// 		alert("Please enter amount for extra payment");
// 		return false;
// 	} else if(extra_monthly > 0 && extra_yearly > 0){
// 		alert("Please enter amount for either monthly or annual extra payment");
//         return false;
// 	} 
// }


// $("document").ready(function() {
// 	$("#ammortization_table_btn").click(function(){
// 		$( "#ammortization_table" ).toggle( "slow", function() {
// 			});
// 	});
// });


// $("document").ready(function() {
// 	$(extra_options_form).hide();
// 	$("#extra_options").click(function(){
// 		$( "#extra_options_form" ).toggle( "slow", function() {
			
// 		});
// 	});
// });

	

// $("document").ready(function() {
// 	$('input[name=checkbox1]').click(function() {
// 		alert('pdf is selected')
// 		if($(this).attr('id') == 'pdf') {
			
// 			 $('#reveal-if-active').show();           
// 		}
 
// 		else {
// 			 $('#group2').hide();   
// 		}
// 	});
//  });
$('document').ready(function(){
	// $('#radiogrp2').hide();
	// $('#radiogrp3').hide();
	// $('#pdf').click(function() {

	// 	if ($( "#pdf" ).prop( "checked", true )) {
	// 		$('#radiogrp2').show();
	// 		$('#radiogrp3').hide();
	// 	}
		
	//  });
	 
	//  $('#dxf').click(function() {
	// 	if ($( "#dxf" ).prop( "checked", true ))  {
	// 		$('#radiogrp3').show();
	// 		$('#radiogrp2').hide();
	// 	}
	//  });

	var input = document.getElementById( 'file-upload' );
	var infoArea = document.getElementById( 'file-upload-filename' );
	
	input.addEventListener( 'change', showFileName );

	function showFileName( event ) {
	
	// the change event gives us the input it occurred in 
	var input = event.srcElement;
	
	// the input has an array of files in the `files` property, each one has a name that you can use. We're just using the name here.
	var fileName = input.files[0].name;
	
	// use fileName however fits your app best, i.e. add it into a div
	infoArea.value =  fileName;
	}
});

$(function() {
	$("#mycontent").hide();
	$("#loadDiv").on("click",function(e) {
	  e.preventDefault();
	  $("#mycontent").toggle();
	});
  });


  $(document).ready(function() {
    $("textarea").each(function(n, obj) {
        fck = new FCKeditor(obj.id) ;
            fck.BasePath = "/admin-media/fckeditor/" ;
            fck.ReplaceTextarea() ;
    });
});



  $.ajax({ 
	url: "/add", 
	type: 'GET', 
	dataType: 'json', 
	async: true, 
	data: {},  
	success: function (data) { 
		console.log(data)
		// var pos_data = JSON.parse(data); 
		// const loadingTask = PDFJS.getDocument("/test.pdf");
		// const pdf = await loadingTask.promise;
	
		// // Load information from the first page.
		// const page = await pdf.getPage(1);
	
		// const scale = 1;
		// const viewport = page.getViewport(scale);
	
		// // Apply page dimensions to the <canvas> element.
		// const canvas = document.getElementById("pdf");
		// const context = canvas.getContext("2d");
		// canvas.height = viewport.height;
		// canvas.width = viewport.width;
	
		// // Render the page into the <canvas> element.
		// const renderContext = {
		// canvasContext: context,
		// viewport: viewport
		// };
		// await page.render(renderContext);
		// console.log("Page rendered!");
	}
})

  