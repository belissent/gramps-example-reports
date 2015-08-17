

var full_report_list = []
$.getJSON("/gramps-example-reports/report_list.json", function(data) {
	full_report_list = data;
})
.fail(function() {
	full_report_list = [];
});


function build_report_list()
{
	// Get the current page
	var url = window.location.href;
	// this removes the anchor at the end, if there is one
	url = url.substring(0, (url.indexOf('#') == -1) ? url.length : url.indexOf('#'));
	// this removes the query after the file name, if there is one
	url = url.substring(0, (url.indexOf('?') == -1) ? url.length : url.indexOf('?'));
	
	var terms = ss.match(/(gramps\d\d)$/);
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
	$.each(full_report_list, function(version, report_list) {
		build_list($("#" + version), version, report_list);
	});
}


function build_version_list(version)
// version: in the form 'gramps40',  'gramps41', 'gramps42', 'gramps50', etc.
{
	build_list($("#" + version), version, full_report_list[version]);
}


function build_list(element, version, report_list)
{
	var html = '';
	html += '<table class="table table-striped">';
	html += '<thead><tr>';
	html += '<th>Report name</th>';
	html += '<th>Type</th>';
	html += '<th>Version</th>';
	html += '<th>Status</th>';
	html += '</tr></thead>';
	html += '<tbody>';
	for (var i = 0; i < report_list.length; i++)
	{
		html += '<tr>';
		html += '<td><a href="/' + version + '/' + report_list[i].directory + '">' + report_list[i].name + '</a></td>';
		html += '<td>' + report_list[i].type + '</td>';
		html += '<td>' + report_list[i].version + '</td>';
		html += '<td>' + report_list[i].status + '</td>';
		html += '</tr>';
	}
	html += '</tbody>';
	html += '</table>';
	element.html(html);
}
