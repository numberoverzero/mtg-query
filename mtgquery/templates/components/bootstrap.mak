<%inherit file="base.mak"/>
<%namespace name="base" file="base.mak"/>

<%def name="head()">
${parent.head()}
<meta name="viewport" content="width=device-width, intitial-scale=1.0"/>
</%def>

<%def name="css()">
${parent.css()}
##${base.css_link('//netdna.bootstrapcdn.com/bootswatch/2.1.1/slate/bootstrap.min.css')}
##${base.css_link('//netdna.bootstrapcdn.com/twitter-bootstrap/2.2.2/css/bootstrap-responsive.min.css')}
${base.css_link("//netdna.bootstrapcdn.com/twitter-bootstrap/2.2.2/css/bootstrap-combined.min.css")}
</%def>

<%def name="js()">
${parent.js()}
${base.js_script("//netdna.bootstrapcdn.com/twitter-bootstrap/2.2.2/js/bootstrap.min.js")}
</%def>

<%def name="js_onready()">
${parent.js_onready()}
</%def>