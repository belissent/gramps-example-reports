

full_report_list = [];

$.getJSON("/gramps-example-reports/report_list.json", function(data) {
	full_report_list = data;
	build_report_list();
})
.fail(function() {
	full_report_list = [];
	$("#contents").html('<div class="alert alert-danger" role="alert">Internal error</div>');
});


function build_report_list()
{
	// Get the current page
	var url = window.location.href;
	// this removes the anchor at the end, if there is one
	url = url.substring(0, (url.indexOf('#') == -1) ? url.length : url.indexOf('#'));
	// this removes the query after the file name, if there is one
	url = url.substring(0, (url.indexOf('?') == -1) ? url.length : url.indexOf('?'));
	
	var terms = url.match(/(gramps\d\d)$/);
	if (terms == null)
	{
		// We are in the root directory
		build_header_list();
	}
	else
	{
		// We are in a version directory '/grampsXX'
		build_version_list(terms[0]);
	}
}


function build_header_list()
{
	var html = '';
	html += '<ul class="nav nav-pills">';
	html += '	<li role="presentation"><a href="#gramps40" role="tab" data-toggle="tab">Version 4.0</a></li>';
	html += '	<li role="presentation"><a href="#gramps41" role="tab" data-toggle="tab">Version 4.1</a></li>';
	html += '	<li role="presentation"><a href="#gramps42" role="tab" data-toggle="tab">Version 4.2</a></li>';
	html += '	<li role="presentation" class="active"><a href="#gramps50" role="tab" data-toggle="tab">Version 5.0</a></li>';
	html += '</ul>';
	html += '<div class="tab-content">';
	$.each(full_report_list, function(version, report_list) {
		var txt = build_list(version, report_list);
		html += '<div id="' + version + '" role="tabpanel" class="tab-pane' + ((version == 'gramps50') ? ' active' : '') + '">' + txt + '</div>';
	});
	html += '</div>';
	$("#contents").html(html);
}


function build_version_list(version)
// version: in the form 'gramps40',  'gramps41', 'gramps42', 'gramps50', etc.
{
	var txt = build_list(version, full_report_list[version]);
	var html = '';
	html += txt;
	html += '<p><a href="/gramps-example-reports">Other GRAMPS versions</a>';
	$("#contents").html(html);
}


function build_list(version, report_list)
{
	var html = '';
	html += '<table class="table table-striped">';
	html += '<thead><tr>';
	html += '<th>Report name</th>';
	html += '<th>Title</th>';
	html += '<th>Type</th>';
	html += '<th>Version</th>';
	html += '<th>Status</th>';
	html += '</tr></thead>';
	html += '<tbody>';
	for (var i = 0; i < report_list.length; i++)
	{
		html += '<tr>';
		html += '<td><a href="/gramps-example-reports/' + report_list[i].result + '">' + report_list[i].name + '</a></td>';
		html += '<td>' + report_list[i].title + '</td>';
		html += '<td>' + report_list[i].type + '</td>';
		html += '<td>' + report_list[i].version + '</td>';
		html += '<td>' + report_list[i].status + '</td>';
		html += '</tr>';
	}
	html += '</tbody>';
	html += '</table>';
	return(html);
}
