var margin = {top: 30, right: 20, bottom: 30, left: 20},
 width = 1024 - margin.left - margin.right,
 textMargin = 5.5,
 barHeight = 20,
 i = 0,
 duration = 400,
 contraction = 3,
 root;

var tree = d3.layout.tree().nodeSize([0, 20]);

var diagonal = d3.svg.diagonal().projection(function(d) {
 return [d.y, d.x];
});

var maxWidth = width;

var svg = d3.select("div.div_svg").append("svg")
 .attr("width", width + margin.left + margin.right).append("g")
 .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var calc_div = d3.select("div.calc_svg");
var svg1 = d3.select("div.calc_svg").append("svg")
 .attr("width", width + margin.left + margin.right)
 .append("g").attr("class", "node_test");

d3.json("json/indentedtree-index.json", function(error, descendant) {
 descendant.x0 = 0;
 descendant.y0 = 0; 
 calc_max_width(root = descendant);
 if (width < maxWidth) {
  width = maxWidth;
  d3.select("div.div_svg").select("svg").attr("width", width + margin.left + margin.right);
 }
});

function calc_max_width(source) {
 var nodes = tree.nodes(root);
 var node = svg1.selectAll("g.node_test")
  .data(nodes)
  .enter()
  .append("text")
  .text(set_text)
  .each(function(d) {
    wid = this.getBBox().width;
    newmax = (wid + d.y + margin.right + margin.left);
    if (maxWidth < newmax) {
     maxWidth = newmax;
    }
  });
 calc_div.select("svg").remove();
}

var tip = d3.tip()
 .attr("class", "d3-tip")
 .style("background", "#000000")
 .style("color", "#ffffff")
 .offset([-10, 0])
 .html(function(d) {
  return set_biography_text(d);
 });

svg.call(tip);

d3.json("json/indentedtree-index.json", function(error, descendant) {
 descendant.x0 = 0;
 descendant.y0 = 0;
 set_initial_contraction(root = descendant);
 update(root = descendant);
});

function set_initial_contraction(source) {
 var nodes = tree.nodes(root);
 nodes.forEach(function(n, i) {
  if (n.depth >= (contraction-1) && n.children) {
   n._children = n.children;
   n.children = null;
  }
 });
}

function update(source) {
 // Compute the flattened node list. TODO use d3.layout.hierarchy.
 var nodes = tree.nodes(root);
 var height = Math.max(500, nodes.length * barHeight +
  margin.top + margin.bottom);

 d3.select("svg").transition().duration(duration).attr("height", height);

 d3.select(self.frameElement).transition().duration(duration)
  .style("height", height + "px");

 // Compute the "layout".
 nodes.forEach(function(n, i) {
  // Set X Co-ordinate for each node
  n.x = i * barHeight;
 });

 // Update the nodes
 var node = svg.selectAll("g.node")
  .data(nodes, function(d) { return d.id || (d.id = ++i); });

 var nodeEnter = node.enter().append("g")
  .attr("class", "node")
  .attr("transform", function(d) {
    return "translate(" + source.y0 + "," + source.x0 + ")";
   })
  .style("opacity", 1e-6);

 // Enter any new nodes at the parents previous position.
 nodeEnter.append("rect")
  .attr("y", -barHeight / 2)
  .attr("height", barHeight)
  .attr("width", function(n) { return maxWidth - n.y;})
  .attr("cursor", "pointer")
  .on("click", click)
  .on("mouseover", tip.show)
  .on("mousemove", function(d) {
   tip.style("top", (d3.event.pageY-10)+"px")
   tip.style("left", (d3.event.pageX+10)+"px");})
  .on("mouseout", tip.hide)
  .style("fill", color);

 nodeEnter.append("text")
  .attr("dy", 3.5)
  .attr("dx", textMargin)
  .text(set_text);

 // Transition nodes to their new position.
 node.transition()
  .select("text")
  .text(set_text);

 nodeEnter.transition()
  .duration(duration)
  .attr("transform", function(d) {
    return "translate(" + d.y + "," + d.x + ")";
   })
  .style("opacity", 1);

 node.transition()
  .duration(duration)
  .attr("transform", function(d) {
    return "translate(" + d.y + "," + d.x + ")";
   })
  .style("opacity", 1)
  .select("rect")
  .style("fill", color);

 // Transition exiting nodes to the parents new position.
 node.exit().transition()
  .duration(duration)
  .attr("transform", function(d) {
    return "translate(" + source.y + "," + source.x + ")";
   })
  .style("opacity", 1e-6)
  .remove();

 // Update the links
 var link = svg.selectAll("path.link")
  .data(tree.links(nodes), function(d) { return d.target.id; });

 // Enter any new links at the parents previous position.
 link.enter().insert("path", "g")
  .attr("class", "link")
  .attr("d", function(d) {
    var o = {x: source.x0, y: source.y0};
    return diagonal({source: o, target: o});
   })
  .transition()
  .duration(duration)
  .attr("d", diagonal);

 // Transition links to their new position.
 link.transition()
  .duration(duration)
  .attr("d", diagonal);

 // Transition exiting nodes to the parents new position.
 link.exit().transition()
  .duration(duration)
  .attr("d", function(d) {
    var o = {x: source.x, y: source.y};
    return diagonal({source: o, target: o});
   })
  .remove();

 // Stash the old positions for transition.
 nodes.forEach(function(d) {
  d.x0 = d.x;
  d.y0 = d.y;
 });
}

// Toggle children on click.
function click(d) {
 if (d.children) {
  d._children = d.children;
  d.children = null;
 } else {
  d.children = d._children;
  d._children = null;
 }
 update(d);
}

function color(d) {
 return d._children ? "#3182bd" : d.children ? "#c6dbef" : "#fd8d3c";
}

function set_text(d) {
 var ret_str = d.display_num + " " + d.name + " (" + d.born + " - " + d.died + ")";
 if (d.display_num == "sp.") {
  if (d.marriage !== undefined && d.marriage.length > 0) {
   ret_str = ret_str + ", " + d.marriage;
  }
  if (d.divorve !== undefined && d.divorce.length > 0) {
   ret_str = ret_str + ", " + d.divorce;
  }
 }
 return ret_str;
}

function set_biography_text(d) {
 var ret_str = "<div class='bio_box'>";
 if (d.image_ref !== undefined) {
    ret_str = ret_str + "<img align='right' alt='' border=0 src='";
    ret_str = ret_str + d.image_ref + "'/>";
 }
 ret_str = ret_str + "<p class='bio_header'><strong>" + d.name + "</strong></p>";
 ret_str = ret_str + "<div class='bio_text'>" + d.biography + "</div>";
 ret_str = ret_str + "</div>";

 return ret_str;
}

