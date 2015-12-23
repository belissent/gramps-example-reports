// Gramps - a GTK+/GNOME based genealogy program
//
// Copyright (C) 2014 Pierre Bélissent
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
	s = SetURLParameter(s, 'v', params.gramps_version, search.gramps_version, '');
	s = SetURLParameter(s, 'l', params.log, search.log, -1);
	s = SetURLParameter(s, 'n', params.name, search.name, '');
	s = SetURLParameter(s, 'id', params.id, search.id, '');
	s = SetURLParameter(s, 't', params.type, search.type, '');
	s = SetURLParameter(s, 'c', params.category, search.category, '');
	s = SetURLParameter(s, 's', params.status, search.status, '');
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

versions = ['gramps40', 'gramps41', 'gramps42', 'gramps50'];
versions2 = ['40', '41', '42', '50'];
versions3 = ['4.0', '4.1', '4.2', '5.0'];
versions = ['gramps42', 'gramps50'];
versions2 = ['42', '50'];
versions3 = ['4.2', '5.0'];


// Trigger page build
$(document).ready(build_page);


function build_page()
{
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
		html += ' <a href="list.html?' + BuildSearchString({gramps_version: versions2[i]}) + '"><button class="btn btn-primary" type="button">Version ' + versions3[i] + '</button></a>';
	}
	html += ' <a href="list.html"><button class="btn btn-primary" type="button">All versions</button></a>';
	$("#contents").html(html);
}


//=================================================================
//=============================================== Reports list page
//=================================================================

function filter_list()
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
		if ((typeof(search[filter]) == 'undefined') || (search[filter] == '')) continue;
		reports = $.grep(reports, function(elt, index) {
			return((elt[filter] == search[filter]) || (typeof(elt[filter]) == 'undefined'));
		});
	}
	
	return(reports);
}


function build_list()
{
	var reports = filter_list();
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
			datum.title_html = '<a href="' + homedir + '/' + reports[i].result + '">' + reports[i].title + '</a>';
		else
			datum.title_html = reports[i].title;
		datum.status_html = '<a href="' + url + '?' + BuildSearchString({log: i}) + '">' + ((reports[i].status) ? 'OK' : 'Error') + '</a>';
		datum.gramps_version_float = (parseFloat(datum.gramps_version) / 10.0).toFixed(1);
		data.push(datum);
	}
	$('#reports').bootstrapTable({
		columns: [{
			field: 'title_html',
			sortName: 'title',
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
			field: 'gramps_version_float',
			title: 'Gramps version',
			filterControl: 'select',
			align: 'center',
			sortable: true
		}, {
			field: 'status_html',
			sortName: 'status',
			title: 'Status',
			filterControl: 'select',
			align: 'center',
			sortable: true
		}, {
			field: 'time',
			title: 'Execution time',
			filterControl: 'select',
			align: 'center',
			sortable: true
		}],
		data: data,
		filterControl: false,
		search: true,
		showColumns: true,
		cookie: true,
		cookieIdTable: 'gramps-example-reports-list'
	});
}


//=================================================================
//=================================================== log page
//=================================================================

function build_log()
{
	var reports = filter_list();
	var report = reports[search.log];
	var build = builds['gramps' + report.gramps_version];
	var html = '';
	html += '<p>Report log for the report <strong><em>' + report.title + '</em></strong> (name: <strong><em>' + report.name + '</em></strong>, id: <strong><em><mark>' + report.id + '</mark></em></strong>)</p>';
	html += '<ul>';
	html += '<li>Gramps commit: <a href="https://github.com/' + build.user + '/gramps/commit/' + report.commit_gramps + '">' + report.commit_gramps + '</a></li>';
	if (report.type == 'Addon')
		html += '<li>Addons commit: <a href="https://github.com/' + build.user + '/addons/commit/' + report.commit_addons + '">' + report.commit_addons + '</a></li>';
	html += '<li>Example reports commit: <a href="https://github.com/' + build.user + '/gramps-example-reports/commit/' + report.commit_examples + '">' + report.commit_examples + '</a></li>';
	html += '<li>Travis build: <a href="https://travis-ci.org/' + build.user + '/gramps-example-reports/builds/' + report.travis_build_id + '"># ' + report.travis_build_number + '</a></li>';
	html += '</ul>';
	var txt = report.log
	var txt = txt.replace(/&/g, '&amp;');
	var txt = txt.replace(/>/g, '&gt;');
	var txt = txt.replace(/</g, '&lt;');
	var re = new RegExp('(Using options string.*name=)(' + report.id + ')([ ,\\n].*)', 'g');
	// var txt = txt.replace(re, '<p><span class="alert alert-danger" role="alert">$1<mark>$2</mark>$3</span></p>');
	// var txt = txt.replace(re, '<p class="alert">$1<mark>$2</mark>$3</p>');
	var txt = txt.replace(re, '<p class="bg-danger">$1<mark>$2</mark>$3</p>');
	html += '<pre>' + txt + '</pre>';
	$("#contents").html(html);
}
