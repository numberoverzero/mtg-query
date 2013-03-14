<%inherit file="components/bootstrap.mak"/>
<%namespace name="base" file="components/base.mak"/>
<%namespace name="components" file="components/components.mak"/>

<%def name="body()">
<% navbar_index = base.get_var('navbar_index', None) %>
${components.navbar("mtg-query", "/", ["Synergy", "Help"], ["/synergy", "/help"], navbar_index)}
${parent.body()}
</%def>

<%def name="css()">
${parent.css()}
${base.css_link('/css/mtgquery.css', 'screen')}
</%def>

<%def name="js_onready()">
${parent.js_onready()}
</%def>