// Gramps - a GTK+/GNOME based genealogy program
//
// Copyright (C) 2014 Pierre B�lissent
//
// This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.
// This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
// You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA


//=================================================================
//=================================================== Search string
//=================================================================

// The parameters used for all the pages are given below
// The ParseSearchString function updates the variables below from the URL search string
// The BuildSearchString function builds the URL search string from the variables below

var search = {
	//gramps_version; // Gramps version on 2 digits
	//log; // Index of the report (in table full_report_list) for printing the log
	//name; // filters the table for reports with corresponding name
	//id; // filters the table for reports with corresponding id
	//type; // filters the table for reports with corresponding type
	//category; // filters the table for reports with corresponding category
	//status; // filters the table for reports with corresponding status
};

filters = ['gramps_version', 'name', 'id', 'type', 'category', 'status'];
filter_names = ['Gramps version', 'Name', 'Id', 'Type', 'Category', 'Status']

// Was the URL search string parsed ?
var searchInitialized = false;

function ParseSearchString()
{
	// Parse the URL search string
	if (searchInitialized) return;
	searchInitialized = true;
	search.gramps_version = GetURLParameter('v', '');
	search.log = GetURLParameter('l', -1);
	search.name = GetURLParameter('n', '');
	search.id = GetURLParameter('id', '');
	search.type = GetURLParameter('t', '');
	search.category = GetURLParameter('c', '');
	search.status = GetURLParameter('s', '');
}

function GetURLParameter(sParam, def)
{
	// Get a value from the URL search string
	// sParam: name of the parameter
	// def: Parameter default value
	var sPageURL = window.location.search.substring(1);
	var sURLVariables = sPageURL.split('&');
	for (var i = 0; i < sURLVariables.length; i++)
	{
		var sParameterName = sURLVariables[i].split('=');
		if (sParameterName[0] == sParam)
		{
			var s = decodeURIComponent(sParameterName[1]);
			if (typeof(def) == 'number')
			{
				s = parseInt(s);
				if (isNaN(s)) s = def;
			}
			if (def instanceof Array) s = $.parseJSON(s);
			if (typeof(def) == 'boolean')
			{
				if ($.inArray(s, ['true', 'on']) >= 0) s = true;
				if ($.inArray(s, ['false', 'off']) >= 0) s = false;
				if (!isNaN(parseInt(s))) s = parseInt(s);
				s = s ? true : false;
			}
			return(s);
		}
	}
	return(def);
}

function BuildSearchString(params)
{
	// Builds the URL search string from the global parameters values ("search")
	// and from the optional parameter of the function "params"
	// "params" has the same structure as "search"
	params = (typeof(params) !== 'undefined') ? params : {};
	var s = '';
	page = window.location.href.replace(/\?.*/, '').replace(toRoot, '���').replace(/.*���/, '');
	s = SetURLParameter(s, 'v', params.Txt, search.gramps_version, '');
	s = SetURLParameter(s, 'l', params.Txt, search.log, -1);
	s = SetURLParameter(s, 'n', params.Txt, search.name, '');
	s = SetURLParameter(s, 'id', params.Txt, search.id, '');
	s = SetURLParameter(s, 't', params.Txt, search.type, '');
	s = SetURLParameter(s, 'c', params.Txt, search.category, '');
	s = SetURLParameter(s, 's', params.Txt, search.status, '');
	return(s);
}

function SetURLParameter(sString, sParam, new_val, val, def)
{
	// Update the URL search string "sString" with the parameter "sParam"
	// new_val is the new parameter value, if any
	// val is the current parameter value, if any
	// val is the default parameter value, of type: number, boolean, Array, string
	
	// Manage when values are not provided
	val = (val == null || typeof(val) == 'undefined') ? def : val;
	val = (new_val == null || typeof(new_val) == 'undefined' || new_val == def) ? val : new_val;
	// Manage each type of value
	if (typeof(def) == 'number')
	{
		val = parseInt(val);
	}
	// else if (typeof(def) == 'string')
	// {
		// val = (val == '') ? def : val;
		// val = (new_val == '') ? val : new_val;
	// }
	else if (def instanceof Array)
	{
		val = (val == null || typeof(val) == 'undefined' || val.length == 0) ? def : val;
		val = (new_val == null || typeof(new_val) == 'undefined' || new_val.length == 0) ? val : new_val;
		val = JSON.stringify(val);
		def = JSON.stringify(def);
	}
	else if (typeof(def) == 'boolean')
	{
		val = val ? 1: 0;
		def = def ? 1: 0;
	}
	// Don't modify the search string if the value = default value
	if (val == def) return(sString);
	if (sString != '') sString += '&';
	return(sString + sParam + '=' + encodeURIComponent(val.toString()));
}


//=================================================================
//=================================================== Build page
//=================================================================

ParseSearchString();

// Get current directory
var winloc = window.location.pathname;
var homedir = '.';

// Get the current page
var url = window.location.href;
// this removes the anchor at the end, if there is one
url = url.substring(0, (url.indexOf('#') == -1) ? url.length : url.indexOf('#'));
// this removes the query after the file name, if there is one
url = url.substring(0, (url.indexOf('?') == -1) ? url.length : url.indexOf('?'));

$(document).ready(build_page);

versions = ['gramps40', 'gramps41', 'gramps42', 'gramps50'];
versions2 = ['40', '41', '42', '50'];
versions3 = ['4.0', '4.1', '4.2', '5.0'];
versions = ['gramps42', 'gramps50'];
versions2 = ['42', '50'];
versions3 = ['4.2', '5.0'];


function build_page()
{
	// Get selected version
	var terms = url.match(/gramps(\d\d)/);
	if (!(terms == null))
	{
		// We are in a version directory '/grampsXX'
		homedir = '..';
		search.gramps_version = terms[1];
	}
	// Get selected version
	var terms = url.match(/list.html/);
	var is_header = (search.gramps_version == '') && !(url.match(/list.html/));
	
	// build the page
	if (search.log >= 0)
	{
		// Print a report log
		build_log();
	}
	else if (is_header)
	{
		// We are in the root directory
		build_header();
	}
	else
	{
		build_list();
	}
}


//=================================================================
//=================================================== Main page
//=================================================================

function build_header()
{
	var html = '';
	for (var i = 0; i < versions3.length; i += 1)
	{
		html += ' <a href="gramps' + (versions3[i] * 10) + '/index.html"><button class="btn btn-primary" type="button">Version ' + versions3[i] + '</button></a>';
	}
	html += ' <a href="list.html"><button class="btn btn-primary" type="button">All versions</button></a>';
	$("#contents").html(html);
}


//=================================================================
//=============================================== Reports list page
//=================================================================

function build_list()
{
	// Build one report list
	var reports = [];
	for (var i = 0; i < versions.length; i += 1)
	{
		var v = versions[i];
		if (typeof(full_report_list[v]) == 'undefined') continue;
		for (var j = 0; j < full_report_list[v].length; j += 1)
		{
			full_report_list[v][j].gramps_version = versions2[i];
			reports.push(full_report_list[v][j]);
		}
	}
	// Filter the reports
	for (var f = 0; f < filters.length; f += 1)
	{
		var filter = filters[f];
		if (typeof(search[filter]) == 'undefined') continue;
		reports = $.grep(reports, function(elt, index) {
			return((elt[filter] == search[filter]) || (typeof(elt[filter]) == 'undefined'));
		});
	}
	// Write the table
	var html = '';
	if (reports.length == 0)
	{
		html += '<div class="alert alert-warning" role="alert">';
		html += 'No reports match the filter:';
		html += '<ul>';
		for (var f = 0; f < filters.length; f += 1)
		{
			var filter = filters[f];
			if (search[filter] != '') html += '<li>' + filter_names[f] + ': ' + search[filter] + '</li>';
		}
		html += '</ul>';
		html += '</div>';
		$('#contents').html(html);
		return;
	}
	html += '<table id="reports" data-toggle="table" class="table table-striped" data-filter-control="true">';
	html += '</table>';
	$('#contents').html(html);
	// Fill the table
	data = []
	for (var i = 0; i < reports.length; i++)
	{
		var datum = {}
		$.extend(datum, reports[i]); // deep copy
		if (reports[i].status)
			datum.title= '<a href="' + homedir + '/' + reports[i].result + '">' + reports[i].title + '</a>';
		if (reports[i].status)
			datum.status = 'OK';
		else
			datum.status = '<a href="' + url + '?v=' + reports[i].gramps_version + '&l=' + i + '">Error</a>';
		data.push(datum);
	}
	$('#reports').bootstrapTable({
		columns: [{
			field: 'title',
			title: 'Title',
			filterControl: 'select',
			sortable: true
		}, {
			field: 'name',
			title: 'Name',
			filterControl: 'select',
			sortable: true
		}, {
			field: 'type',
			title: 'Type',
			filterControl: 'select',
			align: 'center',
			sortable: true
		}, {
			field: 'category',
			title: 'Category',
			filterControl: 'select',
			align: 'center',
			sortable: true
		}, {
			field: 'format',
			title: 'Format',
			filterControl: 'select',
			align: 'center',
			sortable: true
		}, {
			field: 'version',
			title: 'Version',
			filterControl: 'select',
			align: 'center',
			sortable: true
		}, {
			field: 'status',
			title: 'Status',
			filterControl: 'select',
			align: 'center',
			sortable: true
		}],
		data: data,
		filterControl: false,
		search: true
	});
}

function _build_list()
{
	// Build one report list
	var reports = [];
	for (var i = 0; i < versions.length; i += 1)
	{
		var v = versions[i];
		if (typeof(full_report_list[v]) == 'undefined') continue;
		for (var j = 0; j < full_report_list[v].length; j += 1)
		{
			full_report_list[v][j].gramps_version = versions2[i];
			reports.push(full_report_list[v][j]);
		}
	}
	// Filter the reports
	for (var f = 0; f < filters.length; f += 1)
	{
		var filter = filters[f];
		$.grep(reports, function(elt, index) {
			return(elt[filter] == search[filter]);
		});
	}
	// Print table
	var html = '';
	if (reports.length == 0)
	{
		html += '<div class="alert alert-warning" role="alert">';
		html += 'No reports match the filter:';
		html += '<ul>';
		for (var f = 0; f < filters.length; f += 1)
		{
			var filter = filters[f];
			if (search[filter] != '') html += '<li>' + filter_names[f] + ': ' + search[filter] + '</li>';
		}
		html += '</ul>';
		html += '</div>';
	}
	else
	{
		html += build_filtered_list(reports);
	}
	$('#contents').html(html);
}


function build_filtered_list(report_list)
{
	var html = '';
	html += '<table id="reports" data-toggle="table" class="table table-striped" data-filter-control="true">';
	html += '<thead><tr>';
	html += '<th>Title</th>';
	html += '<th data-filter-control="select">Name</th>';
	html += '<th data-filter-control="select">Type</th>';
	html += '<th data-filter-control="select">Category</th>';
	html += '<th>Version</th>';
	html += '<th data-filter-control="select">Status</th>';
	html += '</tr></thead>';
	html += '<tbody>';
	for (var i = 0; i < report_list.length; i++)
	{
		html += '<tr>';
		if (report_list[i].status)
		{
			html += '<td><a href="' + homedir + '/' + report_list[i].result + '">' + report_list[i].title + '</a></td>';
		}
		else
		{
			html += '<td>' + report_list[i].title + '</td>';
		}
		html += '<td>' + report_list[i].name + '</td>';
		html += '<td>' + report_list[i].type + '</td>';
		html += '<td>' + report_list[i].category + '</td>';
		html += '<td>' + report_list[i].version + '</td>';
		if (report_list[i].status)
		{
			html += '<td>OK</td>';
		}
		else
		{
			html += '<td><a href="' + url + '?v=' + report_list[i].gramps_version + '&l=' + i + '">Error</a></td>';
		}
		html += '</tr>';
	}
	html += '</tbody>';
	html += '</table>';
	return(html);
}


//=================================================================
//=================================================== log page
//=================================================================

function build_log()
{
	var report = full_report_list['gramps' + search.gramps_version][search.log];
	var html = '';
	html += '<p>Report log for the report <mark>' + report.title + '</mark> (name: <mark>' + report.name + '</mark>, id: <mark>' + report.id + '</mark>)</p>';
	var txt = report.log
	var txt = txt.replace(/&/g, '&amp;');
	var txt = txt.replace(/>/g, '&gt;');
	var txt = txt.replace(/</g, '&lt;');
	var re = new RegExp('(Using options string.*name=)(' + report.id + ')([ ,\\n].*)', 'g');
	var txt = txt.replace(re, '<p><span class="alert alert-danger" role="alert">$1<mark>$2</mark>$3</span></p>');
	html += '<pre>' + txt + '</pre>';
	$("#contents").html(html);
}
