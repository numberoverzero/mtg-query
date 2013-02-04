<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3/org/1999/xhtml">
<head>
  ${self.head()}
  ${self.css()}
</head>

<body>
  ${self.body()}
  ${self.js()}
  <script>
  ${"$(document).ready(function(){" |n}
  ${self.js_onready()}
  ${"});" |n}
  </script>
</body>
</html>
<%def name="head()">
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
</%def>
<%def name="css()"></%def>
<%def name="js()">
${js_script("http://ajax.googleapis.com/ajax/libs/jquery/1.7/jquery.js")}
${js_script("/js/underscore-min.js")}
</%def>

<%def name="js_onready()">
</%def>

<%def name="isdef(var)"><%
  return var in context.kwargs
%></%def>
<%def name="get_var(var, default=None)"><%
  return context.kwargs[var] if isdef(var) else default
%></%def>
<%def name="css_link(path, media='')">
  <link rel="stylesheet" type="text/css" href="${path|h}" media="${media}"></link>
</%def>
<%def name="js_script(path)">
  <script src="${path}"></script>
</%def>