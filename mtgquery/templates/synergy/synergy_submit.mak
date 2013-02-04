<%! import mtgquery.templates.util.common_js as common_js %>
<%inherit file="../mtgquery_base.mak"/>
<%namespace name="base" file="../components/base.mak"/>
<%namespace name="form" file="synergy_form.mak"/>

<%def name="body()">
${parent.body()}
<div class="row-fluid">
  <div class="span4 offset4">
    % if base.isdef('form_name'):
    ${form.form("Synergy", name=form_name, description=form_description, cards_text=form_cards_text)}
    % else:
    ${form.form("Synergy")}
    % endif
  </div>
  <div class="span4"/>
</div>
</%def>

<%def name="css()">
${parent.css()}
</%def>

<%def name="js()">
${parent.js()}
${form.form_js()}
</%def>

<%def name="js_onready()">
${parent.js_onready()}
${form.form_js_onready()}
</%def>