<%!
    import mtgquery.templates.util.common_js as common_js
%>

<%inherit file="../mtgquery_base.mak"/>
<%namespace name="base" file="../components/base.mak"/>
<%namespace name="raw" file="synergy_view_data.mak"/>
<%def name="body()">
${parent.body()}
<div class="row-fluid">
  <div class="span8 offset2">
    <div id="notification-area"></div>
  </div>
  <div class="span2"/>
</div>
<div class="well well-small container">
    ${raw.render(name, description, counts, urls, link_alt_href, 'Basic View', new_link_href=copy_from_href)}
</div>
</%def>

<%def name="css()">
${parent.css()}
</%def>

<%def name="js()">
${parent.js()}
% if len(notifications) > 0:
${base.js_script("/js/jquery.notifier.js")}
% endif
</%def>

<%def name="js_onready()">
${parent.js_onready()}
${raw.js_onready()}
% if len(notifications) > 0:
${common_js.notifier_init("notify", "notification-area", 3, notifications=(n.msg for n in notifications)) |n }
% endif
</%def>