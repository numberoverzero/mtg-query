<%inherit file="../mtgquery_base.mak"/>
<%namespace name="form" file="trade_form.mak"/>

<%def name="body()">
${parent.body()}
${form.form("Price Comparison")}
</%def>

<%def name="css()">
${parent.css()}
${form.form_css()}
</%def>

<%def name="js()">
${parent.js()}
${form.form_js()}
</%def>

<%def name="js_onready()">
${parent.js_onready()}
${form.form_js_onready()}
</%def>