function CheckPassword()
{
	if ( $("#acset").val() == '' || $("#pwset").val() == '') {
		$("#wronginfo").html('<font color="#FF0000" >帳號或密碼不得為空！</font>');
	}
	else{
	    $.ajax({
	      url: "/search",
	      type: "post",
	      data: {account: $("#acset").val(), password: $("#pwset").val(), cpe_num: $("#cpeset").val()},
	      success: function(response) {
	      	if (response.indexOf('錯誤') > 0) {
	      		$("#wronginfo").html(response);
	      	}
	      	else {
	      		$("#one").html(response);
	      	}
	      },
	      error: function(xhr) {
	        alert("Something went wrong");
	      }
	    });
	}
}