// this gets called when the DOM has finished loading
$(document).ready(function() {
$('#btn-cam-1').on('click', {param1:'-not used-'}, resp_test );

function resp_test() {
	$.getJSON(
		'/_resp_test',
		{
			prm_inp_ctrl: $(this).attr('id')
		},
		function(data) {
			$('#msg-cam-1').text(data.rsp_msg1);
			});
}

})
