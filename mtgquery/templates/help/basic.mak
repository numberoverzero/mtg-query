<%!
    import mtgquery.templates.util.common_js as common_js
%>
<%inherit file="../mtgquery_base.mak"/>
<%namespace name="base" file="../components/base.mak"/>

<%def name="body()">
${parent.body()}
<div class="row-fluid">
  <div class="well well-small span6 offset3">
    ${contents |n}
  </div>
  <div class="span3" />
</div>
</%def>

<%def name="js_onready()">
${parent.js_onready()}
${common_js.card_tooltips() |n}
</%def>