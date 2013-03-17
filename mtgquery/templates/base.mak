<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3/org/1999/xhtml">
<head>
  <%block name="head">
    <meta name="viewport" content="width=device-width, intitial-scale=1.0"/>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
  </%block>
  <%block name="css">
    ${css_link("//netdna.bootstrapcdn.com/bootswatch/2.3.0/cyborg/bootstrap.min.css")}
    ${css_link('/css/mtgquery.css', 'screen')}
  </%block>
</head>
<body>
% if navbar_index:
  ${comp.navbar("Synergy", "/", left_links, right_links, navbar_index)}
% endif
  ${next.body()}
<%block name="js">
  ${js_script("http://ajax.googleapis.com/ajax/libs/jquery/1.7/jquery.js")}
  ${js_script("//cdnjs.cloudflare.com/ajax/libs/underscore.js/1.4.4/underscore-min.js")}
  ${js_script("//netdna.bootstrapcdn.com/twitter-bootstrap/2.2.2/js/bootstrap.min.js")}
</%block>
  <script>
    ${"$(document).ready(function(){" |n}
    <%block name="js_onready"/>
    ${"});" |n}
  </script>
</body>
</html>
<%! left_links = [["Submit", "Search", "Random", "Newest"], ["/submit", "/search", "/random", "/new"]] %>
<%! right_links = [["Help"], ["/help"]] %>
<%namespace name="comp" file="components.mak"/>
<%def name="css_link(path, media='')"><link rel="stylesheet" type="text/css" href="${path|h}" media="${media}"></%def>
<%def name="js_script(path)"><script src="${path}"></script></%def>